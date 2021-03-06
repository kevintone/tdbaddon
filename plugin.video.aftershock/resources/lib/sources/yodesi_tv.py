# -*- coding: utf-8 -*-

'''
    Aftershock Add-on
    Copyright (C) 2015 IDev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse, datetime

from resources.lib.libraries import client
from resources.lib import resolvers
from resources.lib.libraries import logger

class source:
    def __init__(self):
        self.base_link_1 = 'http://www.yodesi.net'
        self.base_link_2 = 'http://www.yodesi.net'
        self.base_link_3 = 'http://www.yodesi.net'

        self.search_link = '/feed/?s=%s&submit=Search'
        self.info_link = ''
        self.now = datetime.datetime.now()

        self.list = []

    def get_shows(self, name, url):
        try :
            return
        except:
            return

    def get_show(self, tvshowurl, imdb, tvdb, tvshowtitle, year):
        if tvshowurl:
            return tvshowtitle

    def get_episodes(self, title, url):
        try :
            return
        except:
            return

    def get_episode(self, url, ep_url, imdb, tvdb, title, date, season, episode):
        query = '%s %s' % (imdb, title)
        query = self.search_link % (urllib.quote_plus(query))
        ep_url = query
        if ep_url :
            return ep_url

    def get_sources(self, url):
        try:
            logger.debug('%s SOURCES URL %s' % (self.__class__, url))
            quality = ''
            sources = []

            result = ''

            links = [self.base_link_1, self.base_link_2, self.base_link_3]
            for base_link in links:
                try: result = client.source(base_link + '/' + url)
                except: result = ''
                if 'item' in result: break

            result = result.decode('iso-8859-1').encode('utf-8')

            result = result.replace('\n','')

            items = client.parseDOM(result, 'content:encoded')[0]

            items = re.compile('class=\"single-heading\">(.+?)<span').findall(items)

            for i in range(0, len(items)):
                try :
                    if '720p' in items[i]:
                        quality = 'HD'
                    else:
                        quality = 'SD'
                    urls = client.parseDOM(items[i], "a", ret="href")
                    for j in range(0,len(urls)):
                        result = client.source(urls[j])
                        item = client.parseDOM(result, name="div", attrs={"style":"float:none;height:700px;margin-left:200px"})[0]
                        rUrl = re.compile('(SRC|src|data-config)=[\'|\"](.+?)[\'|\"]').findall(item)[0][1]
                        urls[j] = rUrl
                    host = client.host(urls[0])
                    url = "##".join(urls)
                    sources.append({'source':host, 'parts': str(len(urls)), 'quality':quality,'provider':'YoDesi','url':url, 'direct':False})
                    urls = []
                except:
                    pass
            logger.debug('%s SOURCES [%s]' % (__name__,sources))
            return sources
        except:
            return sources

    def resolve(self, url, resolverList):
        try:
            logger.debug('%s ORIGINAL URL [%s]' % (__name__, url))
            tUrl = url.split('##')
            if len(tUrl) > 0:
                url = tUrl
            else :
                url = urlparse.urlparse(url).path

            links = []
            for item in url:
                r = resolvers.request(item, resolverList)
                if not r :
                    raise Exception()
                links.append(r)
            url = links
            logger.debug('%s RESOLVED URL [%s]' % (__name__, url))
            return url
        except:
            return False