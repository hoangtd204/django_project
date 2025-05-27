from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from .models import Student, ClassName, StudentClass
from students.crud_students.serializers import StudentSerializer, ClassNameSerializer, StudentClassSerializer


#Viewsets for Student
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'student_id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
           self.perform_create(serializer)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def list(self, request, *args, **kwargs):
        try:
           students=self.get_object()
           serializer=StudentSerializer(students, many=True)
           return Response(
            {"success": True,"data":serializer.data},
            status=status.HTTP_200_OK,
            )
        except Student.DoesNotExist:
            return Response(
                {"success": False, "data":serializer.errors,},
                status=status.HTTP_204_NO_CONTENT,
            )

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
    lookup_field = 'student'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'start_date' not in data:
            data['start_date'] = timezone.now().date()

        if 'end_date' not in data:
            data['end_date'] = timezone.now().date() + timedelta(days=30)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        try:
            students = self.get_object()
            serializer = StudentSerializer(students, many=True)
            return Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Student.DoesNotExist:
            return Response(
                {"success": False, "data": serializer.errors, },
                status=status.HTTP_204_NO_CONTENT,
            )