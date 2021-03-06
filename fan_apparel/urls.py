from django.urls import path
from . import views


urlpatterns = [
    path('users/register/', views.registerUser, name='register'),

    path('users/login', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),


    path('products/', views.getProducts, name='products'),

    path('users/profile/', views.getUserProfile, name='user-profile'),

    path('users/profile/update/', views.updateUserProfile, name='user-profile-update'),

    path('products/<str:pk>', views.getProduct, name='product'),

    path('orders/add/', views.addOrderItems, name='orders-add'),
]
