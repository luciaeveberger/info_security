# howdy/urls.py
from django.conf.urls import url
from secretsmodules import views


app_name = 'secretsmodules'
urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
<<<<<<< HEAD
    url(r'^register/',views.RegisterForm.as_view(), name='register'),
    url(r'^details/(?P<id>\d{1,50})/$',views.DetailsView.as_view(), name = 'details')
=======
    url(r'^add_to_cart/(?P<secret_id>[0-9]+)$', views.add_to_cart, name='add_to_cart'),
    url(r'^register/',views.RegisterForm.as_view(), name='register')
>>>>>>> be09e33f760c814f2b23a9390c612f71304de5d0
]
