from django.urls import path,include
from blog import views

app_name='blog'

urlpatterns = [

   path('uselist/',views.UserListView.as_view(),name='uselist'),
   path('catlist/',views.CategoryListView.as_view(),name='catlist'),
   path('list/',views.BlogListView.as_view(),name='list'),
   path('list/<int:pk>/',views.BlogDetailView.as_view(),name='detail'),
   path('list/update/<int:pk>',views.BlogUpdateView.as_view(),name='update'),
   path('list/delete/<int:pk>',views.BlogDeleteView.as_view(),name='delete'),
   path('list/create',views.BlogCreateView.as_view(),name='create'),
   path('list/<int:pk>/create2',views.CommentCreateView.as_view(),name='create2'),
   path('draft/',views.DraftListView.as_view(),name='draft'),
   path('list/<int:pk>/publish',views.post_publish,name='publish'),
   path('list/<int:pk>/approve/',views.comment_approve,name='approve'),
   path('list/<int:pk>/remove/',views.comment_remove,name='remove'),
   path('register',views.UserCreateView.as_view(),name='register'),
   path('list/category',views.CategoryCreateView.as_view(),name='category'),
   path('<str:cats>/',views.CategoryView,name='cats'),
   path('like/<int:pk>/',views.LikeView,name='jay_like'),
   path('<int:pk>',views.UserProfile.as_view(),name='user_profile'),
   path('<int:pk>/update2',views.UserUpdateView.as_view(),name='update_user'),






]
