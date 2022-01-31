from django.urls import path
from .views import (
    login_page, home_page, logout_request, employee_account_create, all_access_page,
    profile_page, manage_faq, delete_faq, manage_policy, delete_policy, manage_holiday,
    delete_holiday, leave_action, employee_search, employee_view, edit_employee_details)

app_name = 'users_app'

urlpatterns = [
    path('', all_access_page),
    path('home', home_page, name="users_home_page"),
    path("login", login_page, name="users_login_page"),
    # path("signup", sign_up_page, name="users_signup_page"),
    path('logout', logout_request, name="users_logout_page"),
    path("add_employee", employee_account_create, name="users_add_employee_page"),

    path('profile', profile_page, name="users_profile_page"),
    path('manage_faqs', manage_faq, name="users_man_faq_page"),
    path('delete_faqs/<int:id>', delete_faq, name="users_del_faq_page"),
    path('manage_policy', manage_policy, name="users_man_policy_page"),
    path('delete_policy/<int:id>', delete_policy, name="users_del_policy_page"),
    path('manage_holiday', manage_holiday, name="users_man_holiday_page"),
    path('delete_holiday/<int:id>', delete_holiday, name="users_del_holiday_page"),

    # path("testing", Testing.as_view())
    path('leave',leave_action, name='ajax_leave'),
    path('search', employee_search, name='users_employee_search_page'),
    path('search/employee/<slug:username>',employee_view, name='users_employee_view_page'),
    path('search/employee/<slug:username>/edit',edit_employee_details, name='users_employee_edit_page'),
]
# users_app:users_home_page


from .views_api import LoginView, EmployeeListView, EmployeeCreateView

urlpatterns += [
    path('api/login', LoginView.as_view()),
    path('api/getEmployees', EmployeeListView.as_view()),
    path('api/createEmployee', EmployeeCreateView.as_view()),
]
