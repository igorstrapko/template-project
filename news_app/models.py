from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from project.blocks import (
    QuoteBlock,
    YouTubeBlock,
    ArticleImageBlock,
)


class NewsIndexPage(Page):
    max_count = 1

    lead_line = models.CharField("Lead line", max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    def get_context(self, request, *args, **kwargs):
        context = super(NewsIndexPage, self).get_context(
            request, *args, **kwargs)
        news_index = NewsIndexPage.objects.first()
        all_news_pages = NewsPage.objects.child_of(
            news_index).live().public().order_by('-date')
        paginator = Paginator(all_news_pages, 10)
        page = request.GET.get("page")
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles
        return context

    content_panels = Page.content_panels + [
        FieldPanel('lead_line'),
        ImageChooserPanel('image', heading='Article hero image'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['news_app.NewsPage']


class NewsPage(Page):
    date = models.DateField()
    lead_line = models.CharField(max_length=250)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=[
         'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul'])),
        ('image', ArticleImageBlock()),
        ('quote', QuoteBlock()),
        ('youtube', YouTubeBlock()),
    ], use_json_field=True, block_counts={'paragraph': {'min_num': 1}})

    search_fields = Page.search_fields + [
        index.SearchField('lead_line'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('lead_line'),
        ImageChooserPanel('hero_image', heading='Article hero image'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['news_app.NewsIndexPage']
    subpage_types = []
