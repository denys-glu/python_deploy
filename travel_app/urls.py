from django.urls import path
from . import views

urlpatterns = [
    path('/', views.index),
    path('/add_trip', views.add_trip),
    path('/add_trip_post', views.add_trip_post),
    path('/view/<int:trip_id>', views.view_trip),
    path('/delete/<int:trip_id>', views.delete_trip),
    path('/cancel/<int:trip_id>', views.cancel_trip),
    path('/join/<int:trip_id>', views.join_trip)
]
