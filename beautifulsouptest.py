from bs4 import BeautifulSoup
import requests


source = requests.get('https://coreyms.com/').text
soup = BeautifulSoup(source, 'lxml')

articles = soup.find_all('article')

for article in articles:
    headline = article.h2.a.text
    content = article.find('div', class_='entry-content')
    summary = content.p.text
    try:
        video_id = content.find('iframe', class_='youtube-player')['src'].split('/')[4].split('?')[0]
        video = 'https://www.youtube.com/watch?v='+video_id
    except:
        video = None
    print(headline)
    print(summary)
    print(video)
    print()
