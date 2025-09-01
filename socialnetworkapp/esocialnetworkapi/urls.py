from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .admin import admin_site, admin
from esocialnetworkapi import views


router = DefaultRouter()
router.register("users", views.UserViewSet, basename="user")
router.register('posts', views.PostViewSet, basename='post')
router.register('comments', views.CommentViewSet, basename='comment')
router.register('reactions', views.ReactionViewSet, basename='reaction') 
router.register('survey', views.SurveyPostViewSet, basename='survey')
router.register('group', views.GroupViewSet, basename='group')
router.register('contact', views.ContactViewSet, basename='contact')

urlpatterns = [
    path('admin_all/', admin.site.urls, name="admin_all"),
    path('admin/', admin_site.urls, name="custom_admin"),
    path('api/', include(router.urls)),
    path('api/group-create/', views.GroupCreateView.as_view(), name='group-create'),
    path('api/group-update/', views.GroupUpdateView.as_view(), name='group-update'),
    path('api/users/<int:user_id>/posts/', views.UserPostListView.as_view(), name='user-posts'),
    path('api/users/<int:id>', views.UserProfileView.as_view(), name='user-profile'),
    path('api/chat/', views.ChatAPIView.as_view(), name="chat-api"),
    re_path(r'^.*$', views.FrontendAppView.as_view()),

]

