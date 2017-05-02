from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last
from .utils import compare_by_metrics
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def best_style(request):

    BEST_STYLE_MAX_VALUE = 100
    user_uuid = request.GET['user_uuid']
    product_uuid = request.GET['shoe_uuid']
    scan_type = request.GET['type']

    prev_last = None
    next_last = None

    user = User.objects.get(uuid=user_uuid)
    scan = user.default_scans.filter(scan_type=scan_type).first()
    best_size_score = BEST_STYLE_MAX_VALUE
    best_size_result = None

    lasts = Last.objects.filter(product__uuid=product_uuid)
    for last in Lasts:
        try:
            compare_result = CompareResult.objects.get(last=last, scan_1=scan)
        except CompareResult.DoesNotExist:
            compare_result = compare_by_metrics(scan, last)
        if best_size_score > compare_result.compare_result:
            best_size_score = compare_result.compare_result
            best_size_result = compare_result
    
    try:
        last = Last.objects.get(product__uuid=product_uuid, size=user.size)
        best_style_result = CompareResults.objects.get(last=last, scan_id=scan.id)
    except Shoe.DoesNotExist:
        best_style_result = CompareResults(compare_result=BEST_STYLE_MAX_VALUE, output_model="")

    # try:
    #     best_size_shoe = Shoe.objects.get(id=best_size_result.shoe_id)
    # except Shoe.DoesNotExist:
    #     best_size_shoe = shoes.first()

    # try:
    #     prev_shoe = Shoe.objects.get(uuid=shoe_uuid, size=best_size_shoe.size-1)
    #     prev_best_size_result = CompareResults.objects.get(shoe_id=prev_shoe.id, scan_id=scan.id)
    # except Shoe.DoesNotExist:
    #     prev_best_size_result = None

    # try:
    #     next_shoe = Shoe.objects.get(uuid=shoe_uuid, size=best_size_shoe.size+1)
    #     next_best_size_result = CompareResults.objects.get(shoe_id=next_shoe.id, scan_id=scan.id)
    # except Shoe.DoesNotExist:
    #     next_best_size_result = None

    # result = {
    #     'best_size': {
    #         'size': best_size_shoe.size,
    #         'out_model': best_size_result.output_model
    #     },
    #     'best_style': {
    #         'style_score': BEST_STYLE_MAX_VALUE - best_style_result.compare_result,
    #         'out_model': best_style_result.output_model
    #     }
    # }

    # if prev_best_size_result:
    #     result['prev_size'] = {
    #         'size': prev_shoe.size,
    #         'out_model': prev_best_size_result.output_model
    #     }
    # if next_best_size_result:
    #     result['next_size'] = {
    #         'size': next_shoe.size,
    #         'out_model': next_best_size_result.output_model
    #     }

    return HttpResponse(json.dumps(result))
