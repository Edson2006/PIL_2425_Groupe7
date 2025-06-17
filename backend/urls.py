from django.contrib import admin
from django.urls import path
from accounts.views import (  
    diag,
    index, 
    sign_in_out, 
    dashboard, 
    sign_out, 
    debug_users,
    edit_profile,
    create_offer,
    create_request,
    my_offers,
    my_requests,
    find_matches,
    conversations_list,
    conversation_detail,
    start_conversation,
    edit_offer,
    edit_request,
    switch_role,
    delete_offer,
    delete_request,
    all_offers,
    all_requests
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='home'), 
    path('connexion/', sign_in_out, name='sign_in_out'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deconnexion/', sign_out, name='sign_out'),
    path('debug-users/', debug_users, name='debug_users'),
    path('switch-role/<str:role>/', switch_role, name='switch_role'), 
    
    # Profil
    path('profil/modifier/', edit_profile, name='edit_profile'),
    
    # Offres et demandes
    path('offres/creer/', create_offer, name='create_offer'),
    path('demandes/creer/', create_request, name='create_request'),
    path('mes-offres/', my_offers, name='my_offers'),
    path('mes-demandes/', my_requests, name='my_requests'),
    path('matching/', find_matches, name='find_matches'),
    
    # Messagerie
    path('conversations/', conversations_list, name='conversations_list'),
    path('conversations/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('conversation/commencer/<int:user_id>/', start_conversation, name='start_conversation'),
    path('offres/modifier/<int:pk>/', edit_offer, name='edit_offer'),
    path('demandes/modifier/<int:pk>/', edit_request, name='edit_request'),
    path('offres/supprimer/<int:pk>/', delete_offer, name='delete_offer'),
    path('demandes/supprimer/<int:pk>/', delete_request, name='delete_request'),
    path('toutes-les-offres/', all_offers, name='all_offers'),
    path('toutes-les-demandes/', all_requests, name='all_requests'),
    path('diag/', diag, name='diag'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)