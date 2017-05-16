from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from fitting.models import Size, User, ModelType
from .utils import set_default_scan
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def set_default_size_view(request):
    user_uuid = request.GET['user']
    size_value = request.GET['size']
    size_type = request.GET.get('type', ModelType.TYPE_FOOT)
    
    user = User.objects.get(uuid=user_uuid)
    size = Size.objects.get(value=size_value, model_type=size_type)
    for s in Size.objects.filter(model_type=size_type):
    	user.sizes.remove(s)
    user.sizes.add(size)
        
    return HttpResponse(
        json.dumps({ 'default_size': str(size) })
    )
