#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, random, re
from app.bot import bot
from bs4 import BeautifulSoup

class Youtube(object):
    def __init__(self, instance, conversation, query):
        self.instance = instance
        self.conversation = conversation
        self.youtube = {}
        self.build(query)

    def build(self, query):
        self.youtube = search_yt(query)

    def send_youtube(self):
        text = u"*" + self.youtube['title'] + "* \n*URL*: " + self.youtube['url']
        print self.youtube['image_url']
        bot.send_image(self.instance, self.conversation, self.youtube['image_url'], text)


def search_yt(string):

    query = re.sub('[\\\\/:+*?"`<>&!-.;#~$%|]', '', string).strip().replace(' ', '+')

    url = 'https://www.youtube.com/results?search_query=' + query
    print url

    req = requests.get(url)
    html = BeautifulSoup(req.text, "html.parser")

    results = html.find('div', {'id': 'results'})
    elements = results.find_all('div', {'class': 'yt-lockup'})

    el = elements[0]

    content = el.find('div', {'class': 'yt-lockup-content'})
    title = content.find('h3').find('a')['title']
    href = content.find('h3').find('a')['href']
    yt_url = "https://www.youtube.com" + href

    if "watch" not in href:
        thumbnail = el.find('div', {'class': 'yt-lockup-thumbnail'}).find('span', {'class': 'yt-thumb-simple'}).find('img')['src']
    else:
        id = href[9:]
        thumbnail = 'https://i.ytimg.com/vi/' + id + '/hqdefault.jpg'

    output = {
        'title': title,
        'url': yt_url,
        'image_url': thumbnail
    }

    return output