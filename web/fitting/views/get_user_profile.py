from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import User, Attribute, Scan


@csrf_exempt
def get_user_profile(request):
    user_uuid = request.GET['user_uuid']
    user_profile = {}
    user = User.objects.get(uuid=user_uuid)
    try:
        scan_id = Scan.objects.get(user_id=user.id, scan_id=request.GET['scan_id']).id
    except (MultiValueDictKeyError, Scan.DoesNotExist):
        scan_id = user.default_scan_id
    attributes = Attribute.objects.filter(user_id=user.id, scan_id=scan_id)
    for attribute in attributes:
        user_profile[attribute.name] = {}
        user_profile[attribute.name]['left'] = attribute.value_for_left
        user_profile[attribute.name]['right'] = attribute.value_for_right

    return HttpResponse(json.dumps(user_profile))
