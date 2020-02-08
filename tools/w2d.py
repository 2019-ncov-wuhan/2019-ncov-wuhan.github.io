from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json


data = {}
data['items'] = []

response = requests.get('https://2019-ncov-wuhan.github.io/').text

soup = BeautifulSoup(response, 'html.parser')

items = soup.find_all('li', class_="timeline-item")
for item in items:
	item_json = {}
	item_json['date'] = item.h2.get_text().strip()
	item_json['keywords'] = []
	item_json['events'] = []
	
	for event in item.find_all('p'):
		event_json = {}
		event_json['description'] = event.get_text().strip().replace('\n', '').replace(' ', '').replace('链接', '')
		link = event.find('a')
		event_json['links'] = []
		img = event.find('img')
		if link != None:
			event_json['links'].append(link['href'].strip())
		if img != None:
			event_json['img'] = img['src'].strip()
		item_json['events'].append(event_json)

	data['items'].append(item_json)

with open('../data/events.json', 'w') as output:
	json.dump(data, output, indent=4, ensure_ascii=False)
