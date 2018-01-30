import logging
import os
import sys, traceback
from django.conf import settings
from django.db import transaction
from fitting.utils import gen_file_name
from . import upload
from fitting.models import Scan, ScanAttribute, Scanner
from pathlib import Path
from .attributes import *
from blender_scripts.worker import execute_blender_script

STL_EXTENSION = 'stl'


def set_default_scan(user, scan):

    default_scans = user.default_scans.filter(model_type=scan.model_type)
    for s in default_scans:
        user.default_scans.remove(s)
    user.default_scans.add(scan)
    user.save()

def create_file(file_name):
    file_path = os.path.join(
        os.sep,
        settings.MEDIA_ROOT,
        file_name
    )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    Path(file_path).touch()
    return file_path


def create_scan_visualization(scan):
    BLENDER_EXTENSION = 'blend'
    scan_3d = ScanAttribute(name='scan_3d', scan=scan)
    scan_image = ScanAttribute(name='scan_image', scan=scan)
    blender_file_name = gen_file_name(scan, '{}.{}'.format(scan.model_type, BLENDER_EXTENSION))
    blender_file_path = create_file(blender_file_name)

    execute_blender_script(
        script='stl_to_blend.py',
        out_file=blender_file_path,
        params=[scan.attachment.path],
    )
    execute_blender_script(
        script='prepare_scan.py',
        in_file=blender_file_path,
    )

    image_file_name = gen_file_name(scan, '{}.{}'.format(scan.model_type, 'png'))
    image_file_path = create_file(image_file_name)

    execute_blender_script(
        script='generate_image.py',
        in_file=blender_file_path,
        out_file=image_file_path,
        params=['768', '1366'],
    )
    scan_image.value = '/'.join([settings.PROXY_HOST] + image_file_path.split('/')[2:])
    scan_image.save()
    
    json_file_name = gen_file_name(scan, '{}.{}'.format(scan.model_type, 'json'))
    json_file_path = create_file(json_file_name)

    execute_blender_script(
        script='blend4web_json.py',
        in_file=blender_file_path,
        out_file=json_file_path,
    )

    if os.path.exists(blender_file_path):
        os.remove(blender_file_path)
    if os.path.exists(blender_file_path + '1'):
        os.remove(blender_file_path + '1')
    scan_3d.value = '/'.join([settings.PROXY_HOST] + json_file_path.split('/')[2:])
    scan_3d.save()


@transaction.atomic
def update_scan(user, scanner, scan_id, scan_type, scan_path):

    try:
        scan = Scan.objects.get(user=user, model_type=scan_type, scan_id=scan_id)
    except Scan.DoesNotExist:
        scan = Scan(user=user, model_type=scan_type, scan_id=scan_id)
    
    scan.scan_id = scan_id
    scan.scanner = scanner
    foot_attachment_content = upload(scan_path)
    attachment_name = gen_file_name(scan, '{}.{}'.format(scan_type, STL_EXTENSION))
    attachment_path = create_file(attachment_name)
    Path(attachment_path).write_bytes(foot_attachment_content)
    
    scan.attachment = attachment_name
    scan.save()

    ScanAttribute.objects.filter(scan=scan).delete()

    sc = Scanner.objects.filter(scanner_id=scanner).first()
    scan_url = sc.storage_account.get_account_url() if sc is not None else user.base_url
    logger.debug(scan_url)
    try:
        update_scan_attributes(scan_url, scan, scan_type)
    except requests.HTTPError:
        logger.debug('HTTPError')
        traceback.print_exc(file=sys.stdout)
    if scan.attachment:
        create_scan_visualization(scan)

    return scan

