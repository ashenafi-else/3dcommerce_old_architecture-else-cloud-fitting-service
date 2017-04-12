from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from fitting.models import User, Scan


@csrf_exempt
def get_user_scans(request):
    user_uuid = request.GET['user_uuid']
    user = User.objects.get(uuid=user_uuid)
    scans = Scan.objects.filter(user_id=user.id)
    user_scans = []
    for scan in scans:
        user_scans.append({'scan_id': scan.scan_id, 'created_date': str(scan.created_date)})

    return HttpResponse(json.dumps({'user_scans': user_scans}))
