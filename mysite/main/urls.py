from django.urls import path
from . import views
urlpatterns = [
    path('csrf_token/', views.get_csrf_token, name='csrf_token'),
    path('account/', views.AccountView.as_view(), name='account'),
    path("app/", views.AppView.as_view(), name='app'),
    path('drive/', views.DriveView.as_view(), name='drive'),
    path('page/', views.PageView.as_view(), name='page')
]