from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from main import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    re_path(r'^properties(?:/(?P<job_id>d+))?/$', views.Properties.as_view(), name='properties'),

    path('job-options/<str:action>/<int:job_id>', views.JobOptionsHandlerView.as_view(), name='job_options'),
    path('prop-options/<str:action>/<int:prop_id>', views.PropertyOptionsHandlerView.as_view(), name='prop_options'),

    path('login/', views.Login.as_view(), name='login'),
    path('change-password', views.ChangePassword.as_view(), name='password'),
    path('logout', LogoutView.as_view(), name='logout'),
]