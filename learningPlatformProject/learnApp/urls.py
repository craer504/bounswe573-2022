from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.learnapp_home, name="home_url"),
    path('workspace/<str:pk>/', views.learnapp_workspace, name="workspace_url"),
    path('create_workspace/', views.createWorkspace, name="create_workspace"),
    path('update_workspace/<str:pk>/',views.updateWorkspace, name="update_workspace"),
    path('delete_workspace/<str:pk>/',views.deleteWorkspace, name="delete_workspace"),
    path('delete_message/<str:pk>/', views.deleteMessage, name="delete_message"),
    path('profile/<str:pk>/', views.userProfile, name="user_profile"),
    path('update_user/', views.updateUser, name="update_user"),
]
