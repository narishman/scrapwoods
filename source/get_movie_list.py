#! /usr/bin/python3

from bs4 import BeautifulSoup
import requests

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
        print(f'-E- page returned code: {page.status.code}  site: {site}')
    return page.content


#parse the movie list page to get a list of the movies and the link to the reviews
review_links = get_movie_review_links(website)
print(review_links)


