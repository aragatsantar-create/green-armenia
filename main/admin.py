from django.contrib import admin
from .models import Project, ProjectImage, Volunteer, AboutPage, ContactInfo, JoinPage

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

# === РЕГИСТРАЦИЯ НОВОЙ МОДЕЛИ С УДОБНЫМИ ГРУППАМИ ===
@admin.register(JoinPage)
class JoinPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🇷🇺 Русский язык', {
            'fields': ('title_ru', 'subtitle_ru', 'text_1_ru', 'text_2_ru', 'text_3_ru', 'text_4_ru', 'text_5_ru'),
        }),
        ('🇬🇧 English', {
            'fields': ('title_en', 'subtitle_en', 'text_1_en', 'text_2_en', 'text_3_en', 'text_4_en', 'text_5_en'),
        }),
        ('🇦🇲 Հայերեն (Армянский)', {
            'fields': ('title_hy', 'subtitle_hy', 'text_1_hy', 'text_2_hy', 'text_3_hy', 'text_4_hy', 'text_5_hy'),
        }),
    )