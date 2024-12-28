from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Optionally filter courses by faculty or professor."""
        queryset = super().get_queryset()
        faculty = self.request.query_params.get('faculty')
        professor = self.request.query_params.get('professor')
        if faculty:
            queryset = queryset.filter(faculty=faculty)
        if professor:
            queryset = queryset.filter(professor_id=professor)
        return queryset
