from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import User, ScanAttribute, Scan


@csrf_exempt
def get_user_profile(request):
    user_uuid = request.GET['user_uuid']
    scan_id = request.GET['scan']
    user_profile = {}
    user = User.objects.get(uuid=user_uuid)
    scans = Scan.objects.filter(user=user, scan_id=scan_id)
    for scan in scans:
        attributes = ScanAttribute.objects.filter(scan=scan)
        for attribute in attributes:
            if attribute.name not in user_profile:
                user_profile[attribute.name] = {}
            user_profile[attribute.name][scan.model_type] = attribute.value

    return HttpResponse(json.dumps(user_profile))
