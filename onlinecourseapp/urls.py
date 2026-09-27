from django.urls import path
from . import views

app_name = 'onlinecourseapp'

urlpatterns = [
    # Homepage / Course List
    path('', views.popular_course_list, name='index'),
    
    # Course Details
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Exam Page
    path('course/<int:course_id>/exam/', views.exam, name='exam'),
    
    # Submit Exam View
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    
    # Exam Result View
    path('submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
