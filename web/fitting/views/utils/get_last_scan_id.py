from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging
import re

logger = logging.getLogger(__name__)


def get_last_scan_id(user, scanner, interval):
    url = f'{user.base_url}{scanner}/?C=M;O=D'
    request = requests.get(
        url=url,
    )
    bs = BeautifulSoup(request.text, 'html.parser')
    image_tag = bs.find('img', alt='[DIR]')
    row = None
    if image_tag is not None:
        row = image_tag.find_parent('tr')
    scan_id = None
    if row is not None:
        date_tag = row.find('td', attrs={'align': 'right'},)
        string_date = None
        date = None
        if date_tag is not None:
            string_date = date_tag.string
        if string_date is not None:
            date = datetime.strptime(string_date.strip(), '%Y-%m-%d %H:%M')
        logger.debug(date)
    return scan_id