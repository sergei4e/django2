import sys
from datetime import datetime

from slugify import slugify
from requests_html import HTMLSession
from django.utils.timezone import make_aware

from concurrent.futures import ThreadPoolExecutor

from news.models import Article, Author, Category


# BBC Author in db has id=3
author = Author.objects.get(id=3)


def crawl_one(url):

    try:

        with HTMLSession() as session:
            response = session.get(url)

        name = response.html.xpath('//div[@class="story-body"]/h1')[0].text
        content = response.html.xpath('//div[@class="story-body__inner"]/p')

        image_url = response.html.xpath('//div[@class="story-body__inner"]//img/@src')[0]
        pub_date = response.html.xpath(
            '//li[@class="mini-info-list__item"]/div/@data-datetime')[0]

        cats = response.html.xpath('//li[@class="tags-list__tags"]')

        my_content = ''
        short_description = ''
        for element in content:
            my_content += f'<{element.tag}>' + element.text + f'<{element.tag}>'
            if len(short_description) < 200:
                short_description += element.text + ' '

        image_name = slugify(name)
        img_type = image_url.split('.')[-1]

        img_path = f'images/{image_name}.{img_type}'

        with open(f'media/{img_path}', 'wb') as f:
            with HTMLSession() as session:
                response = session.get(image_url)
                f.write(response.content)

        pub_date = datetime.strptime(pub_date, '%d %B %Y')

        categories = []

        for cat in cats:
            categories.append(
                {
                    'name': cat.text.strip(),
                    'slug': slugify(cat.text)
                }
            )

        article = {
            'name': name,
            'slug': slugify(name),
            'content': my_content,
            'short_description': short_description.strip(),
            'main_image': img_path,
            'pub_date': make_aware(pub_date),
            'author': author
        }

        # article = Article(**article)
        # articles.append(article)

        article, created = Article.objects.get_or_create(**article)

        for category in categories:
            cat, created = Category.objects.get_or_create(**category)
            article.categories.add(cat)

        print(article)

    except Exception as e:
        print(f'[{url}]', e, type(e), sys.exc_info()[-1].tb_lineno)


def get_fresh_news():
    base_url = 'https://www.bbc.com/news/technology'

    with HTMLSession() as session:
        response = session.get(base_url)

    links = response.html.absolute_links

    fresh_news = []

    for link in links:
        try:
            if link.split('-')[-1].isdigit():
                fresh_news.append(link)
        except:
            pass

    return fresh_news


def run():
    # Article.objects.all().delete()
    fresh_news = get_fresh_news()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawl_one, fresh_news)
    # Article.objects.bulk_create(articles, ignore_conflicts=True)


if __name__ == '__main__':
    run()
