from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page, Orderable
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail import blocks
from wagtail.search import index
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
)

from modelcluster.fields import ParentalKey

from project.blocks import (
    QuoteBlock,
    YouTubeBlock,
    ArticleImageBlock,
)


class ArticleAuthorsOrderable(Orderable):
    """This allows us to select one or more article authors from Snippets."""

    page = ParentalKey("blog_app.BlogPage", related_name="article_authors")
    author = models.ForeignKey(
        "blog_app.ArticleAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        # Use a SnippetChooserPanel because article.ArticleAuthor is registered as a snippet
        SnippetChooserPanel("author"),
    ]


class BlogIndexPage(Page):
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

    parent_page_types = ['home.HomePage']
    subpage_types = ['blog_app.BlogPage', ]

    content_panels = Page.content_panels + [
        FieldPanel('lead_line'),
        ImageChooserPanel('image', heading='article hero'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(
            request, *args, **kwargs)
        all_articles = BlogPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_articles, 10)
        page = request.GET.get("page")
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context["articles"] = articles
        return context


class BlogPage(Page):
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
    ],
        use_json_field=True,
        block_counts={'paragraph': {'min_num': 1}}
    )
    search_fields = Page.search_fields + [
        index.SearchField('lead_line'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('lead_line'),
        ImageChooserPanel('hero_image', heading='Article hero image'),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [
                InlinePanel("article_authors", label="Author",
                            min_num=1, max_num=4)
            ],
            heading="Author(s)"
        ),
    ]

    parent_page_types = ['blog_app.BlogIndexPage']
    subpage_types = []


@register_snippet
class ArticleAuthor(models.Model):
    """Article author for snippets."""

    name = models.CharField(max_length=100)
    bio = RichTextField(features=['bold', 'italic', 'link'])
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("bio"),
                ImageChooserPanel("image"),
            ],
            heading="Name, bio and image",
        ),
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta:  # noqa
        verbose_name = "Article Author"
        verbose_name_plural = "Article Authors"
