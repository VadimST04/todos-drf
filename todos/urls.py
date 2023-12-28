from django.urls import path

from todos import views

urlpatterns = [
    path('', views.TodosAPIView.as_view(), name='all-my-todos'),
    path('create/', views.TodosAPIView.as_view(), name='create-todos'),
    path('<int:pk>/', views.TodosAPIView.as_view(), name='delete-todos'),
]
