from django.urls import path
from .views import ProjectCreateView, ProjectDetailView, ProjectListView


urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),  # You can call project_list manually inside view
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('', ProjectListView.as_view(), name='project-list'),
]
