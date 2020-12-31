from django.urls import path

from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:entry_id>/', views.read, name='read'),
    path('add/', views.add, name='add'),
    path('<int:entry_id>/edit/', views.edit, name='edit'),
    path('<int:entry_id>/update/', views.update, name='update'),
    path('<int:entry_id>/delete/', views.delete, name='delete'),
    path('confirm/', views.confirm, name='confirm'),
    path('signup/', views.signup, name='signup'),
]

