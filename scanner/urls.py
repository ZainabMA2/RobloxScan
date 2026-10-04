from django.urls import path
from .views import(
    RobloxProjectListView,
    RobloxProjectCreateView,
    RobloxProjectDetailView,
    RobloxProjectUpdateView,
    RobloxProjectDeleteView,
    CodeScanCreateView,
    CodeScanDetailView,
    DashboardView

)

app_name ="scanner"
urlpatterns=[
    path("projects/",RobloxProjectListView.as_view(), name="project_list"),
    path("projects/add/",RobloxProjectCreateView.as_view(), name="project_add"),
    path("projects/<int:pk>/",RobloxProjectDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/update/",RobloxProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/",RobloxProjectDeleteView.as_view(), name="project_delete"),
    path("projects/<int:pk>scan/", CodeScanCreateView.as_view(), name="scan_create"),
    path("scans/<int:pk>/", CodeScanDetailView.as_view(), name="scan_result"),
    path("dashboard/",DashboardView.as_view(), name="dashboard")

]