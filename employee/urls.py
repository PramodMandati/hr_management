from django.urls import path
from .views import home_page, emp_leave_apply, leave_status

app_name = 'employee_app'

urlpatterns = [
    path("", home_page, name="employee_home_page"),
    path('leave', emp_leave_apply, name='emp_leave_page'),
    path('leave_status', leave_status, name='emp_leave_status_page')
]
