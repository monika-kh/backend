from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from basics.serializers import TechnologySerializer

from .models import Employee, EmployeeAttendence, Technology, User


class AttendenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendence
        fields = "__all__"


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField()

    class Meta:
        model = EmployeeAttendence
        fields = (
            "date",
            "is_present",
        )


class UpdateAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendence
        fields = ("is_present",)


class EmployeeListSerializer(serializers.ModelSerializer):
    emp_attendence = EmployeeAttendanceSerializer(many=True)

    class Meta:
        model = Employee
        fields = ("id", "emp_attendence", "department")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance:
            representation["username"] = instance.user.username
            representation["firstname"] = instance.user.first_name
            representation["lastname"] = instance.user.last_name

        return representation


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tech_list = []
        if instance:
            representation["username"] = instance.user.username
            representation["firstname"] = instance.user.first_name
            representation["lastname"] = instance.user.last_name
            representation["user_id"] = instance.user.id
            for i in instance.technologies_familiar_with.all():
                tech_list.append(i.name)
            representation["tech_list"] = tech_list
        return representation


class UserDetailUpdateSerializer(serializers.ModelSerializer):
    department = serializers.CharField(write_only=True)
    phone_number = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "type",
            "department",
            "last_name",
            "first_name",
            "phone_number",
            "city",
            "address",
        ]

    def update(self, obj, validated_data):
        user = User.objects.filter(id=self.initial_data["user"])

        if user:
            user[0].first_name = (
                validated_data["first_name"]
                if validated_data["first_name"] else ""
            )
            user[0].last_name = (
                validated_data["last_name"]
                if validated_data["last_name"] else ""
            )
            user[0].save()
            emp = Employee.objects.filter(user=self.initial_data["user"])
            if emp:
                emp[0].department = (
                    validated_data["department"]
                    if validated_data["department"] else ""
                )
                emp[0].phone_number = (
                    validated_data["phone_number"]
                    if validated_data["phone_number"]
                    else ""
                )
                emp[0].address = (
                    validated_data["address"]
                    if validated_data["address"] else ""
                )
                emp[0].city = (
                    validated_data["city"].lower()
                    if validated_data["city"] else ""
                )
                if self.initial_data["technologies_familiar_with"] is not None:
                    if emp[0].technologies_familiar_with.all() is not None:
                        emp[0].technologies_familiar_with.set("")
                    for t in self.initial_data["technologies_familiar_with"]:
                        technology = Technology.objects.get(name=t)
                        emp[0].technologies_familiar_with.add(technology)
                emp[0].save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class StaffDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "department",
            "gender",
            "technologies_familiar_with",
            "phone_number",
            "address",
            "city",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.technologies_familiar_with.all().exists():
            tech = [i.name for i in instance.technologies_familiar_with.all()]
            data["tech"] = tech
        return data


class PhoneNumberSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, PhoneNumber):
            return str(value)
        return None


class SearchEmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    firstname = serializers.CharField(source="user.first_name", read_only=True)
    lastname = serializers.CharField(source="user.last_name", read_only=True)
    technologies_familiar_with = TechnologySerializer(many=True)
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "city",
            "department",
            "username",
            "firstname",
            "lastname",
            "phone_number",
            "technologies_familiar_with",
            "address",
        )

    def get_phone_number(self, obj):
        return obj.phone_number["national_number"] if obj.phone_number else 0
