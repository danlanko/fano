# coding=utf-8
from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('dashboard', login_redirect, name='dashboard'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('member_list', MemberList.as_view(), name='member_list'),
    path('block_member/<user_id>', deactivate_member, name='deactivate_member'),
    path('unblock_member/<user_id>', activate_member, name='activate_member'),
    path('delete_member/<user_id>', delete_member, name='delete_member'),
    path('new_song', NewSong.as_view(), name='new_song'),
    path('update_song/<song_id>', UpdateSongs.as_view(), name='update_song'),
    path('song_list', SongList.as_view(), name='song_list'),
    path('delete_song/<song_id>', delete_song, name='delete_song'),
    path('member_profile/<member_id>/<user_id>', MemberProfile.as_view(), name='member_profile'),
    path('update_profile/<member_id>/<user_id>', UpdateProfile.as_view(), name='update_profile'),
    path('new_blog', BlogView.as_view(), name='new_blog'),
    path('blog_list', BlogList.as_view(), name='blog_list'),
    path('update_blog/<slug>', BlogUpdate.as_view(), name='update_blog'),
    path('delete_blog/<blog_id>', delete_blog, name='delete_blog'),
    path('embed_new_video', EmbedVideo.as_view(), name='embed_video'),
    path('video_list', VideoList.as_view(), name='video_list'),
    path('delete_video/<video_id>', delete_video, name='delete_video'),
    path('proceed_payment<user_id>', proceed_payment, name='proceed_payment'),

]
