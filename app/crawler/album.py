import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from crawler.utils.parsing import get_dict_from_dl


class AlbumData:
    def __init__(self, album_id):
        self.album_id = album_id
        self.title = None
        self.url_img_cover = None
        # self.release_date = None
        # self.publisher = None
        # self.agency = None
        self.meta_dict = None

    def get_detail(self):
        url = 'https://www.melon.com/album/detail.htm'
        params = {
            'albumId': self.album_id,
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text)
        info = soup.select_one('div.section_info')
        entry = info.select_one('div.entry')
        src = info.select_one('div.thumb img').get('src')

        title = entry.select_one('div.info > .song_name').contents[2].strip()
        url_img_cover = re.search(r'(.*?)/melon/quality.*', src).group(1)
        meta_dict = get_dict_from_dl(entry.select_one('div.meta dl'))

        self.title = title
        self.url_img_cover = url_img_cover
        self.meta_dict = meta_dict

    @property
    def release_date(self):
        try:
            return datetime.strptime(self.meta_dict.get('발매일'), '%Y.%m.%d')
        except:
            return

    @property
    def publisher(self):
        return self.meta_dict.get('발매사')

    @property
    def agency(self):
        return self.meta_dict.get('기획사')
