#! /usr/bin/python3

from bs4 import BeautifulSoup
import requests
import re
import os.path
import pprint

website = 'https://www.behindwoods.com/tamil-movies/tamil-movie-reviews-a-to-z.html'
review_links = dict()

def get_movie_review_links(site):
    content = get_page(site)
    soup = BeautifulSoup(content, 'html.parser')
    a = soup.find_all('a', class_='font_17')
    for tag in a:
        movie_name = tag.string.replace('MOVIE REVIEW', '').strip().lower()
        #print(f"{movie_name}\t{tag.get('href')}")
        review_links[movie_name] = tag.get('href')
    return review_links

def get_page(site):
    page = requests.get(site)
    if page.status_code != 200 :
        print(f'-E- page not found  site: {site}')
        return None
    return page.content

def parse_review(link):
    review = get_page(link)
    if review:
        soup = BeautifulSoup(review, 'html.parser')
        rating = soup.find(itemprop='ratingValue')
        #rating = soup.find(re.compile('span.*ratingValue'))
        #print(rating)
        if rating:
            return rating.string

        rating = soup.find(property='ratingValue')
        if rating:
            return rating.string


        rating = soup.find(src = re.compile('.*star.*?.gif'))
        if rating:
            gif = os.path.basename(rating.get('src'))
            m = re.search('star\-(.*).gif', gif)
            if m:
                return m.group(1)
    return None



#    rating = soup.find_all('span')
#    rating_value = None
#    for tag in rating:
#        if tag.get('itemprop') == 'ratingValue':
#            rating_value = tag.string 
#            return rating_value
#    #print(f'rating : {rating_value}')
#    rating = soup.find_all('img')
#
#    return rating_value



def get_reviews(review_links):
    #pprint.pprint(review_links)
    for movie, link in review_links.items():
        #print(movie)
        rating_value = parse_review(link)
        print(f'"{movie}",\t"{rating_value}"')
        #break
        

#parse the movie list page to get a list of the movies and the link to the reviews
review_links = get_movie_review_links(website)
#print(review_links)

#iterate through the movie review list and get the ratings of each movie
get_reviews(review_links)
