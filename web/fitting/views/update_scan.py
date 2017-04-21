from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
import requests
import csv
from fitting.models import Scan, User, Attribute
from fitting.utils import upload, CompareShoesThread
from django.core.files.base import ContentFile
import logging

from web.settings import str2bool

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def update_scan_view(request):
    user_uuid = request.GET['user']
    scanner = request.GET['scanner']
    scan_id = request.GET['scan']
    scan_type = request.GET['type']
    try:
        is_scan_default = str2bool(request.GET['is_default'])
    except MultiValueDictKeyError:
        is_scan_default = False

    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        user = User(uuid=user_uuid)
        user.save()
    try:
        scan = update_scan(user, scanner, scan_id, scan_type)
    except ValueError:
        return HttpResponseBadRequest()

    if is_scan_default or not user.default_scan_id:
        user.default_scan_id = scan.id
        user.save()

    return HttpResponse(
        json.dumps(str(scan))
    )


@transaction.atomic
def update_scan(user, scanner, scan_id, scan_type):

    left_foot_path = '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id)
    right_foot_path = '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id)
    try:
        left_foot_attachment = ContentFile(upload(left_foot_path))
    except ValueError:
        left_foot_attachment = ContentFile(b'')
    try:
        right_foot_attachment = ContentFile(upload(right_foot_path))
    except ValueError:
        right_foot_attachment = ContentFile(b'')

    try:
        left_scan = Scan.objects.get(user=user, scan_type=scan_type, scan_id=scan_id)
    except Scan.DoesNotExist:
        left_scan = Scan(user=user, scan_type=scan_type, scan_id=scan_id)
    left_scan.scan_id = scan_id
    left_scan.scanner = scanner
    left_scan.attachment = left_foot_attachment
    print('_________________________________')
    print(left_foot_attachment)
    left_scan.save()

    # try:
    #     scan_images = Attribute.objects.get(user=user, name='scan_image', scan_id=scan.id)
    # except Attribute.DoesNotExist:
    #     scan_images = Attribute(user=user, name='scan_image', scan_id=scan.id)
    # try:
    #     update_scan_attributes(user, user.base_url, left_scan, 'left')
    #     scan_images.value_for_left = get_scan_image_url(path_left_foot_in_fitting_service)
    # except requests.HTTPError:
    #     pass
    # try:
    #     update_scan_attributes(user, user.base_url, left_scan, 'right')
    #     scan_images.value_for_right = get_scan_image_url(path_right_foot_in_fitting_service)
    # except requests.HTTPError:
    #     pass

    # scan_images.save()
    # try:
    #     scan_3d = Attribute.objects.get(user_id=user.id, name='scan_3d', scan_id=scan.id)
    # except Attribute.DoesNotExist:
    #     scan_3d = Attribute(user_id=user.id, name='scan_3d', scan_id=scan.id)
    # scan_3d.value_for_right = get_3d_url(path_left_foot_in_fitting_service, path_right_foot_in_fitting_service)
    # scan_3d.save()
    # CompareShoesThread(scan.id).start()

    return left_scan


def get_3d_url(left_foot, right_foot):
    get_scan_3d = requests.post(
        url='http://else-3d-service.cloudapp.net/scripts/scans_to_json',
        data=json.dumps({'left_stl_url': left_foot, 'right_stl_url': right_foot}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_3d.raise_for_status()
    return get_scan_3d.json()['result_json_url']


def get_scan_image_url(url):
    get_scan_image = requests.post(
        url='http://else-3d-service.cloudapp.net/scripts/stl_to_image',
        data=json.dumps({'stl_url': url, 'resolution': [384, 683]}),
        headers={
            'Content-Type': 'application/json'
        }
    )
    get_scan_image.raise_for_status()
    return get_scan_image.json()['result_image_url']


def update_scan_attributes(user_id, base_url, scan, scan_type):
    path_to_csv = '{}{}/{}/{}_{}_mes.csv'.format(base_url, scan.scanner, scan.scan_id, scan.scan_id, scan_type)
    request = requests.get(path_to_csv)
    profile = list(request.iter_lines(decode_unicode=True))[1:]
    request.raise_for_status()
    for row in csv.DictReader(profile, delimiter=';'):
        for key, value in row.items():
            if key != '':
                try:
                    attribute = Attribute.objects.get(user_id=user_id, name=key, scan_id=scan.id)
                except Attribute.DoesNotExist:
                    attribute = Attribute(user_id=user_id, name=key, scan_id=scan.id)
                if scan_type == 'left':
                    attribute.value_for_left = value
                else:
                    attribute.value_for_right = value
                attribute.save()
