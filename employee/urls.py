from django.urls import path
from .views import home_page, employee_profile, emp_leave_apply, leave_status

app_name = 'employee_app'

urlpatterns = [
    path("", home_page, name="employee_home_page"),
    path('employee/profile', employee_profile, name='employee_profile_page'),
    path('employee/leave', emp_leave_apply, name='emp_leave_page'),
    path('employee/leave_status', leave_status, name='emp_leave_status_page')
]
