from slugify import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.views.generic import TemplateView, ListView, DetailView
from django.urls import reverse

from .models import Article, Category, Comment, Tag
from .forms import CommentForm
from .documents import ArticleDocument


class IndexView(TemplateView):
    template_name = 'news/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_articles'] = Article.objects.all().order_by(
            '-pub_date')[:3].prefetch_related('categories')
        return context


class BlogListView(ListView):
    template_name = 'news/blog.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().prefetch_related('categories')


class CategoryListView(ListView, SingleObjectMixin):
    template_name = 'news/blog.html'
    model = Article
    ordering = '-pub_date'
    paginate_by = 10
    slug_url_kwarg = 'cat_slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.object.article_set.all()\
            .prefetch_related('categories')
        return super().get_queryset()


@method_decorator(csrf_protect, name='dispatch')
class PageDetailView(FormMixin, DetailView):
    template_name = 'news/page.html'
    model = Article
    slug_url_kwarg = 'post_slug'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            prev_article = Article.objects.get(id=self.object.id - 1)
        except ObjectDoesNotExist:
            prev_article = None
        try:
            next_article = Article.objects.get(id=self.object.id + 1)
        except ObjectDoesNotExist:
            next_article = None
        context['prev_article'] = prev_article
        context['next_article'] = next_article
        context['comments'] = self.object.comments.filter(is_moderated=True)
        return context

    def get_success_url(self):
        return reverse('blog')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        data['article'] = self.object
        Comment.objects.create(**data)
        return super().form_valid(form)


class ContactView(TemplateView):
    template_name = 'news/contact.html'


class AboutView(TemplateView):
    template_name = 'news/about.html'


class SearchView(ListView):
    template_name = 'news/search.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.query_text = self.request.GET.get('q')
        try:
            Tag.objects.create(
                name=self.query_text,
                slug=slugify(self.query_text)
            )
        except Exception:
            pass
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return ArticleDocument.search().query(
            "match", content=self.query_text).to_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['query'] = self.query_text
        return context


class TagListView(ListView, SingleObjectMixin):
    template_name = 'news/tag.html'
    model = Tag
    ordering = '-pub_date'
    paginate_by = 3
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Tag.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = ArticleDocument.search().query(
            "match", content=self.object.name).to_queryset()
        return super().get_queryset()


class RobotsView(TemplateView):
    template_name = 'news/robots.txt'
    content_type = 'text/plain'
