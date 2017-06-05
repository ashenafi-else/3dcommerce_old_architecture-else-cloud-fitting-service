from django.http import HttpResponse
from django.db import models
from fitting.models import Scan, Last

from ..blender_scripts.worker import execute_blender_script

def generate_images(request):

    product_uuid = request.GET['product']
    scan_id = request.GET['scan']
    #
    product_file_path = Last.objects.get(uuid=product_uuid)
    scan_file_path = Scan.objects.get(scan_id=scan_id)

    # execute_blender_script(
    #     script='image_generator.py',
    #     out_file= # to be fixed
    #     params=
    #     blender=
    # )
    return HttpResponse('It works!')
