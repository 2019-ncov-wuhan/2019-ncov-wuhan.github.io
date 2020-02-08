from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json

response = requests.get('https://2019-ncov-wuhan.github.io/').text

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
		for word in item['keywords']:
			word_soup = BeautifulSoup("""<span class="small text-gray"></span>""", 'html.parser')
			word_soup.span.string = word
			item_soup.li.append(word_soup)
		for event in item['events']:
			event_soup = BeautifulSoup("""<p class="text-small mt-2 font-weight-light"></p>""", 'html.parser')
			event_soup.p.string = event['description']
			link_count = 1
			for link in event['links']:
				link_soup = BeautifulSoup("""<a href="">链接""" + str(link_count) + """</a>""", 'html.parser')
				link_soup.a['href']=link
				event_soup.p.append(link_soup)
			if ('img' in event):
				img_soup = BeautifulSoup("""<img src="" style="width:-webkit-fill-available"/>""", 'html.parser')
				img_soup.img['src']="https://2019-ncov-wuhan.github.io/imgs/"+event['img']
				event_soup.p.append(img_soup)
			hr_soup = BeautifulSoup("""<hr/>""", 'html.parser')
			item_soup.li.append(event_soup)
			item_soup.li.append(hr_soup)
		item_soup.find_all("hr")[-1].decompose()
		items_tag.insert(index, item_soup)
		index = index+1

with open('../index.html', 'w') as output:
	output.write(soup.prettify())