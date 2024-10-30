from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('certificate/', views.CertificateListView.as_view(), name='Certificate-list'),
    path('certificate/<int:pk>/', views.CertificateDetailView.as_view(), name='Certificate-detail'),
    path('courses/', views.CourseListView.as_view(), name='courses-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='courses-detail'),
    path('reset-database/',
         views.reset_database, name='reset_database'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
]
