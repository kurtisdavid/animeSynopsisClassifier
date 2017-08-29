import urllib.request
from bs4 import BeautifulSoup
import os
import sys
import glob
import bson

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
    
    # current = glob.glob('../animeScrape/*/*.txt')
    # for x in current:
    #     foundAnime[x.split('\\')[-1][:-4]] = 1
    # start scraping!
    for link in genre_links:

        #foundAnime = genreCollect(link,foundAnime)
        foundAnime = mongoCollect(link,foundAnime)

def clean(synopsis):

    lines = synopsis.split('\n')

    real = []
    lastLine = ''

    invalid = False

    # don't include genres in synopsis
    for line in lines[1:]:

        if line.strip() == '':

          continue

        if 'No synopsis yet' in line:

          invalid = True
          break

        real.append(line)
        lastLine = line

    if invalid:

      return None

    if lastLine != '' and lastLine[0] in {'(':0, '[':0} and lastLine[-1] in {')':0,']':0}:

      real = '\n'.join(real[:-1])

    else:

      real = '\n'.join(real)

    return real

def mongoCollect(link, foundAnime):

    genre = link.split('/')[-1]

    soup = BeautifulSoup(urllib.request.urlopen('https://myanimelist.net'+link).read(),'lxml')
    # setup directory
    directory = '../mongoScrape/' + genre
    if not os.path.exists(directory):
        os.makedirs(directory)

    # try find number of pages of anime to scrape
    try:
        n_pages = int(soup.find('div', class_ = 'pagination ac').span.nextSibling.get('href').split('=')[-1])
    except:
        n_pages = 1

    # collect anime from each page
    for i in range(1,n_pages+1):
        
        pg = 'https://myanimelist.net'+link+'?page='+str(i)
        print(pg)
        soup = BeautifulSoup(urllib.request.urlopen(pg).read(),'lxml')
        

        anime = soup.findAll('div', class_ =lambda value: value and value.startswith('seasonal-anime js-seasonal-anime'))

        for an in anime:
            
            # get main link
            anime_link = an.div.div.find('a',class_ = 'link-title').get('href')
            
            # title of anime
            title = anime_link.split("/")[-1]

            # don't collect any data if we've already taken it before
            if title in foundAnime:
                continue
            
            # collect all of the genres
            an_genres = []
            found = an.div.findAll('span', class_ = 'genre')

            for g in found:
                an_genres.append(g.a.get('title'))

            genre_list = an_genres
            # convert to a string to be written
            an_genres = ';'.join(an_genres)


            # get synopsis
            synopsis = an.find('span', class_ = 'preline').getText().strip()
            
            try: 
                moreSoup = BeautifulSoup(urllib.request.urlopen(anime_link.encode('utf-8').decode('ascii', 'ignore')).read(),'lxml')
            except:
                err = open('./errors.txt','a+')
                err.write(anime_link + '\n')
                print(anime_link)
                continue
            
            sideBar = moreSoup.find('div',class_ = 'js-scrollfix-bottom')
            
            info = {'Studios:': '', 'Rating:': ''}
            
            # side bar had no classes so have to go through the divs
            for div in sideBar.findAll('div'):
                
                try:
                    
                    span = div.span.getText()
                        
                    if span == 'Studios:':
                        
                        info[span] = div.a.getText()
                        
                    elif span == 'Rating:':
                        
                        info[span] = div.getText().strip()[10:]
                        break
                        
                except:
                    
                    if len(div.findAll('a')) != 0 and len(div.a.findAll('img')) == 1:

                        img_link = div.a.img['src']

                    continue
    
            
            

            # final output string
            final_output = an_genres + '\n' + title + '\nStudios: ' + info['Studios:'] + '\nRating: ' + info['Rating:'] + '\nSynopsis: ' + synopsis  

            result = clean(final_output)

            entry = {'title': title, 'synopsis': result, 'genres': genre_list, 'image-link': img_link}
            
            encoded = bson.BSON.encode(entry)

            # write to file
            try:
                file = open(directory + '/' + title + '.bson','wb')
                file.write(encoded)
            except:
                err = open('./errors.txt','a+')
                err.write(anime_link + '\n')
                print(anime_link)
                continue
            # add to hash table
            foundAnime[title] = 1

    return foundAnime


def genreCollect(link, foundAnime):

    genre = link.split('/')[-1]

    soup = BeautifulSoup(urllib.request.urlopen('https://myanimelist.net'+link).read(),'lxml')
    # setup directory
    directory = '../animeScrape/' + genre
    if not os.path.exists(directory):
        os.makedirs(directory)

    # try find number of pages of anime to scrape
    try:
        n_pages = int(soup.find('div', class_ = 'pagination ac').span.nextSibling.get('href').split('=')[-1])
    except:
        n_pages = 1

    # collect anime from each page
    for i in range(1,n_pages+1):
        
        pg = 'https://myanimelist.net'+link+'?page='+str(i)
        print(pg)
        soup = BeautifulSoup(urllib.request.urlopen(pg).read(),'lxml')
        

        anime = soup.findAll('div', class_ =lambda value: value and value.startswith('seasonal-anime js-seasonal-anime'))

        for an in anime:
            
            # get main link
            anime_link = an.div.div.find('a',class_ = 'link-title').get('href')
            
            # title of anime
            title = anime_link.split("/")[-1]

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
            synopsis = an.find('span', class_ = 'preline').getText().strip()
            
            try: 
                moreSoup = BeautifulSoup(urllib.request.urlopen(anime_link.encode('utf-8').decode('ascii', 'ignore')).read(),'lxml')
            except:
                print(anime_link)
                continue
            
            sideBar = moreSoup.find('div',class_ = 'js-scrollfix-bottom')
            
            info = {'Studios:': '', 'Rating:': ''}
            
            # side bar had no classes so have to go through the divs
            for div in sideBar.findAll('div'):
                
                try:
                    
                    span = div.span.getText()
                        
                    if span == 'Studios:':
                        
                        info[span] = div.a.getText()
                        
                    elif span == 'Rating:':
                        
                        info[span] = div.getText().strip()[10:]
                        break
                        
                except:
                    
                    continue
            
            
            

            # final output string
            final_output = an_genres + '\n' + title + '\nStudios: ' + info['Studios:'] + '\nRating: ' + info['Rating:'] + '\nSynopsis: ' + synopsis  

            # write to file
            try:
                file = open(directory + '/' + title + '.txt','w', encoding="utf-8")
                file.write(final_output)
                file.close()
            except:
            	continue
            # add to hash table
            foundAnime[title] = 1

    return foundAnime



startScrape()

 