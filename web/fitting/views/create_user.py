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
def create_user(request):
    user_uuid = request.GET['user']
    size_value = request.GET.get('size', '35')
    size_type = request.GET.get('type', ModelType.TYPE_FOOT)
    
    user = User.objects.filter(uuid=user_uuid).first()
    if user is None:
        user = User(uuid=user_uuid)
        user.save()
        size = Size.objects.get(value=size_value, model_type=size_type)
        user.sizes.add(size)
    else:
        size = user.sizes.get(value=size_value, model_type=size_type)
        
    return HttpResponse(
        json.dumps({ 'default_size': str(size) })
    )
