from django.contrib import admin
from dponisetting.dponiwiki.models import Island, IslandComponent, StaticPage


class IslandAdmin(admin.ModelAdmin):
	list_display = ('name', 'summary', 'created', 'modified', 'iscanonical')
	search_fields = ('name', 'summary')
	list_filter = ('owner', 'created', 'iscanonical')
	prepopulated_fields = {'slug': ('name',)}

class IslandComponentAdmin(admin.ModelAdmin):
	list_display = ('name', 'created', 'modified', 'owner', 'host_islands_list')
	search_fields = ('name', 'content')
	list_filter = ('created',)
	prepopulated_fields = {'slug': ('name',)}
	
class StaticPageAdmin(admin.ModelAdmin):
	list_display = ('name', 'created', 'modified', 'owner')
	search_fields = ('name',)
	list_filter = ('name', 'created')
	prepopulated_fields = {'slug': ('name',)}

	
admin.site.register(Island, IslandAdmin)
admin.site.register(IslandComponent, IslandComponentAdmin)
admin.site.register(StaticPage, StaticPageAdmin)