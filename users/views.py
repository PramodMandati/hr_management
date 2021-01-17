from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import (LoginForm, SignUpForm, UserEmployeeForm, EmployeeSignUpForm,
                    FAQForm, PolicyForm, HolidayForm, Search)
from .models import Admin, Employee, FAQS, Policies, Holidays
from employee.models import LeaveModel


# Create your views here.

def is_admin(user):
    try:
        a = user.admin
        return True
    except:
        return False


@login_required(login_url="/login")
@user_passes_test(is_admin, login_url='/login')
def home_page(request):
    if request.user.is_authenticated:
        obj = LeaveModel.objects.filter(is_approve=None)
        return render(request, "users/home.html", {'objects': obj})
    return redirect("users_app:users_login_page")


def login_page(request):
    if not request.user.is_authenticated:
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            user = User.objects.get(username=request.POST.get('username'))
            login(request=request, user=user)
            try:
                a = request.user.admin
                return redirect("users_app:users_home_page")
            except:
                return redirect("employee_app:employee_home_page")
        return render(request, 'users/login.html', {'form': form})
    try:
        a = request.user.admin
        return redirect("users_app:users_home_page")
    except:
        return redirect("employee_app:employee_home_page")


def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect("users_app:users_home_page")
    form = SignUpForm(data=request.POST or None)
    context = {"show_thing": False, 'form': form}
    if form.is_valid():
        user = User.objects.create_user(username=request.POST.get('username'),
                                        password=request.POST.get('password'),
                                        email=request.POST.get('email'))
        Admin.objects.create(user=user)
        form = SignUpForm()
        context.update({'form': form, "show_thing": True})
    return render(request, 'users/signup.html', context=context)


@login_required(login_url="/login")
def logout_request(request):
    logout(request)
    return redirect("users_app:users_login_page")


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def employee_account_create(request):
    form = UserEmployeeForm(data=request.POST or None)
    form2 = EmployeeSignUpForm(data=request.POST or None)
    created = False
    if form.is_valid() and form2.is_valid():
        user = form.save()
        emp = form2.save(commit=False)
        emp.user = user
        emp.hr_admin = request.user.admin
        emp.save()
        form = UserEmployeeForm()
        form2 = EmployeeSignUpForm()
        created = True
    return render(request, "users/e_signup.html", {"form": form, "form2": form2, "created": created})


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def profile_page(request):
    if request.method == 'POST':
        user = request.user
        user.set_password(request.POST.get('new_password'))
        user.save()
        login(request, user)
    return render(request, 'users/profile.html')


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def manage_faq(request):
    form = FAQForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = FAQForm()
    object_list = FAQS.objects.all()
    context = {'form': form, 'object_list': object_list}
    return render(request, 'users/manage_FAQS.html', context)


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def delete_faq(request, id):
    if FAQS.objects.filter(id=id).exists():
        obj = FAQS.objects.filter(id=id)[0]
        obj.delete()
    return redirect("users_app:users_man_faq_page")


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def manage_policy(request):
    form = PolicyForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = PolicyForm()
    object_list = Policies.objects.all()
    context = {'form': form, 'object_list': object_list}
    return render(request, 'users/manage_Policies.html', context)


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def delete_policy(request, id):
    if Policies.objects.filter(id=id).exists():
        obj = Policies.objects.filter(id=id)[0]
        obj.delete()
    return redirect("users_app:users_man_policy_page")


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def manage_holiday(request):
    form = HolidayForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = HolidayForm()
    object_list = Holidays.objects.all()
    context = {'form': form, 'object_list': object_list}
    return render(request, 'users/manage_holiday.html', context)


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def delete_holiday(request, id):
    if Holidays.objects.filter(id=id).exists():
        obj = Holidays.objects.filter(id=id)[0]
        obj.delete()
    return redirect("users_app:users_man_holiday_page")


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def leave_action(request):
    if request.is_ajax():
        id = request.POST.get('leave_id')
        obj = LeaveModel.objects.get(id=int(id))
        if request.POST.get('status') == 'true':
            obj.is_approve = True
        else:
            obj.is_approve = False
        obj.save()
        return JsonResponse({})


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def employee_search(request):
    form = Search(request.POST or None)
    context = {'form': form, 'search_result': False}
    if form.is_valid():
        object_list = Employee.objects.filter(
            Q(user__username__icontains=form.cleaned_data.get('username')) |
            Q(role=form.cleaned_data.get('role')) |
            Q(team=form.cleaned_data.get('team'))
        )
        context['object_list'] = object_list
        context['search_result'] = True
    return render(request, 'users/employee_search.html', context)


@login_required(login_url='/login')
@user_passes_test(is_admin, login_url='/login')
def employee_view(request, username):
    obj = Employee.objects.filter(user__username=username).first()
    if request.method == 'POST':
        obj.delete()
        return redirect("users_app:users_employee_search_page")
        print(username)
    return render(request, 'users/employee_view.html', {'object': obj})
