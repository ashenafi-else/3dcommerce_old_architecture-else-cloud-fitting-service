import logging
import sys, traceback
import requests
from django.db import transaction
from .update_scan import update_scan
from fitting.models import ModelType

logger = logging.getLogger(__name__)


@transaction.atomic
def update_foot_scans(user, scanner, scan_id, scan_type):
	try:
		left_scan = update_scan(user, scanner, scan_id, ModelType.TYPE_LEFT_FOOT, '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id))
	except requests.HTTPError:
		traceback.print_exc(file=sys.stdout)
		left_scan = None
	try:
		right_scan = update_scan(user, scanner, scan_id, ModelType.TYPE_RIGHT_FOOT, '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id))
	except requests.HTTPError:
		traceback.print_exc(file=sys.stdout)
		right_scan = None
	if left_scan is None and right_scan is None:
		raise ValueError('Left and right scans aren`t exist together')
	return [
		left_scan,
		right_scan
	]

