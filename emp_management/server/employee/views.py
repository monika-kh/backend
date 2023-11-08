from datetime import date, datetime

from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend, FilteringFilterBackend)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

# from users.permissions import IsEmployee

from .documents import EmployeeDocument
from .models import Employee, EmployeeAttendence
from .serializers import (AttendenceSerializer, EmployeeAttendanceSerializer,
                          EmployeeListSerializer, EmployeeSerializer,
                          SearchEmployeeSerializer, UpdateAttendanceSerializer,
                          UserDetailUpdateSerializer)


class CreateAttendenceView(APIView):
    def post(self, request):
        serializer = AttendenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class EmployeeListView(APIView):
    def get(self, request):
        current_month = datetime.now().month
        current_year = datetime.now().year
        employees = Employee.objects.prefetch_related(
            Prefetch(
                "emp_attendence",
                queryset=EmployeeAttendence.objects.filter(
                    date__month=current_month, date__year=current_year
                ).only("date", "is_present"),
            )
        ).all()
        serializer = EmployeeListSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeDetailView(APIView):

    def get(self, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        attendance = EmployeeAttendence.objects.filter(
            employee=employee, date__month=timezone.now().month
        )
        attendance_serializer = EmployeeAttendanceSerializer(
                        attendance, many=True)
        return Response(
            {
                "employee": serializer.data,
                "attendance": attendance_serializer.data
            }
        )

    def patch(self, request, pk=None):
        if "employee-profile-update" in self.request.path:
            user = settings.AUTH_USER_MODEL
            serializer = UserDetailUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.initial_data)
            else:
                return Response(serializer.errors)
        else:
            employee = get_object_or_404(Employee, pk=pk)
            attendence = EmployeeAttendence.objects.filter(
                employee=employee, date=date.today()
            ).first()
            serializer = UpdateAttendanceSerializer(
                attendence, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                attendence.delete()
                return Response(serializer.data)
            return Response(serializer.errors)


class AllUsersView(APIView):
    def get(self, request):
        d1 = []
        employees = Employee.objects.all()
        for emp in employees:
            data = {}
            data["user_id"] = emp.id
            data["name"] = emp.user.first_name + " " + emp.user.last_name
            data["date"] = date.today().strftime("%d/%m/%Y")
            emp_attend = EmployeeAttendence.objects.filter(
                employee=emp.id, date=date.today()
            )
            if emp_attend.exists():
                data["attendence"] = (
                    emp.emp_attendence.all().last().is_present
                    if emp.emp_attendence.all().last().is_present
                    else False
                )
            else:
                data["attendence"] = False

            d1.append(data)
        return Response(d1)


class GetStaffDetailsView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeSearchView(DocumentViewSet):
    document = EmployeeDocument
    serializer_class = SearchEmployeeSerializer
    lookup_field = "id"

    filter_backends = [
        FilteringFilterBackend,
        CompoundSearchFilterBackend,
    ]

    # Define the fields you want to filter on
    filter_fields = {
        "id": "id",
        "city": "city",
        "department": "department",
        "username": "user.username",
        "firstname": "user.first_name",
        "lastname": "user.last_name",
        "technologies_familiar_with": "technologies_familiar_with.name",
        "phone_number": "phone_number",
        "address": "address",
    }

    search_fields = (
        "id",
        "department",
        "city",
        "user.username",
        "user.first_name",
        "user.last_name",
        "technologies_familiar_with",
        "phone_number",
    )


class AllCityView(APIView):
    def get(self, request):
        data = Employee.objects.all().\
            values_list("city", flat=True).distinct()
        if data is not []:
            return Response(data)
        else:
            return Response({"message": "No data found"})


class UserFirstNameView(APIView):
    def get(self, request):
        data = (
            Employee.objects.all().
            values_list("user__first_name", flat=True).distinct()
        )
        if data is not []:
            return Response(data)
        else:
            return Response({"message": "No data found"})
