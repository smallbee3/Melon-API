import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


def song_search_from_melon(request):
    keyword = request.GET.get('keyword')
    context = {}
    if keyword:
        song_info_list = []
        url = 'https://www.melon.com/search/song/index.htm'
        params = {
            'q': keyword,
            'section': 'song',
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.select('form#frm_defaultList table > tbody > tr')

        for tr in tr_list:
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            if tr.select_one('td:nth-of-type(3) a.fc_gray'):
                title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            else:
                title = tr.select_one('td:nth-of-type(3) > div > div > span').get_text(strip=True)

            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
                strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

            song_info_list.append({
                'song_id': song_id,
                'title': title,
                'artist': artist,
                'album': album,
            })
        context['song_info_list'] = song_info_list
    return render(request, 'song/song_search_from_melon.html', context)
