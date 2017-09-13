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
def get_default_size_view(request):
    user_uuid = request.GET['user']
    size_type = request.GET.get('type', ModelType.TYPE_FOOT)
    
    user = User.objects.get(uuid=user_uuid)
    size = user.sizes.filter(model_type=size_type).first()

    return HttpResponse(
        json.dumps({ 'default_size': size.value })
    )
