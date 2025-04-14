from django.urls import path
from . import views


urlpatterns=[
    path('schools/',views.school_list,name='school_list'),
    path('school/',views.create_school,name='create_school'),
    path('school/<int:pk>/update/',views.school_update,name='update_school'),
    path('school/<int:pk>/delete/',views.school_delete,name='delete_school'),
    path('schools/<int:pk>/',views.school_details,name='school_detials'),
    path('students/',views.student_list,name='student_list'),
    path('student/',views.create_student,name='create_student'),
    path('students/<int:pk>/',views.student_details,name='student_detials'),
    path('student/<int:pk>/update/',views.student_update,name='update_student'),
    path('student/<int:pk>/delete/',views.student_delete,name='delete_student'),
    path('classes/',views.class_list,name='class_list'),
    path('class/',views.create_class,name='create_class'),
    path('classes/<int:pk>/',views.class_details,name='class_detials'),
    path('class/<int:pk>/update/',views.class_update,name='update_class'),
    path('class/<int:pk>/delete/',views.class_delete,name='delete_class'),
    path('teachers/',views.teacher_list,name='teacher_list'),
    path('teacher/',views.create_teacher,name='create_teacher'),
    path('teachers/<int:pk>/',views.teacher_details,name='teacher_detials'),
    path('teacher/<int:pk>/update/',views.teacher_update,name='update_teacher'),
    path('teacher/<int:pk>/delete/',views.teacher_delete,name='delete_teacher'),
]