import logging
import os
from django.conf import settings
from django.db import transaction
from fitting.utils import gen_file_name
from . import upload
from fitting.models import Scan, ScanAttribute
from pathlib import Path
from .attributes import *

STL_EXTENSION = 'stl'


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
    attachment_path = os.path.join(
        os.sep,
        settings.MEDIA_ROOT,
        attachment_name
    )
    os.makedirs(os.path.dirname(attachment_path), exist_ok=True)
    Path(attachment_path).touch()
    Path(attachment_path).write_bytes(foot_attachment_content)
    
    scan.attachment = attachment_name
    scan.save()

    try:
        scan_image = ScanAttribute.objects.get(name='scan_image', scan=scan)
    except ScanAttribute.DoesNotExist:
        scan_image = ScanAttribute(name='scan_image', scan=scan)
    try:
        update_scan_attributes(user.base_url, scan, scan_type)
        scan_image.value = get_scan_image_url(scan_path)
    except requests.HTTPError:
        logger.debug('HTTPError')

    scan_image.save()
    # try:
    #     scan_3d = Attribute.objects.get(user=user, name='scan_3d', scan=scan)
    # except Attribute.DoesNotExist:
    #     scan_3d = Attribute(user_id=user, name='scan_3d', scan=scan)
    # try:
    # 	scan_3d.value = get_3d_url(scan_path)
    # except requests.HTTPError:
    #     logger.debug('HTTPError')
    # scan_3d.save()
    # CompareShoesThread(scan).start()

    return scan

