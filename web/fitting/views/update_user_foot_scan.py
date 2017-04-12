from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
import requests
import csv
from fitting.models import Scan, User, Attribute
from fitting.utils import upload_to_fitting, CompareShoesThread
import logging

from web.settings import str2bool

logger = logging.getLogger(__name__)


@csrf_exempt
@transaction.atomic
def update_user_foot_scan(request):
    user_uuid = request.GET['user_uuid']
    scanner = request.GET['update_scanner']
    scan_id = request.GET['update_scan_id']
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
        json.dumps(
            {
                'left': scan.path_left_foot_in_fitting_service,
                'right': scan.path_right_foot_in_fitting_service
            }
        )
    )


@transaction.atomic
def update_scan(user, scanner, scan_id, scan_type):

    original_left_foot_path = '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id)
    original_right_foot_path = '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id)
    try:
        scans = Scan.objects.filter(
            original_right_foot_path=original_right_foot_path,
            original_left_foot_path=original_left_foot_path
        )
        path_left_foot_in_fitting_service = scans[0].path_left_foot_in_fitting_service
        path_right_foot_in_fitting_service = scans[0].path_right_foot_in_fitting_service

    except IndexError:
        try:
            path_left_foot_in_fitting_service = upload_to_fitting(original_left_foot_path, 'UploadScan')
        except ValueError:
            path_left_foot_in_fitting_service = ''
        try:
            path_right_foot_in_fitting_service = upload_to_fitting(original_right_foot_path, 'UploadScan')
        except ValueError:
            path_right_foot_in_fitting_service = ''
            if path_left_foot_in_fitting_service == '' and path_right_foot_in_fitting_service == '':
                raise ValueError

    try:
        scan = Scan.objects.get(user_id=user.id, type=scan_type, scan_id=scan_id)
    except Scan.DoesNotExist:
        scan = Scan(user_id=user.id, type=scan_type, scan_id=scan_id)
    scan.scan_id = scan_id
    scan.scanner = scanner
    scan.original_left_foot_path = original_left_foot_path
    scan.original_right_foot_path = original_right_foot_path
    scan.path_left_foot_in_fitting_service = path_left_foot_in_fitting_service
    scan.path_right_foot_in_fitting_service = path_right_foot_in_fitting_service
    scan.save()

    try:
        scan_images = Attribute.objects.get(user_id=user.id, name='scan_image', scan_id=scan.id)
    except Attribute.DoesNotExist:
        scan_images = Attribute(user_id=user.id, name='scan_image', scan_id=scan.id)
    try:
        update_scan_attributes(user.id, user.base_url, scan, 'left')
        scan_images.value_for_left = get_scan_image_url(path_left_foot_in_fitting_service)
    except requests.HTTPError:
        pass
    try:
        update_scan_attributes(user.id, user.base_url, scan, 'right')
        scan_images.value_for_right = get_scan_image_url(path_right_foot_in_fitting_service)
    except requests.HTTPError:
        pass

    scan_images.save()
    try:
        scan_3d = Attribute.objects.get(user_id=user.id, name='scan_3d', scan_id=scan.id)
    except Attribute.DoesNotExist:
        scan_3d = Attribute(user_id=user.id, name='scan_3d', scan_id=scan.id)
    scan_3d.value_for_right = get_3d_url(path_left_foot_in_fitting_service, path_right_foot_in_fitting_service)
    scan_3d.save()
    CompareShoesThread(scan.id).start()

    return scan


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
