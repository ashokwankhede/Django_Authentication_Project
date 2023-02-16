from django.urls import path
from app1 import views

urlpatterns=[
    path('register',views.register,name='register'),
    path('',views.logIn,name='login'),
    path('forgot_pass',views.forgot_pass,name='forgot_pass'),
    path('change_pass/<token>/',views.change_pass,name='change_pass'),
    path('loggedin/',views.Employee_register,name="employee"),
    path('loggedin/show_emp/',views.show_emp,name='show_emp'),
    path('loggedin/show_emp/update_emp/',views.update_emp,name='update'),
    path('loggedin/show_emp/del_emp/',views.del_emp,name='delete'),
    path('logout',views.logout,name='logout'),
]

