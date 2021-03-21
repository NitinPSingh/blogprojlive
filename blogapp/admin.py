from django.contrib import admin
from .models import Post,Comment
from django.contrib.auth.admin import UserAdmin
from .models import UserProfileInfo
# Register your models here.
class CommentInline(admin.TabularInline): # new
    model = Comment
class PostAdmin(admin.ModelAdmin): # new
    inlines = [
    CommentInline,
    ]
admin.site.register(Post,PostAdmin)
admin.site.register(UserProfileInfo)
admin.site.register(Comment)
