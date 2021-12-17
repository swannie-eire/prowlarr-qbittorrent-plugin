# VERSION: 1.0
# prowlarr.py
# AUTHORS: swannie-eire (https://github.com/swannie-eire)
# CONTRIBUTORS:
#               Diego de las Heras (ngosang@hotmail.es)
#               ukharley
#               hannsen (github.com/hannsen)

import json
import os
from urllib.parse import urlencode, unquote
from urllib import request as urllib_request
from http.cookiejar import CookieJar

from novaprinter import prettyPrinter
from helpers import download_file


###############################################################################
# load configuration from file
CONFIG_FILE = 'prowlarr.json'
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIG_FILE)
CONFIG_DATA = {
    'api_key': 'YOUR_API_KEY_HERE',  # prowlarr api
    'tracker_first': False,          # (False/True) add tracker name to beginning of search result
    'url': 'http://127.0.0.1:9696',  # prowlarr url
}


def load_configuration():
    global CONFIG_PATH, CONFIG_DATA
    try:
        # try to load user data from file
        with open(CONFIG_PATH) as f:
            CONFIG_DATA = json.load(f)
    except ValueError:
        # if file exists but it's malformed we load add a flag
        CONFIG_DATA['malformed'] = True
    except Exception:
        # if file doesn't exist, we create it
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps(CONFIG_DATA, indent=4, sort_keys=True))

    # do some checks
    if any(item not in CONFIG_DATA for item in ['api_key', 'tracker_first', 'url']):
        CONFIG_DATA['malformed'] = True


load_configuration()
###############################################################################


class prowlarr(object):
    name = 'prowlarr'
    url = CONFIG_DATA['url'] if CONFIG_DATA['url'][-1] != '/' else CONFIG_DATA['url'][:-1]
    api_key = CONFIG_DATA['api_key']
    supported_categories = {
        'all': None,
        'anime': 5070,
        'books': 8000,
        'games': "1000&categories=4000",
        'movies': 2000,
        'music': 3000,
        'software': 4000,
        'tv': 5000,
    }


    def download_torrent(self, download_url):
        # fix for some indexers with magnet link inside .torrent file
        if download_url.startswith('magnet:?'):
            print(download_url + " " + download_url)
        response = self.get_response(download_url)
        if response is not None and response.startswith('magnet:?'):
            print(response + " " + download_url)
        else:
            print(download_file(download_url))


    def search(self, what, cat='all'):
        what = unquote(what)
        category = self.supported_categories[cat.lower()]

        # check for malformed configuration
        if 'malformed' in CONFIG_DATA:
            self.handle_error("malformed configuration file", what)
            return

        # check api_key
        if self.api_key == "YOUR_API_KEY_HERE":
            self.handle_error("api key error", what)
            return

        if category is not None:
            prowlarr_url = self.url + "/api/v1/" + 'search?query=' + what.replace(' ', '+') + '&apikey=' + self.api_key + '&indexerIds=' + "-2" + "&categories=" + str(category)
        else:
            prowlarr_url = self.url + "/api/v1/" + 'search?query=' + what.replace(' ', '+') + '&apikey=' + self.api_key + '&indexerIds=' + "-2"

        response = self.get_response(prowlarr_url)
        if response is None:
            self.handle_error("connection error", what)
            return

        x = json.loads(response)

        # process search results
        for result in x:
            res = {}

            title = result.get('title')
            tracker = result.get('indexer')
            if CONFIG_DATA['tracker_first']:
                res['name'] = '[%s] %s' % (tracker, title)
            else:
                res['name'] = '%s [%s]' % (title, tracker)

            if 'downloadUrl' in result:
                res['link'] = str(result.get('downloadUrl'))
            elif 'magnetUrl' in result:
                res['link'] = str(result.get('magnetUrl'))
            else:
                res['link'] = "no link to downlaod"

            res['size'] = str(result.get('size'))
            res['seeds'] = result.get('seeders')
            res['seeds'] = -1 if res['seeds'] is None else res['seeds']
            res['leech'] = result.get('leechers')
            res['leech'] = -1 if res['leech'] is None else res['leech']
            res['desc_link'] = result.get('infoUrl')
            
            if res['desc_link'] is None:
                res['desc_link'] = str(result.get('guid'))
                res['desc_link'] = '' if res['desc_link'] is None else str(res['desc_link'])

            # note: engine_url can't be changed, torrent download stops working
            res['engine_url'] = self.url

            prettyPrinter(self.escape_pipe(res))


    def generate_xpath(self, tag):
        return './{http://torznab.com/schemas/2015/feed}attr[@name="%s"]' % tag

    # Safety measure until it's fixed in prettyPrinter
    def escape_pipe(self, dictionary):
        for key in dictionary.keys():
            if isinstance(dictionary[key], str):
                dictionary[key] = dictionary[key].replace('|', '%7C')
        return dictionary


    def get_response(self, query):
        response = None
        try:
            # we can't use helpers.retrieve_url because of redirects
            # we need the cookie processor to handle redirects
            opener = urllib_request.build_opener(urllib_request.HTTPCookieProcessor(CookieJar()))
            response = opener.open(query).read().decode('utf-8')
        except urllib_request.HTTPError as e:
            # if the page returns a magnet redirect, used in download_torrent
            if e.code == 302:
                response = e.url
        except Exception:
            pass
        return response


    def handle_error(self, error_msg, what):
        # we need to print the search text to be displayed in qBittorrent when
        # 'Torrent names only' is enabled
        prettyPrinter({
            'seeds': -1,
            'size': -1,
            'leech': -1,
            'engine_url': self.url,
            'link': self.url,
            'desc_link': 'https://github.com/test',  # noqa
            'name': "Prowlarr: %s! Right-click this row and select 'Open description page' to open help. Configuration file: '%s' Search: '%s'" % (error_msg, CONFIG_PATH, what)  # noqa
        })


if __name__ == "__main__":
    prowlarr_se = prowlarr()
    prowlarr_se.search("ubuntu")
