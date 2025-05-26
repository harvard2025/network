from django.contrib import admin

# Register your models here.
from .models import Post, User, Follow, Like

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)

admin.site.site_header = 'PrroCoders'


