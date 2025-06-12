from django.contrib import admin
from django.urls import path
# On importe les vues depuis la nouvelle application 'accounts'
from accounts import views 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # La page d'accueil pointe vers la vue 'index' dans 'accounts'
    path('', views.index, name='home'), 
    # La page de connexion/inscription pointe vers la vue 'sign_in_out' dans 'accounts'
    path('signin/', views.sign_in_out, name='sign_in_out'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
