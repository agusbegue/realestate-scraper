from django.urls import path
from main import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/<int:pk>', views.JobView.as_view(), name='list'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='detail'),
    path('crawl/', views.crawl, name='crawl'),
    path('error/', views.error, name='error'),
    path('loading/', views.loading, name='loading'),
    path('tabel/', views.OrderListJson.as_view(), name='order_list_json'),
    path('lugares/', views.get_lugares, name='lugares'),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # url(r'^api/crawl/', views.crawl, name='crawl'),
]