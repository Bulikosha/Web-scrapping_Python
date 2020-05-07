import requests
from bs4 import BeautifulSoup
import csv

# Plan:
# 1. Find the number of pages from olx.kz with certain options;
# 2. Make list of URL's
# 3. Parse

# https://www.olx.kz/elektronika/noutbuki-i-aksesuary/alma-ata/q-macbook/

def get_html(url):
	r = requests.get(url)
	return r.text


# function to determining the number of pages
def get_total_pages(html):
	soup = BeautifulSoup(html,'lxml')
	pages = soup.find('div', class_='pager rel clr').find_all('a', class_='block br3 brc8 large tdnone lheight24')[-1].get('href')
	total_pages = pages.split('=')[1]
	return int(total_pages)

def write_csv(data):
	#function to save result data to csv file
	with open('olx_lenovo.csv', 'a') as f:
		writer = csv.writer(f, delimiter=';', lineterminator='\n')

		writer.writerow((data['title'],
						  data['price'],
						  data['location'],
						  data['url']))

def get_page_data(html):
	soup = BeautifulSoup(html,'lxml')

	ads = soup.find('div', class_='rel listHandler').find_all('div', class_='offer-wrapper')
	for ad in ads:
		# title, price, location, url
		try:
			# title = ad.find('td', class_='title-cell').find_all('h3')
			title = ad.find('td', class_='title-cell').find('strong').text.encode("ascii", errors='ignore')
			# encode('ascii', errors='ignore') helped to avoid "UnicodeEncodeError" and finish parsing
			# .encode('utf-8') - did not help
		except:
			title = ""
		try:
			price = ad.find('td', class_='wwnormal tright td-price').find('p', class_='price').text.strip()
		except:
			price = ""
		try:
			location = ad.find('td', class_='bottom-cell').find('small').text.strip()
		except:
			location = ""
		try:
			url = ad.find('td', class_='title-cell').find('a').get('href')
		except:
			url = ""

		data = {'title': title,
				'price': price,
				'location': location,
				'url': url
				}

		write_csv(data)


def main():
	url = 'https://www.olx.kz/elektronika/noutbuki-i-aksesuary/alma-ata/q-macbook/'
	base_url = 'https://www.olx.kz/elektronika/noutbuki-i-aksesuary/alma-ata/q-'
	quiry_part = 'lenovo'
	page_part = '/?page='
	total_pages = get_total_pages(get_html(url))
	for i in range(1, (total_pages+1)):
		url_gen = base_url + quiry_part + page_part + str(i)
		# print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)

if __name__=='__main__':
	main()
