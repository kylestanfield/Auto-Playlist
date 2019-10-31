import configparser
import requests
from xml.etree import ElementTree

def getTopTracks(user, api_key, period):
    api_method = 'method=user.gettoptracks'

    last_fm_URL = 'http://ws.audioscrobbler.com/2.0/'
    API_CALL_URL = (last_fm_URL + '?' + api_method \
                     + '&user=' + user + '&period=' + period \
                    + '&api_key=' + api_key).encode('utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'From': 'stanfield@ucsb.edu'
    }
    api_response = requests.get(API_CALL_URL, headers=headers)

    tree = ElementTree.fromstring(api_response.content)

    track_list = []
    if tree.attrib['status'] == 'ok':
        for i in range(50):
            track_list.append((tree[0][i][0].text, tree[0][i][6][0].text))
    else:
        return -1
    return track_list

if __name__ == '__main__':
    parser = configparser.ConfigParser()
    parser.read('config.ini')
    last_fm_key = parser.get('API Keys', 'last_fm')

    print(getTopTracks('sonfon', last_fm_key, '7day'))

    
