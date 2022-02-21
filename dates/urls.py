from django.urls import path
from dates import views


urlpatterns = [
    path('clients/create/', views.ClientCreateView.as_view(), name='create-client'),
    path('clients/<int:pk>/match/', views.AddFollowerView.as_view(), name='clients-match'),
    path('clients/list/', views.ClientsFollowerView.as_view()),
    path('list/', views.ClientListView.as_view()),
]
