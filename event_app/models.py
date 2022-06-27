from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.search import index
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


class EventIndexPage(Page):
    max_count = 1
    page_description = "Use this page to index all your events"
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
    subpage_types = ['event_app.EventPage']

    content_panels = Page.content_panels + [
        FieldPanel('lead_line'),
        ImageChooserPanel('image', heading='article hero'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(EventIndexPage, self).get_context(
            request, *args, **kwargs)
        all_events = EventPage.objects.live().public().order_by('date', 'start_time')
        paginator = Paginator(all_events, 2)
        page = request.GET.get("page")
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        context["events"] = events
        return context


class EventPage(Page):
    page_description = "Use this page to publish details about your event"
    description = RichTextField(features=[
        'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'blockquote'])
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    date = models.DateField('date')
    start_time = models.TimeField('start_time')
    end_time = models.TimeField('end_time', null=True, blank=True)
    venue = models.CharField('venue', max_length=80, null=True, blank=True)
    address = models.CharField(
        'address', max_length=250, null=True, blank=True)
    url_link = models.URLField('url link for e-events', null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('date'),
        index.SearchField('venue'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        ImageChooserPanel('hero_image', heading='article hero'),
        FieldPanel('date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('venue'),
        FieldPanel('address'),
        FieldPanel('url_link'),
    ]

    parent_page_types = ['event_app.EventIndexPage']
    subpage_types = []
