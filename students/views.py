from django.contrib.messages import success
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from .models import Student, ClassName, StudentClass, Location, Schedule, Teacher
from students.crud_students.serializers import StudentSerializer, ClassNameSerializer, StudentClassSerializer, TeacherSerializer, LocationSerializer, ScheduleSerializer


#Viewsets for Student
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
           self.perform_create(serializer)
           return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
           return Response({"success": False ,"errors:" :serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Student.DoesNotExist:
            return Response(
                {"success": False, "message": "Student not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    "success": True,
                    "message": "Student updated successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "success": False,
                "message": "Validation failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        try:
            student =self.get_object()
            student.delete()
            return Response(
                {"success": True, "message": "Student deleted successfully."},
                status=status.HTTP_200_OK,
            )

        except Student.DoesNotExist:
            return Response(
                {"success": False, "message": "Student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            student_class = self.get_object()
            serializer = self.get_serializer(student_class)
            print("dfkmd")
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except StudentClass.DoesNotExist:
            return Response({
                "success": False,
                "message": "StudentClass not found."
            }, status=status.HTTP_404_NOT_FOUND)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



#Viewsets for ClassName
class ClassNameViewSet(viewsets.ModelViewSet):
    queryset = ClassName.objects.all()
    serializer_class = ClassNameSerializer
    lookup_field = 'name'






    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now().date()
        has_students = StudentClass.objects.filter(
            classname=instance,
            start_date__lte=today,
            end_date__gte=today
        ).exists()

        if has_students:
            return Response(
                {"detail": "Can not delete student is learning in the class."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if 'name' in request.data:
            return Response(
                {"error": "Cannot update the name field."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)


class StudentClassViewSet(viewsets.ModelViewSet):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer
    lookup_field = 'id'


    def create(self, request, *args, **kwargs):
        class_id = request.data.get('class_id')
        if not class_id:
            return Response({"error": "class_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            classname = ClassName.objects.get(pk=class_id)
        except ClassName.DoesNotExist:
            return Response({"error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)

        current_size = StudentClass.objects.filter(class_id=classname).count()
        if current_size >= classname.max_size:
            return Response(
                {"error": "Class is full, cannot register more students."},
                status=status.HTTP_400_BAD_REQUEST
            )


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().select_related('class_id', 'schedule')
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": f"An error occurred while fetching data: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def retrieve(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        if student_id:
            queryset = StudentClass.objects.filter(student_id__student_id=student_id).select_related('class_id',
                                                                                                     'schedule')
            if not queryset.exists():
                return Response({
                    "success": True,
                    "data": [],
                    "message": "No records found for the given student_id."
                }, status=status.HTTP_200_OK)
        else:
            queryset = StudentClass.objects.all().select_related('class_id', 'schedule')

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        today = timezone.now().date()
        if instance.start_date <= today <= instance.end_date:
            return Response(
                {"detail": "Cannot delete student class because it's active today."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer