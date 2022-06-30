from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', blank=True, null=True)
    instagram = models.URLField(
        help_text='Your Instagram URL', blank=True, null=True)
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL', blank=True, null=True)
    twitter = models.URLField(
        help_text='Your Twitter channel or user account URL', blank=True, null=True)
    linkedin = models.URLField(
        help_text='Your LinkedIn channel or user account URL', blank=True, null=True)
    tiktok = models.URLField(
        help_text='Your Tik Tok channel or user account URL', blank=True, null=True)

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('youtube'),
            FieldPanel('twitter'),
            FieldPanel('linkedin'),
            FieldPanel('tiktok'),
        ], heading="Multimedia Settings",)
    ]
