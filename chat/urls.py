from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('home/', views.homepage, name="homepage"),
    path('', views.chat_icon, name="chat_icon"),
    path("<int:pk>/", views.chatroom, name="chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
]
urlpatterns += staticfiles_urlpatterns()