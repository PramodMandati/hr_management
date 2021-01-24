from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login

from .forms import LeaveForm
from .models import LeaveModel


# Create your views here.
def is_employee(user):
    try:
        user.employee
        return True
    except:
        return False


@login_required(login_url="/login")
@user_passes_test(is_employee, login_url='/login')
def home_page(request):
    show_pop_up = False
    if request.method == 'POST':
        user = request.user
        user.set_password(request.POST.get('emp_new_pass'))
        user.save()
        login(request, user)
        show_pop_up = True
    return render(request, 'employee/emp_profile.html', {'show_pop_up': show_pop_up})


# @login_required(login_url='/login')
# @user_passes_test(is_employee, login_url='/login')
# def employee_profile(request):
#     show_pop_up = False
#     if request.method == 'POST':
#         user = request.user
#         user.set_password(request.POST.get('emp_new_pass'))
#         user.save()
#         login(request, user)
#         show_pop_up = True
#     return render(request, 'employee/emp_profile.html', {'show_pop_up': show_pop_up})


@login_required(login_url='/login')
@user_passes_test(is_employee, login_url='/login')
def emp_leave_apply(request):
    show_pop_up = False
    form = LeaveForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.employee = request.user.employee
        obj.save()
        form = LeaveForm()
        show_pop_up = True
    return render(request, 'employee/emp_leave.html', {'form': form, 'show_pop_up': show_pop_up})


@login_required(login_url='/login')
@user_passes_test(is_employee, login_url='/login')
def leave_status(request):
    object_list = request.user.employee.leavemodel_set.all()
    return render(request, 'employee/emp_leave_status.html', {'object_list': object_list})
