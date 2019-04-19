##ImgScraper.py
import re
import sys
import os
import requests
import argparse
import urllib.request
from bs4 import BeautifulSoup

class ImgScraper:
    def __init__(self, keyword, outDir, number, verbose):
        self.keywords = keyword.split()
        self.outDir = outDir
        self.number = number
        self.verbose = True if verbose is True else False

    def scrapeImages(self):
        quote_page = 'https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj3sszTpNzhAhUFXK0KHUPNAJ8Q_AUIDygC&biw=1352&bih=675&num={}'.format('+'.join(self.keywords), str(self.number))
        if self.verbose:
            print("Grabbing images from %s" % quote_page)
        response = requests.get(quote_page)
        soup = BeautifulSoup(response.content, 'html.parser')
        thumbs = soup.findAll("img")
        if self.verbose:
            print("Found {} images".format(len(thumbs)))
        try:
            os.mkdir(self.outDir)
            if self.verbose:
                print('Created Directory: %s' % self.outDir)
        except FileExistsError:
            if self.verbose:
                print('Directory: %s already exists' % self.outDir)
        for i in range(len(thumbs)):
            if self.verbose:
                print('Saving image at:\t{}\nas:\t{}'.format(thumbs[i]['src'], '{}_{}_{}_.jpg'.format(self.outDir, '_'.join(self.keywords), str(i))))
            urllib.request.urlretrieve(thumbs[i]['src'],  '{}_{}_{}_.jpg'.format(self.outDir, '_'.join(self.keywords), str(i) ) )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', type=str, help="Keyword(s), separated by spaces")
    parser.add_argument('-o', type=str, help="folder to output image files. Default images/")
    parser.add_argument('-n', type=int, help="Number of images to scrape. Default 20")
    parser.add_argument('-v', action='store_true', help="Verbose")
    args = parser.parse_args()
    if args.k is None:
        print('Keyword must be provided')
        parser.print_help()
        sys.exit(1)
    if args.o is None:
        args.o = 'images/'
    if args.n is None:
        args.n = 20
    scraper = ImgScraper(args.k, args.o, args.n, args.v)
    scraper.scrapeImages()

if __name__ == '__main__':
    main()