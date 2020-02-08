from django.contrib.sitemaps import Sitemap
from .models import Article, Category, Tag


class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    limit = 5

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.pub_date


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    limit = 5

    def items(self):
        return Category.objects.all()


class TagSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    limit = 5

    def items(self):
        return Tag.objects.all()


sitemaps = {
    'articles': ArticleSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap
}
