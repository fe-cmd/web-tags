from django.urls import path
from . import views

app_name = "questans"

urlpatterns = [
    path('', views.result, name="result"),
    path('filters/', views.show_filters, name="show_filters"), 
    path('filters1/', views.show_filters1, name="show_filters1"), 
    path('filters/fetch_questions/', views.fetch_questions, name="fetch_questions"),    
    path('filters1/fetch_questions1/', views.fetch_questions1, name="fetch_questions1"),
    path('filters/fetch_questions/downloads/', views.downloadpq, name="downloadpq"),
    path('filters1/fetch_questions1/downloads/', views.downloadpq, name="downloadpq")
]
