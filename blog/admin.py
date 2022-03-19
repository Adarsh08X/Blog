from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)