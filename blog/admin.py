from django.contrib import admin
from blog.models import Blog,Comment,Category,Profile

# Register your models here.

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Profile)
