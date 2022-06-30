from django.db import models
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel
)
from modelcluster.models import ClusterableModel

from project.blocks import MenuItemBlock


@register_snippet
class Menu(index.Indexed, ClusterableModel):
    """The main menu clusterable model."""
    title = models.CharField(max_length=12, unique=True, primary_key=True)

    menu = StreamField(
        [
            ("menu_items", MenuItemBlock()),
        ],
        default={}
    )

    featured = models.BooleanField(default=False)

    panels = [
        FieldPanel('title'),
        StreamFieldPanel('menu'),
        FieldPanel('featured'),
    ]

    def __str__(self):
        return self.title
