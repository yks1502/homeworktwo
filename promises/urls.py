from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from promises import views

urlpatterns = [
  url(r'^promises/$', views.PromiseList.as_view()),
  url(r'^promises/(?P<pk>[0-9]+)/$', views.PromiseDetail.as_view()),
  url(r'^users/$', views.UserList.as_view()),
  url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
  url(r'^userall/$', views.UserAllList.as_view()),
  url(r'^userall/(?P<pk>[0-9]+)/$', views.UserAllDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
