# coding=utf-8
from django.urls import path
from .views import *


urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/signup/', SignUp.as_view(), name='sign_up'),
    path('contact_mail/', contact_form, name='contact_form'),
    path('single_blog/<blog_slug>', BlogDetail.as_view(), name='blog_detail'),
    path('artistes', Artist.as_view(), name='artist'),
    path('artiste_detail/<member_id>', ArtistDetail.as_view(), name='artist_detail'),

]
