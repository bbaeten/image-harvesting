##ImgScraper.py
import requests
import urllib.request
from bs4 import BeautifulSoup




def main():
    quote_page = 'https://www.google.com/search?q=paintball+mask&safe=off&rlz=1C1GCEU_enUS825US825&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjAtJrEsMbhAhUJWa0KHchADhUQ_AUIDygC&biw=1918&bih=886'
    response = requests.get(quote_page)

    soup = BeautifulSoup(response.content, 'html.parser')
    thumbs = soup.findAll("img")

    for i in range(len(thumbs)):

        print(thumbs[i]['src'])
        urllib.request.urlretrieve(thumbs[i]['src'], str(i) + "_.jpg")

if __name__ == '__main__':
    main()