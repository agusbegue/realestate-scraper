from django.contrib import admin

from .models import Post, ScrapyJob

admin.site.register(Post)
admin.site.register(ScrapyJob)
