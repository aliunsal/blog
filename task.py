from celery import task
from PIL import Image, ImageOps
from django.core.mail import EmailMessage


@task(name='image_resize')
def resize_image(image_file, x, y):
    size = (x, y)
    image = Image.open(image_file)
    thumb = ImageOps.fit(image, size, Image.ANTIALIAS)
    thumb.save(image_file)


@task(name="mail_send")
def mail_send(subject, html_content, from_email, to):
    msg = EmailMessage(subject, html_content, from_email, to)
    msg.content_subtype = "html"
    msg.send()