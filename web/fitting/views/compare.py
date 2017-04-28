from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import Scan, User, CompareResult, Last
from .utils import compare_by_metrics
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def compare(request):

    BEST_STYLE_MAX_VALUE = 100
    user_uuid = request.GET['user_uuid']
    shoe_uuid = request.GET['shoe_uuid']

    prev_shoe = None
    next_shoe = None

    user = User.objects.get(uuid=user_uuid)
    scan = Scan.objects.filter(user=user,).first()
    best_size_score = BEST_STYLE_MAX_VALUE
    best_size_result = None

    shoes = Last.objects.filter(product__uuid=shoe_uuid)
    for shoe in shoes:
        try:
            compare_result = CompareResult.objects.get(last=shoe, scan_1=scan)
        except CompareResult.DoesNotExist:
            compare_result = compare_by_metrics(scan, shoe)
        if best_size_score > compare_result.compare_result:
            best_size_score = compare_result.compare_result
            best_size_result = compare_result
        logger.debug(compare_result)
    result = {}
    # try:
    #     shoe = Shoe.objects.get(uuid=shoe_uuid, size=user.size)
    #     best_style_result = CompareResults.objects.get(shoe_id=shoe.id, scan_id=scan.id)
    # except Shoe.DoesNotExist:
    #     best_style_result = CompareResults(compare_result=BEST_STYLE_MAX_VALUE, output_model="")

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
