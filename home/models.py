from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    PageChooserPanel,
    StreamFieldPanel
)


class HomePage(Page):
    max_count = 1
    lead_line = models.CharField(
        "Lead line",
        max_length=250,
    )
    body = RichTextField(
        features=[
            'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'hr'
        ],
        default=""
    )
    hero_link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.PROTECT,
        related_name='+',
        help_text="Landscape mode only; horizontal width between 1000px and 3000px."
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    subpage_types = [
        'news_app.NewsIndexPage',
        'blog_app.BlogIndexPage',
        'event_app.EventIndexPage',
        'event_app.EventPage',
        'about_app.AboutUsPage',
        'contact_app.ContactPage',
    ]

    content_panels = Page.content_panels + [
        FieldPanel('lead_line', classname="full"),
        FieldPanel('body'),
        PageChooserPanel('hero_link_page'),
        ImageChooserPanel('hero_image', heading='Home page hero'),
        ImageChooserPanel('image', heading='Home page image'),
    ]
