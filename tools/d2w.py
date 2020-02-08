from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json

response = requests.get('https://2019-n-cov.github.io/').text

soup = BeautifulSoup(response, 'html.parser')

items_tag = soup.find('ul', class_="timeline")
items_tag.clear()

with open('../data/events.json', 'r') as input:
	data = json.load(input)
	index = 0
	for item in data['items']:
		item_soup = BeautifulSoup("""<li class="timeline-item bg-white rounded ml-3 p-4 shadow"><div class="timeline-arrow"></div><h2 class="h5 mb-0"></h2></li>""", 'html.parser')
		date_tag = item_soup.find("h2")
		date_tag.string = item['date']
		for event in item['events']:
			event_soup = BeautifulSoup("""<p class="text-small mt-2 font-weight-light"></p>""", 'html.parser')
			event_soup.p.string = event['description']
			# link_ = event['link']
			if ('link' in event):
				link_soup = BeautifulSoup("""<a href="">链接</a>""", 'html.parser')
				link_soup.a['href']=event['link']
				event_soup.p.append(link_soup)
			item_soup.li.append(event_soup)

		items_tag.insert(index, item_soup)
		index = index+1

with open('../index.html', 'w') as output:
	output.write(soup.prettify())