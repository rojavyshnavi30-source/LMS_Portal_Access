from django.urls import path
from . import views
urlpatterns=[
    path('', views.show_all_lms, name='show_all_lms'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/', views.add_course, name='add_doctor'),
    path('update/<int:pk>/',views.update_course,name='update'),
    path('delete/<int:pk>/',views.delete_course,name='delete'),
    path('course_list/', views.course_list, name='course_list'),
    path('course-details-json/<int:course_id>/', views.course_details_json, name='course_details_json'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course1, name='delete_course'),
    path('add_courses/', views.add_courses, name='add_courses'),
    path('search/',views.searchBar,name='search'),
]