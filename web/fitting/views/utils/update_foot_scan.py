import logging
import requests
from django.db import transaction
from .update_scan import update_scan

logger = logging.getLogger(__name__)


@transaction.atomic
def update_foot_scans(user, scanner, scan_id, scan_type):
	try:
		left_scan = update_scan(user, scanner, scan_id, scan_type + '_left', '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id))
	except requests.HTTPError:
		left_scan = None
	try:
		right_scan = update_scan(user, scanner, scan_id, scan_type + '_right', '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id))
	except requests.HTTPError:
		right_scan = None
	if left_scan is None and right_scan is None:
		raise ValueError('Left and right scans aren`t exist together')
	return [
		left_scan,
		right_scan
	]

