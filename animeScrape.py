import urllib.request
from bs4 import BeautifulSoup
import os
import sys

def startScrape():

    # setup connections
    r = urllib.request.urlopen('https://myanimelist.net/anime.php').read()
    soup = BeautifulSoup(r,'lxml')

    # first type of genre-link is what we want, so soup.find() works fine
    genre_columns = soup.find('div', class_ = 'genre-link').children


    genre_links = []

    # go through genre tree and collect genres
    for col in genre_columns:
        for child in col.children:
            genre_links.append(child.a.get('href'))

    # hashtable to keep track of which anime already saved
    foundAnime = {}
    # start scraping!
    for link in genre_links:

        foundAnime = genreCollect(link,foundAnime)



def genreCollect(link, foundAnime):

    genre = link.split('/')[-1]
    print(genre)

    soup = BeautifulSoup(urllib.request.urlopen('https://myanimelist.net'+link).read(),'lxml')

    # setup directory
    directory = './' + genre
    if not os.path.exists('./' + genre):
        os.makedirs(directory)

    # find number of pages of anime to scrape
    n_pages = int(soup.find('div', class_ = 'pagination ac').span.nextSibling.get('href').split('=')[-1])

    for i in range(1,n_pages+1):

        soup = BeautifulSoup(urllib.request.urlopen('https://myanimelist.net'+link+'?page='+str(i)).read(),'lxml')

        anime = soup.findAll('div', class_ = 'seasonal-anime js-seasonal-anime')
        for an in anime:

            title = an.div.div.find('a',class_ = 'link-title').get('href').split("/")[-1]

            if title in foundAnime:

                continue
            
            an_genres = []
            found = an.div.findAll('span', class_ = 'genre')

            for g in found:
                an_genres.append(g.a.get('title'))

            an_genres = ';'.join(an_genres)

            # get synopsis and get rid of unneeded part of summary **Make sure to credit MAL Rewrite**
            synopsis = an.find('span', class_ = 'preline').getText()
            synopsis = synopsis.replace('\n[Written by MAL Rewrite]', '')

            final_output = an_genres + "\n" + synopsis

            file = open("./" + genre + "/" + title + '.txt','w', encoding="utf-8")
            file.write(final_output)
            file.close()

            foundAnime[title] = 1

    return foundAnime



startScrape()

 