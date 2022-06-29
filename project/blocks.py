from django.db import models
from wagtail.blocks import (
    CharBlock,
    StructBlock,
    TextBlock,
    RegexBlock,
    ChoiceBlock,
    PageChooserBlock,
    EmailBlock,
    IntegerBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class QuoteBlock(StructBlock):
    text = TextBlock(required=True)
    author = CharBlock(required=False)

    class Meta:
        label = "Quote"
        icon = "openquote"
        template = "blocks/quote.html",


class ArticleImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = CharBlock(
        required=False,
        max_length=140,
        help_text="Caption under image, NOT an Alt text",
    )
    image_type = ChoiceBlock(choices=[
        ('normal', 'Normal'),
        ('full_width', 'Full width'),
        ('float_right', 'Float to right'),
    ], default='normal')

    class Meta:
        icon = "image"


class YouTubeBlock(StructBlock):
    headline = TextBlock(required=False)
    youtube_link = RegexBlock(regex=r'(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)', error_messages={
        'invalid': "Not a valid YouTube URL"
    })

    def get_context(self, value):
        context = super(YouTubeBlock, self).get_context(value)
        try:
            context["youtube_embed"] = context["self"]["youtube_link"].replace(
                "watch?v=", "embed/")
        except:
            pass
        return context

    class Meta:
        icon = "media"
        label = "YouTube embed"
        template = "blocks/youtube.html"


class DonationBlock(StructBlock):
    call_to_action = TextBlock(
        default="For the price of no more than a coffee a month, you can help us find, highlight, and end injustices at home and around the world.")

    class Meta:
        icon = "group"
        label = "Donation block"
        template = "blocks/donation.html"


class MenuItemBlock(StructBlock):
    name = CharBlock(required=True)
    page = PageChooserBlock()

    class Meta:
        label = "Menu item"


class ContactBlock(StructBlock):
    building_number_or_name = CharBlock(required=False)
    street = CharBlock(required=False)
    town = CharBlock(required=False)
    post_code = CharBlock(required=False)
    phone = IntegerBlock(required=False)
    email = EmailBlock(required=False)

    class Meta:
        template = "includes/contact/contact.html"
        label = "Contact Details"


class SocialMediaBlock(StructBlock):
    twitter = URLBlock(required=False, help_text='Your Twitter page URL')
    facebook = URLBlock(required=False, help_text='Your Facebook page URL')
    instagram = URLBlock(required=False, help_text='Your Instagram, page URL')
    linkedin = URLBlock(required=False, help_text='Your LinkedIn page URL')

    class Meta:
        template = "includes/social-media/social-media.html"
        label = "Social Media Links"
