from rest_framework import viewsets, status
from rest_framework.response import Response

from django.utils import timezone
from .models import Student, ClassName, StudentClass, Location, Schedule, Teacher
from students.Views.serializers import (
    StudentSerializer, ClassNameSerializer, StudentClassSerializer,
    TeacherSerializer, LocationSerializer, ScheduleSerializer
)

# BaseViewSet for DRY principle
class BaseViewSet(viewsets.ModelViewSet):
    def success_response(self, data=None, message=None, status_code=status.HTTP_200_OK):
        response = {"success": True}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
        return Response(response, status=status_code)

    def error_response(self, message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response = {"success": False, "message": message}
        if errors:
            response["errors"] = errors
        return Response(response, status=status_code)

# ViewSet for Student
class StudentViewSet(BaseViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response("Validation failed.", errors=serializer.errors)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Student created successfully.", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'student_id' in request.data and request.data['student_id'] != instance.student_id:
            return self.error_response("Updating student_id is not allowed.")

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )

        if not has_changes:
            return self.success_response(message="No changes detected.", data=serializer.data)

        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message="Student updated successfully.")


    def destroy(self, request, *args, **kwargs):
        try:
            student = self.get_object()
            student.delete()
            return self.success_response(message="Student deleted successfully.")
        except Student.DoesNotExist:
            return self.error_response("Student not found.", status_code=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(data=serializer.data)
        except Student.DoesNotExist:
            return self.error_response("Student not found.", status_code=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(data=serializer.data)

# ViewSet for ClassName
class ClassNameViewSet(BaseViewSet):
    queryset = ClassName.objects.all()
    serializer_class = ClassNameSerializer
    lookup_field = 'class_id'

    def create(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule_id')
        if not schedule_id:
            return self.error_response("schedule_id is required.")

        try:
            Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            return self.error_response("Schedule not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response("Validation failed.", errors=serializer.errors)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Class created successfully.", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if 'name' in request.data:
            return self.error_response("Cannot update the 'name' field.")

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if not serializer.is_valid():
            return self.error_response("Validation failed.", errors=serializer.errors)
        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message="Class updated successfully.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now().date()
        is_active = instance.start_date <= today <= instance.end_date
        has_students = StudentClass.objects.filter(class_id=instance).exists()

        if is_active or has_students:
            return self.error_response("Cannot delete class because it is active or has registered students.")

        return super().destroy(request, *args, **kwargs)

# ViewSet for StudentClass
class StudentClassViewSet(BaseViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        class_id = request.data.get('class_id')
        if not class_id:
            return self.error_response("class_id is required.")

        try:
            ClassName.objects.get(pk=class_id)
        except ClassName.DoesNotExist:
            return self.error_response("Class not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response("Validation failed.", errors=serializer.errors)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Student class created successfully.", status_code=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('class_id__')
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(data=serializer.data)
        except Exception as e:
            return self.error_response(f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        if student_id:
            queryset = StudentClass.objects.filter(student_id__student_id=student_id).select_related('class_id', 'schedule')
            if not queryset.exists():
                return self.success_response(data=[], message="No records found.")
        else:
            queryset = StudentClass.objects.all().select_related('class_id', 'schedule_id')

        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now().date()
        is_active = instance.start_date <= today <= instance.end_date
        has_students = StudentClass.objects.filter(class_id=instance).exists()

        if is_active or has_students:
            return self.error_response("Cannot delete class because it is active or has registered students.")

        return super().destroy(request, *args, **kwargs)


# ViewSets for other models
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
