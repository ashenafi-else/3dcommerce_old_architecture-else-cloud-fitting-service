from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fitting.models import Scan, User, CompareResult, Last, ModelType, Size, Product
from .utils import compare_by_metrics
import json


compare_methods = {
    CompareResult.MODE_METRICS: compare_by_metrics
}


def get_best_style(scan, last, compare_type):

    result = {}

    if last and scan:
        best_style = CompareResult.objects.filter(last=last, scan_1=scan).first()
        result['best_style'] = {
            'score': int(best_style.compare_result),
            'output_model': best_style.output_model,
            'output_model_3d': best_style.output_model_3d,
            'size': best_style.last.size.value,
            'size_type': best_style.last.size.model_type
        }
    else:
        result['best_style'] = {
            'score': 0,
            'output_model': '',
            'output_model_3d': '',
            'size': None,
            'size_type': None
        }
    return result


def foot_best_style(product, user, scan_id, size, compare_type):

    result = {}

    if scan_id is None:
        left_scan = user.default_scans.filter(model_type=ModelType.TYPE_LEFT_FOOT).first()
        right_scan = user.default_scans.filter(model_type=ModelType.TYPE_RIGHT_FOOT).first()
    else:
        left_scan = Scan.objects.filter(user=user, scan_id=scan_id, model_type=ModelType.TYPE_LEFT_FOOT).first()
        right_scan = Scan.objects.filter(user=user, scan_id=scan_id, model_type=ModelType.TYPE_RIGHT_FOOT).first()

    left_last = Last.objects.filter(product=product, model_type=ModelType.TYPE_LEFT_FOOT, size=size).first()
    right_last = Last.objects.filter(product=product, model_type=ModelType.TYPE_RIGHT_FOOT, size=size).first()

    try:
        left_result = get_best_style(left_scan, left_last, compare_type)
        right_result = get_best_style(right_scan, right_last, compare_type)
    except CompareResult.DoesNotExist:
        compare_methods[compare_type](left_scan, product)
        compare_methods[compare_type](right_scan, product)
        left_result = get_best_style(left_scan, left_last, compare_type)
        right_result = get_best_style(right_scan, right_last, compare_type)

    if left_result['best_style']['size'] and right_result['best_style']['size']:
        result['best_style'] = {
            'score': (left_result['best_style']['score'] + right_result['best_style']['score']) // 2,
            'output_model': left_result['best_style']['output_model'],
            'output_model_3d': left_result['best_style']['output_model_3d'],
            'size': left_result['best_style']['size'],
            'size_type': left_result['best_style']['size_type']
        }
    else:
        result = left_result if left_result['best_style']['size'] else right_result
    return result    


scan_types = {
    ModelType.TYPE_FOOT: foot_best_style
}


@csrf_exempt
def best_style(request):
    user_uuid = request.GET['user']
    product_uuid = request.GET['product']
    scan_id = request.GET.get('scan', None)
    size_type = request.GET.get('size_type', ModelType.TYPE_FOOT)
    
    user = User.objects.get(uuid=user_uuid)
    size = user.sizes.filter(model_type=size_type).first()
    if size is None:
        user.sizes.add(Size.objects.filter(model_type=size_type).first())
    compare_type = request.GET.get('compare_type', CompareResult.MODE_METRICS)
    product = Product.objects.get(uuid=product_uuid)
    result = scan_types[size_type](product, user, scan_id, size, compare_type)

    return HttpResponse(json.dumps(result))
