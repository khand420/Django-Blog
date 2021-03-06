from django.contrib import admin
from .models import Contact

# Register your models here.
# admin.site.register(Contact)

@admin.register(Contact) #Decorate 
class PostAdmin(admin.ModelAdmin): #For changes in model db
    # list_display = ('title','slug','author','publish','status')
    # list_filter = ('status','created','publish','author')
    search_fields = ('name','content','email')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ('status','publish')
