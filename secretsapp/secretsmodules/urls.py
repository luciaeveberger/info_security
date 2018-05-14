# howdy/urls.py
from django.conf.urls import url
from secretsmodules import views


app_name = 'secretsmodules'
urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^register/',views.RegisterForm.as_view(), name='register'),
    url(r'^details/(?P<id>\d{1,50})/$',views.DetailsView.as_view(), name = 'details')
]
