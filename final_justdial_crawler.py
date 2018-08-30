from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import sys
import csv

link_list=[]
sturl = input('Please enter url name')
orig_stdout = sys.stdout
f = open('out2.html', 'w')
sys.stdout = f
sys.stdout = orig_stdout
f.close()
url=sturl
#print(sturl)
file_name=str(sturl.split('/')[3]+'_'+sturl.split('/')[4]+".csv")
#print(file_name)
out_file=open(file_name,"w")
writer=csv.writer(out_file)
writer.writerow(["type","name","streetAddress","addressLocality","postalCode","addressRegion","addressCountry","telephone1","telephone2"])

def generateLink():
	i=1
	req = Request(str(sturl).strip(), headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	parser = BeautifulSoup(webpage,'html.parser')
	soap=parser.find_all('li',{"class":"cntanr"})
	while bool(parser.find('li',{"class":"cntanr"}))==True:
		url=sturl+'/page-'+str(i)
		i=i+1
		print(url)
		req = Request(str(url).strip(), headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		parser = BeautifulSoup(webpage,'html.parser')
		#print(parser)
		soap=parser.find_all('li',{"class":"cntanr"})
		#print(soap)
		getLink(soap)


def getLink(soap):
	for s in soap:
		link_list.append(s["data-href"])
		#print(s["data-href"])

def getData():

	print(link_list)
	for link in link_list:
		#print('1'+link)
		req1 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
		webpage1 = urlopen(req1).read()
		parser = BeautifulSoup(webpage1,'html.parser')
		file_object=open('data.txt','w')
		file_object.write(str(parser))
		file_object.close()
		p=parser.find_all('script')
		data=p[1].text
		#print('2'+data)
		type=data.split('@type": "')[1].split('"')[0]
		#print(type)
		name=data.split('name": "')[1].split('"')[0]
		#print('3'+name)
		streetAddress=data.split('streetAddress": "')[1].split('"')[0]
		#print(streetAddress)
		addressLocality=data.split('addressLocality": "')[1].split('"')[0]
		#print(addressLocality)
		postalCode=data.split('postalCode": "')[1].split('"')[0]
		#print(postalCode)
		addressRegion=data.split('addressRegion": "')[1].split('"')[0]
		#print(addressRegion)
		addressCountry=data.split('addressCountry": "')[1].split('"')[0]
		#print(addressCountry)
		if data.count('telephone')!=0:
			telephone=data.split('telephone": ["')[1].split('"]')[0]
			print(telephone)
			c=telephone.count(',')
			if c==0:
				telephone1=telephone.split('"')[0]
				telephone2=''
			elif c>=1:
				telephone1=telephone.split('"')[0]
				telephone2=telephone.split('","')[1].split('"')[0]
		else:
			telephone1=''
			telephone2=''
		#print(telephone1)
		#print(telephone2)
		writer.writerow([type,name,streetAddress,addressLocality,postalCode,addressRegion,addressCountry,telephone1,telephone2])
		#writer.close()

generateLink()
#print(link_list)
getData()