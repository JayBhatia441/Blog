from django.urls import path
from blog.api import views
from rest_framework.authtoken.views import obtain_auth_token
app_name:'blog'

urlpatterns = [

path('<int:pk>/',views.api_detail_view,name='detail'),
path('<int:pk>/update',views.api_update_view,name='update'),
path('<int:pk>/delete',views.api_delete_view,name='delete'),
path('create',views.api_create_view,name='create'),
path('register',views.register_view,name='register'),
path('login',obtain_auth_token,name='register'),
path('list',views.APIListView.as_view(),name='list')

]
