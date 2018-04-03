from django.conf.urls import url
from apps.orders import views

urlpatterns = [
    url(r'^place$', views.PlaceOrdereView.as_view(), name='place'),
    url(r'^commit$', views.CommitOrdereView.as_view(), name='commit'),

]