from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from project.blocks import SocialMediaBlock, ContactBlock


class ContactPage(Page):
    max_count = 1
    lead_line = RichTextField()
    contact_details = StreamField(
        [
            ('contact', ContactBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('lead_line'),
        StreamFieldPanel('contact_details'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []
    template = 'contact_app/contact_page.html'
