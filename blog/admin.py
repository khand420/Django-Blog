from django.contrib import admin
from blog.models import Post, BlogComment

admin.site.register((BlogComment))
    # list_display = ('name','email','post','created','active')
    # list_filter = ('active', 'created', 'updated')
    # search_fields = ('name', 'email', 'content')

@admin.register(Post) #Decorate 
class PostAdmin(admin.ModelAdmin): #For changes in model db
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status','publish')

    class Media:
        js= ('js/tinyInject.js',)


   

# @admin.register(BlogComment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name','email','post','created','active')
#     list_filter = ('active', 'created', 'updated')
#     search_fields = ('name', 'email', 'body')