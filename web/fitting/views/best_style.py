from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from fitting.models import Scan, User, CompareResult, Last
from .utils import compare_by_metrics
import json

@csrf_exempt
def best_style(request):
    user_uuid = request.GET['user']
    product_uuid = request.GET['product']
    size_type = request.GET['size_type']
    scan_type = request.GET.get('scan_type', 'foot_right')
    user = User.objects.get(uuid=user_uuid)

    last = Last.objects.filter(product__uuid=product_uuid, size__size_type=size_type).first()
    scan = Scan.objects.filter(user=user, scan_type=scan_type).first()
    result = {}

    if last and scan:
        best_style = CompareResult.objects.filter(last=last, scan_1=scan)

        if best_style.exists():
            best_style = best_style.first()
        else:
            best_style = compare_by_metrics(scan, last)

        result['best_style'] = {
            'score': best_style.compare_result,
            'output_model': best_style.output_model,
            'size': str(best_style.last.size),
        }
    else:
        result['best_style'] = {
            'score': 0.0,
            'output_model': '',
            'size': None,
        }

    return HttpResponse(json.dumps(result))
