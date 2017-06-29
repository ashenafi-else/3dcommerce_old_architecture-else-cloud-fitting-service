from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db.models import Q
from fitting.models import User, Scan, ModelType, ScanAttribute
from .utils.sql_helpers import sql_call
from .best_scan import get_best_foot_scan, extract_calculation_attributes
from fitting_algorithm  import metrics_comparison_config
import logging
import json

logger = logging.getLogger(__name__)


def get_foot_metrics_config(product_id):

    user_sizes = sql_call(connection, "SELECT users.id, users.uuid, sizes.value\
                        FROM fitting_user as users\
                        left outer join fitting_user_sizes as user_sizes\
                        on user_sizes.user_id = users.id\
                        left outer join fitting_size as sizes\
                        on sizes.id = user_sizes.size_id\
                        left outer join\
                        (select user_id, count(distinct id) from fitting_scan group by user_id) as scans\
                        on scans.user_id = users.id\
                        where sizes.value is not null and sizes.value not like '%.%' and scans.count > 1")

    best_scans = [(user['value'], get_best_foot_scan(user['id'])[0]) for user in user_sizes]

    scans_by_size = {}
    for scan in best_scans:

        size = float(scan[0])

        if not size in scans_by_size:
            scans_by_size[size] = {}

        scans_by_size[size][scan[1]] = {
            'LEFT': extract_calculation_attributes(ScanAttribute.objects.filter(scan=Scan.objects.filter(model_type=ModelType.TYPE_LEFT_FOOT, scan_id=scan[1]).first().id)),
            'RIGHT': extract_calculation_attributes(ScanAttribute.objects.filter(scan=Scan.objects.filter(model_type=ModelType.TYPE_RIGHT_FOOT, scan_id=scan[1]).first().id))
            }

        lasts_data = sql_call(connection,"SELECT lasts.product_id, lasts.model_type, sizes.value as size, attrs.name, attrs.scan_attribute_name, attrs.value\
                                            FROM fitting_last as lasts\
                                            left outer join fitting_lastattribute as attrs\
                                            on attrs.last_id = lasts.id\
                                            left outer join fitting_size as sizes\
                                            on sizes.id = lasts.size_id\
                                            where lasts.product_id = {0} and attrs.disabled = false and sizes.value not like '%.%' and attrs.name != ''".format(product_id))

        lasts_by_size = {}
        references = {}

        for last in lasts_data:
            if last['model_type'] == 'RIGHT_FOOT':
                continue

            if last['scan_attribute_name'] not in references:
                references[last['scan_attribute_name']] = last['name']

            size = float(last['size'])

            if size not in lasts_by_size:
                lasts_by_size[size] = {}

            lasts_by_size[size][last['name']] = float(last['value'])

    return metrics_comparison_config.generate_config(references, scans_by_size, lasts_by_size)

get_config = {
    ModelType.TYPE_FOOT: get_foot_metrics_config
}


@csrf_exempt
def generate_comparison_config(request):
    product_id = request.GET['product_id']
    scan_type = request.GET.get('type', ModelType.TYPE_FOOT)

    metrics_config = get_config[scan_type](product_id)

    return HttpResponse(json.dumps({
        'mode': 'ONLY FOR TESTS!!!!!!',
        'product_id': product_id,
        'metrics_config': metrics_config
    }))