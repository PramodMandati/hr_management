from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Employee, FAQS, Policies, Holidays


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(**self.cleaned_data)
        if not user:
            raise forms.ValidationError("invalid username/password")
        return self.cleaned_data


class UserEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        return username

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = "Username should contain only A-Z, a-z, 0-9 and _"


class EmployeeSignUpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ("role", "team", "salary", "phone")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Employee.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phone number already exists")
        return phone


class FAQForm(forms.ModelForm):
    answer = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = FAQS
        fields = ('question', 'answer')


class PolicyForm(forms.ModelForm):
    policy = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Policies
        fields = ('policy',)


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = ['reason', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_date'].required = False
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})


class Search(forms.Form):
    username = forms.CharField(max_length=20, required=False)
    role = forms.ModelChoiceField(queryset=Employee.objects.values_list('role', flat=True).distinct().order_by('role'),
                                  required=False,
                                  to_field_name='role')
    team = forms.ModelChoiceField(queryset=Employee.objects.values_list('team', flat=True).distinct().order_by('team'),
                                  required=False,
                                  to_field_name='team')

    def clean(self):
        return self.cleaned_data
