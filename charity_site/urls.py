from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_lang/', views.set_language, name='set_language'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('join/', views.join, name='join'),
    path('support/', views.support, name='support'),
    path('import-data/', views.import_data, name='import_data'),
    path('make-admin/', views.make_admin_now, name='make_admin'),
]

# ВАЖНО: Эта строка должна быть в конце файла!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
