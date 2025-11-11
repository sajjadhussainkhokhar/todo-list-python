from django.urls import path
from .views import ProjectView

project_view = ProjectView.as_view()


urlpatterns = [
    path('', project_view, name='project-list'),  # You can call project_list manually inside view
    path('<int:pk>/', project_view, name='project-detail'),
]
