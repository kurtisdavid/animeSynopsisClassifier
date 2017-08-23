import urllib.request
from bs4 import BeautifulSoup
import sys
import random

def scrape(link):

    # setup connections
    try:
      r = urllib.request.urlopen(link).read()
      soup = BeautifulSoup(r,'lxml')
    except:
      return None

    synopsis = soup.find('span', itemprop = 'description').getText().strip()

    sideBar = soup.find('div',class_ = 'js-scrollfix-bottom')
            
    info = {'Studios:': '', 'Rating:': ''}

    title = soup.find('span', itemprop = 'name').getText().strip()

    # side bar had no classes so have to go through the divs
    for div in sideBar.findAll('div'):
        
        try:
            
            span = div.span.getText()
            
                
            if span == 'Studios:':
                info[span] = div.a.getText()
                
            elif span == 'Rating:':
                info[span] = div.getText().strip()[10:]
                break
            
            elif span == 'Genres:':
                genres = []
                for l in div.findAll('a'):
                  genres.append(l.getText())

                an_genres = ';'.join(genres)

        except:

            if len(div.findAll('a')) != 0 and len(div.a.findAll('img')) == 1:

              img_link = div.a.img['src']

            continue

    final_output = an_genres + '\n' + title + '\nStudios: ' + info['Studios:'] + '\nRating: ' + info['Rating:'] + '\nSynopsis: ' + synopsis

    return title, clean(final_output), img_link

def clean(synopsis):

    lines = synopsis.split('\n')

    real = []
    lastLine = ''

    invalid = False

    genres = lines[0].split(';')
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

    return real, genres

def generate():

  general_link = "https://myanimelist.net/anime/season"
  r = urllib.request.urlopen(general_link).read()
  soup = BeautifulSoup(r,'lxml')

  seasonal_anime = soup.findAll('div', class_ = 'seasonal-anime js-seasonal-anime');
  chosen = random.choice(seasonal_anime)

  link = chosen.div.div.p.a.get('href')

  return link


