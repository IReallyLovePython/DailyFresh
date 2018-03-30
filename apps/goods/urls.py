from django.conf.urls import url

from apps.goods import views

urlpatterns = [
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    # (?P<sku_id>\d+)会自动传入相应的view中
    url(r'^detail/(?P<sku_id>\d+)', views.DetailView.as_view(), name='detail'),

    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)$',
        views.ListView.as_view(), name='list'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
