from django.contrib import admin
from django.urls import path, include


from .views import EnterPhoneNumber, EnterPhoneCode, ProfileView, ProfileRedirect, ActivationCode, Reset, schema_view



urlpatterns = [
    path('auth/', EnterPhoneNumber.as_view()),
    path('code/', EnterPhoneCode.as_view()),
    path('profile/', ProfileRedirect.as_view(), name='profile-redirect'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('activation_code/', ActivationCode.as_view()),
    path('reset/', Reset.as_view()),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
