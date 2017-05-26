from django.conf.urls import url
from . import views


app_name = 'photo'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'), 
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<album_id>[0-9]+)/detail_change/$', views.detail_change, name='detail_change'),
    url(r'album/add/$', views.albumCreate, name='album-add'),
    url(r'album/(?P<album_id>[0-9]+)/$', views.convertImage, name='convert'),
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
    url(r'album/(?P<album_id>[0-9]+)/download/$', views.get_image, name='get_image'),

]