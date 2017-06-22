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

    # try find number of pages of anime to scrape
    try:
        n_pages = int(soup.find('div', class_ = 'pagination ac').span.nextSibling.get('href').split('=')[-1])
    except:
        n_pages = 1

    # collect anime from each page
    for i in range(1,n_pages+1):

        soup = BeautifulSoup(urllib.request.urlopen('https://myanimelist.net'+link+'?page='+str(i)).read(),'lxml')

        anime = soup.findAll('div', class_ = 'seasonal-anime js-seasonal-anime')
        for an in anime:

            # title of anime
            title = an.div.div.find('a',class_ = 'link-title').get('href').split("/")[-1]

            # don't collect any data if we've already taken it before
            if title in foundAnime:
                continue
            
            # collect all of the genres
            an_genres = []
            found = an.div.findAll('span', class_ = 'genre')

            for g in found:
                an_genres.append(g.a.get('title'))

            # convert to a string to be written
            an_genres = ';'.join(an_genres)

            # get synopsis
            synopsis = an.find('span', class_ = 'preline').getText()

            # final output string
            final_output = an_genres + "\n" + synopsis

            # write to file
            file = open("./" + genre + "/" + title + '.txt','w', encoding="utf-8")
            file.write(final_output)
            file.close()

            # add to hash table
            foundAnime[title] = 1

    return foundAnime



startScrape()

 