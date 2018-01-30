import logging
import sys, traceback
import requests
from django.db import transaction
from .update_scan import update_scan
from fitting.models import ModelType, Scanner

logger = logging.getLogger(__name__)


@transaction.atomic
def update_foot_scans(user, scanner, scan_id, scan_type):

	sc = Scanner.objects.filter(scanner_id=scanner).first()
	left_stl = f'{sc.get_scanner_url()}{scan_id}/model_l.stl' if sc is not None else '{}{}/{}/model_l.stl'.format(user.base_url, scanner, scan_id)
	right_stl = f'{sc.get_scanner_url()}{scan_id}/model_r.stl' if sc is not None else '{}{}/{}/model_r.stl'.format(user.base_url, scanner, scan_id)
	try:
		left_scan = update_scan(user, scanner, scan_id, ModelType.TYPE_LEFT_FOOT, left_stl)
	except requests.HTTPError:
		traceback.print_exc(file=sys.stdout)
		left_scan = None
	try:
		right_scan = update_scan(user, scanner, scan_id, ModelType.TYPE_RIGHT_FOOT, right_stl)
	except requests.HTTPError:
		traceback.print_exc(file=sys.stdout)
		right_scan = None
	scans = []
	if left_scan is not None:
		scans.append(left_scan)
	if right_scan is not None:
		scans.append(right_scan)
	return scans

