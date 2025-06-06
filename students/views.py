from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
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
            return self.error_response("Validation failed.", errors=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Student created successfully.", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'student_id' in request.data and request.data['student_id'] != instance.student_id:
            return self.error_response(message="Updating student_id is not allowed", status_code=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )
        if not has_changes:
            return self.success_response(message="No changes detected.", data=serializer.data, status_code=status.HTTP_200_OK)

        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message="Student updated successfully.", status_code=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )



    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(
                message="Student retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )
        except Http404:
            return self.error_response(
                message="Student not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def list(self, request, *args, **kwargs):
      try:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.success_response(message="Student list retrieved successfully.", data=serializer.data, status_code=status.HTTP_200_OK)
      except Exception as e:
        return self.error_response(message=f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ViewSet for ClassName
class ClassNameViewSet(BaseViewSet):
    queryset = ClassName.objects.all()
    serializer_class = ClassNameSerializer
    lookup_field = 'class_id'
    lookup_url_kwarg = 'class_id'

    def create(self, request, *args, **kwargs):
        schedule_id = request.data.get('schedule_id')
        if not schedule_id:
            return self.error_response(message="schedule_id is required.", status_code=status.HTTP_400_BAD_REQUEST)

        try:
            Schedule.objects.get(pk=schedule_id)
        except Schedule.DoesNotExist:
            return self.error_response(message="Schedule not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(message="Validation failed.", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Class created successfully.", status_code=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('schedule_id')
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(message= "ClassName list retrieved successfully",data=serializer.data,status_code=status.HTTP_200_OK)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return self.error_response(error_message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
        except Http404:
            return self.error_response(message="Class not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(obj)
        return self.success_response(data=serializer.data, message="Class retrieved successfully.", status_code=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        allowed_fields = {'max_size', 'status'}
        incoming_fields = set(request.data.keys())

        disallowed_fields = incoming_fields - allowed_fields

        if disallowed_fields:
            return self.error_response(
                message=f"Only 'max_size' and 'status' can be updated. Not allowed fields: {', '.join(disallowed_fields)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )
        if not has_changes:
            return self.success_response(message="No changes detected.", data=serializer.data)

        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message="Class updated successfully.")

    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )

# ViewSet for StudentClass
class StudentClassViewSet(BaseViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        class_id = request.data.get('class_id')
        if not class_id:
            return self.error_response(message="class_id is required.", status_code=status.HTTP_400_BAD_REQUEST)

        try:
            ClassName.objects.get(pk=class_id)
        except ClassName.DoesNotExist:
            return self.error_response(message="Class not found.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(message="Validation failed.", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Student class created successfully.", status_code=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('class_id')
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(message="Student class list retrieved successfully",data=serializer.data)
        except Exception as e:
            return self.error_response(f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        if student_id:
            obj = StudentClass.objects.filter(student_id__student_id=student_id).select_related('class_id').first()
            if not obj:
                return self.success_response(data=None, message="No record found.",status_code=status.HTTP_200_OK)
        else:
            obj = StudentClass.objects.all().select_related('class_id').first()
            if not obj:
                return self.success_response(data=None, message="No record found.",status_code=status.HTTP_200_OK )

        serializer = self.get_serializer(obj)
        return self.success_response(data=serializer.data,message="Student class retrieved successfully.", status_code=status.HTTP_200_OK)

    def update (self, request, *args, **kwargs):
        return self.error_response(
            message="Updating this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )



# ViewSets for other models
class TeacherViewSet(BaseViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'teacher_id'
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response("Validation failed.", errors=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Teacher created successfully.", status_code=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('teacher_id')
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(message="Teacher list retrieved successfully",data=serializer.data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return self.error_response(f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(data=serializer.data, message="Teacher class retrieved successfully.", status_code=status.HTTP_200_OK)
        except Http404:
            return self.error_response(message="Teacher not found.", status_code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if 'teacher_id' in request.data and request.data['teacher_id'] != instance.teacher_id:
            return self.error_response("Updating teacher_id is not allowed.")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )
        if not has_changes:
            return self.success_response(message="No changes detected.", data=serializer.data,status_code=status.HTTP_200_OK)

        self.perform_update(serializer)
        return self.success_response(data=serializer.data, message="Teacher updated successfully.",status_code=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )

class ScheduleViewSet(BaseViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = 'schedule_id'

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('room_number')
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(message="Schedule list retrieved successfully",data=serializer.data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return self.error_response(f"An error occurred: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(message="Schedule list retrieved successfully",data=serializer.data, status_code=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            return self.success_response(data=[], message="No records found.",status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )


    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        allowed_fields = {'max_size'}
        incoming_fields = set(request.data.keys())

        disallowed_fields = incoming_fields - allowed_fields

        if disallowed_fields:
            return self.error_response(
                message=f"Only 'max_size' can be updated. Not allowed fields: {', '.join(disallowed_fields)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )
        if not has_changes:
            return self.success_response(message="No changes detected.", status_code=status.HTTP_200_OK)

        self.perform_update(serializer)
        return self.success_response(message="No changes detected.", status_code=status.HTTP_200_OK)


class LocationViewSet(BaseViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response( message="Validation failed.", errors=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return self.success_response(data=serializer.data, message="Location created successfully.", status_code=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return self.success_response(message="Room number list retrieved successfully", data=serializer.data,
                                         status_code=status.HTTP_200_OK)
        except Exception as e:
            return self.error_response(f"An error occurred: {str(e)}",
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.success_response(data=serializer.data)
        except Location.DoesNotExist:
            return self.success_response(data=[], message="No records found.")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        allowed_fields = {'max_size'}
        incoming_fields = set(request.data.keys())

        disallowed_fields = incoming_fields - allowed_fields

        if disallowed_fields:
            return self.error_response(
                message=f"Only max_size  can be updated. Not allowed fields: {', '.join(disallowed_fields)}",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        has_changes = any(
            getattr(instance, field) != value
            for field, value in serializer.validated_data.items()
        )
        if not has_changes:
            return Response({"detail": "No changes detected."}, status=status.HTTP_200_OK)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        return self.error_response(
            message="Deleting this record is not allowed.",
            status_code=status.HTTP_403_FORBIDDEN
        )
