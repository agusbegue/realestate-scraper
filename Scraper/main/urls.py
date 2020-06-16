from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from main import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    # path('properties/<int:pk>', views.JobView.as_view(), name='properties'),
    # re_path(r'^properties/(?P<pk>\w+)/$', views.JobView.as_view(), name='properties'),
    re_path(r'^properties(?:/(?P<job_id>d+))?/$', views.Properties.as_view(), name='properties'),

    path('options/<str:action>/<int:job_id>', views.OptionsHandlerView.as_view(), name='options'),

    path('login/', views.Login.as_view(), name='login'),
    path('change-password', views.ChangePassword.as_view(), name='password'),
    path('logout', LogoutView.as_view(), name='logout'),
]