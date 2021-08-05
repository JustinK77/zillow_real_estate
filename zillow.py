from lxml import html
import requests
import unicodecsv as csv
import argparse
from bs4 import BeautifulSoup

def parse(zipcode,filter=None):

	if filter=="newest":
		url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(zipcode)
	elif filter == "cheapest":
		url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort/".format(zipcode)
	else:
		url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)
	
	for i in range(5):
		# try:
		headers= {
					'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
					'accept-encoding':'gzip, deflate, sdch, br',
					'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
					'cache-control':'max-age=0',
					'upgrade-insecure-requests':'1',
					'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		}
		response = requests.get(url,headers=headers)
		print(response.status_code)
		soup = BeautifulSoup(response.content, "html.parser")
		fullWrapper = soup.find(id="wrapper")
		file = open("mylog.log", "w", encoding='utf-8')
		file.write(fullWrapper.prettify())
		prices = fullWrapper.find_all("div", class_="list-card-price")
		addresses = fullWrapper.find_all("address", class_="list-card-addr")
		statuses = fullWrapper.find_all("li", class_="list-card-statusText")
		print(prices, addresses, statuses)
		#//*[@id="zpid_122588394"]/div[1]/div[2]/div
		#print(prices)
		properties_list = []
		for i in range(0, len(addresses)):
			property = {
				'price': prices[i].text,
				'address': addresses[i].text,
				'status': statuses[i].text[2:]
			}
			print(property)
			properties_list.append(property)
		return properties_list
		# search_results = parserTree.xpath("//div[@id='search-results']//article")
		# print(search_results)
		# properties_list = []
		
		# for properties in search_results:
		# 	raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
		# 	raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
		# 	raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
		# 	raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
		# 	raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
		# 	#//*[@id="zpid_122588394"]/div[1]/div[2]/div
		# 	raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
		# 	raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
		# 	url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
		# 	raw_title = properties.xpath(".//h4//text()")
			
		# 	address = ' '.join(' '.join(raw_address).split()) if raw_address else None
		# 	city = ''.join(raw_city).strip() if raw_city else None
		# 	state = ''.join(raw_state).strip() if raw_state else None
		# 	postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
		# 	price = ''.join(raw_price).strip() if raw_price else None
		# 	info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
		# 	broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
		# 	title = ''.join(raw_title) if raw_title else None
		# 	property_url = "https://www.zillow.com"+url[0] if url else None 
		# 	is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
		# 	properties = {
		# 					'address':address,
		# 					'city':city,
		# 					'state':state,
		# 					'postal_code':postal_code,
		# 					'price':price,
		# 					'facts and features':info,
		# 					'real estate provider':broker,
		# 					'url':property_url,
		# 					'title':title
		# 	}
		# 	if is_forsale:
		# 		properties_list.append(properties)
				# except:
		# 	print ("Failed to process the page",url)

if __name__=="__main__":
	argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	argparser.add_argument('zipcode',help = '')
	sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """
	argparser.add_argument('sort',nargs='?',help = sortorder_help,default ='Homes For You')
	args = argparser.parse_args()
	zipcode = args.zipcode
	sort = args.sort
	print ("Fetching data for %s"%(zipcode))
	scraped_data = parse(zipcode,sort)
	print(scraped_data)
	print ("Writing data to output file")
	with open("properties-%s.csv"%(zipcode),'wb')as csvfile:
		fieldnames = ['price', 'address', 'status']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for row in  scraped_data:
			writer.writerow(row)

