from django.contrib import admin
from .models import Project, ProjectImage, Volunteer, AboutPage, ContactInfo

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ['image', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'trees_planted', 'is_active']
    list_filter = ['year', 'is_active']
    search_fields = ['title']
    inlines = [ProjectImageInline]

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email']

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'address']