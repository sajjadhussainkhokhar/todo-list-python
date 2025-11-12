from rest_framework import serializers
from .models import Task
from project.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description']


class TaskSerializer(serializers.ModelSerializer):
    # nested read-only representation for responses
    project = ProjectSerializer(read_only=True)

    # allow clients to pass `project_id` in POST/PUT bodies to set the FK
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source='project', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Task
        # explicit fields so we can include the write-only `project_id`
        fields = [
            'id', 'project', 'project_id', 'user', 'title', 'description', 'status', 'priority', 'due_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
