from django.conf.urls import url

from apps.users import views


urlpatterns = [
    # url(r'^register$', views.register, name='register'),
    # url(r'^do_register', views.do_register, name='do_register'),

    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^active/(.+)$', views.ActiveView.as_view(), name='active'),

    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^login/psw_forget/$', views.PswForgetView.as_view(), name='psw_forget'),
    url(r'^login/psw_sendmail/$', views.PswSendMailView.as_view(), name='psw_sendmail'),
    url(r'^setpsw/(.+)$', views.SetPswView.as_view(), name='setpsw'),
    url(r'^psw_comfirm/', views.PswComfirmView.as_view(), name='psw_comfirm'),

    url(r'^address/$', views.AddressView.as_view(), name='address'),
    url(r'^order/$', views.OrderView.as_view(), name='order'),
    url(r'^$', views.InfoView.as_view(), name='info'),

]
