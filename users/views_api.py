from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.serializers import ModelSerializer, CharField
from .models import Employee


class LoginView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        return JsonResponse({'token': token.key})

    def handle_exception(self, exc):
        resp = super().handle_exception(exc)
        return resp


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']


class EmployeeSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'phone', 'role', 'team', 'salary')

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = User.objects.create_user(**user)
        user.save()
        emp = Employee.objects.create(**validated_data, hr_admin=self.context.get('request').user.admin, user=user)
        emp.save()
        return emp


class IsHRAdmin(BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.admin.is_hr_admin:
                return True
            return False
        except:
            return False


class BearerTokenAuthentication(TokenAuthentication):

    keyword = 'Bearer'


class EmployeeListView(ListAPIView):

    permission_classes = [IsAuthenticated, IsHRAdmin]
    authentication_classes = [BearerTokenAuthentication]

    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return self.request.user.admin.employee_set.all()


class EmployeeCreateView(CreateAPIView):

    permission_classes = [IsAuthenticated, IsHRAdmin]
    authentication_classes = [BearerTokenAuthentication]

    serializer_class = EmployeeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


