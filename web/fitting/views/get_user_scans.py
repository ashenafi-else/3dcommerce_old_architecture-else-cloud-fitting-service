from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from fitting.models import User, Scan, ModelType
import logging


logger = logging.getLogger(__name__)


def get_foot_scans(user):

    result = {}
    scans = Scan.objects.filter(Q(model_type=ModelType.TYPE_LEFT_FOOT) | Q(model_type=ModelType.TYPE_RIGHT_FOOT), user=user,)
    for scan in scans:
        result[scan.scan_id] = {
            'scan_id': scan.scan_id,
            'scanner': scan.scanner,
            'created_date': scan.created_date.strftime("%A, %d. %B %Y %I:%M%p")
        }
    return result.values()


get_scans = {
	ModelType.TYPE_FOOT: get_foot_scans
}


@csrf_exempt
def get_user_scans(request):

    user_uuid = request.GET['user']
    scan_type = request.GET.get('type', ModelType.TYPE_FOOT)
    user = User.objects.get(uuid=user_uuid)
    scans = Scan.objects.filter(user=user)
    user_scans = list(get_scans[scan_type](user))
    
    return HttpResponse(json.dumps({'user_scans': user_scans}))
