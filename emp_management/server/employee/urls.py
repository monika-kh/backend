from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        "add-attendence/", views.CreateAttendenceView.as_view(), name="add-attendence"
    ),
    path("employee-list/", views.EmployeeListView.as_view(), name="employee-list"),
    path(
        "employee-detail/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
    path(
        "employee-profile-update/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="employee-update",
    ),
    path("users/", views.AllUsersView.as_view(), name="users"),
    path("staff-details/", views.GetStaffDetailsView.as_view(), name="staff-details"),
    path(
        "search/", views.EmployeeSearchView.as_view({"get": "list"}), name="emp-search"
    ),
    path("city/", views.AllCityView.as_view(), name="city"),
    path("names/", views.UserFirstNameView.as_view(), name="names"),
]
