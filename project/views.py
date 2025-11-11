from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Project
from dotenv import load_dotenv
import os

class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk = None):
        if pk:
            try:
                project = Project.objects.get(pk=pk)
            except Project.DoesNotExist:
                return Response({'error': 'Project not found'}, status=404)
        
            project_data = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at,
                'updated_at': project.updated_at,
            }
            return Response(project_data)
    
        projects = Project.objects.all().values('id', 'name', 'description', 'created_at', 'updated_at')
        return Response(list(projects))

    def post(self, request):
        if request.method == 'POST':
            load_dotenv()
            name =  os.getenv("PROJECT_NAME") + '-' + request.data.get('name')
            description = request.data.get('description')
            project = Project.objects.create(name=name, description=description)
            return Response({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at,
                'updated_at': project.updated_at,
            }, status=201)


    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=404)

        if request.method == 'PUT':
            project.name = request.data.get('name', project.name)
            project.description = request.data.get('description', project.description)
            project.save()
            return Response({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'created_at': project.created_at,
                'updated_at': project.updated_at,
            })

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=404)

        if request.method == 'DELETE':
            project.delete()
            return Response(status=204)