from django.db import models

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from project.blocks import (
    ArticleImageBlock,
    QuoteBlock,
    YouTubeBlock,
)


class AboutUsPage(Page):
    max_count = 1
    page_description = "Use this page to describe your organisation"

    body = StreamField([
        ('paragraph', blocks.RichTextBlock(features=[
            'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul'])),
        ('image', ArticleImageBlock()),
        ('quote', QuoteBlock()),
        ('youtube', YouTubeBlock()),
    ],
        use_json_field=True,
        block_counts={
        'paragraph': {'min_num': 1}
    }
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
