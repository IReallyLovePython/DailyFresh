from django.conf.urls import url

from apps.cart import views

urlpatterns = [
    url(r'^$', views.CartView.as_view(), name='cart'),
    url(r'^add$', views.CartAddView.as_view(), name='add'),
    url(r'^update$', views.UpdateCartView.as_view(), name='update'),
    url(r'^delete$', views.CartDeleteView.as_view(), name='delete')
]
