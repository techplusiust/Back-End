from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer
from rest_framework.response import Response


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optionally filter courses by faculty or professor."""
        queryset = super().get_queryset()
        faculty_fa = self.request.query_params.get('faculty_fa')
        faculty_en = self.request.query_params.get('faculty_en')
        professor = self.request.query_params.get('professor_id')
        
        if faculty_fa:
            queryset = queryset.filter(faculty_fa=faculty_fa)
        
        elif faculty_en:
            queryset = queryset.filter(faculty_fa=faculty_en)
        
        if professor:
            queryset = queryset.filter(professor_id=professor)
        return queryset
  
  
    def partial_update(self, request, *args, **kwargs):
        """Handle partial updates for a course."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)