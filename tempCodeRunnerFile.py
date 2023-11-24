import nltk
import urllib
import bs4 as bs

source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Taj_Mahal').read()

soup = bs.BeautifulSoup(source, 'lxml')

text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text

print(text)