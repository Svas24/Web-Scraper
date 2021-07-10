import os
import string
import requests
from bs4 import BeautifulSoup

site = 'https://www.nature.com'
trans = {ord(c): "" for c in string.punctuation}
trans[ord(' ')] = '_'

num_of_pages = int(input())
type_filter = input().strip()

for folder_number in range(1, num_of_pages + 1):
    folder_name = 'Page_' + str(folder_number)
    os.mkdir(folder_name)
    req_param = {'searchType': 'journalSearch', 'sort': 'PubDate', 'page': str(folder_number)}
    req = requests.get(site + '/nature/articles', req_param)
    articles = BeautifulSoup(req.text, 'html.parser').findAll('article')
    for article in articles:
        if article.find('span', {'data-test': 'article.type'}).text.strip() == type_filter:
            article_url = site + article.find('a', {'data-track-action': 'view article'})['href']
            article_soup = BeautifulSoup(requests.get(article_url).text, 'html.parser')
            article_body = article_soup.find('div', {'class': 'c-article-body'})
            if not article_body:
                article_body = article_soup.find('div', {'class': 'article-item__body'})
            article_file_path = os.path.join(folder_name, article.h3.text.strip().translate(trans) + ".txt")
            article_file = open(article_file_path, 'wb')
            article_file.write(article_body.text.strip().encode('utf-8'))
            article_file.close()
