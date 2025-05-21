from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from students.models import Student
from students.crud_students.search_student import find_student_by_id
from students.crud_students.create_student import create_student
from students.crud_students.update_student import (
    change_student_inf,
    find_student_by_id_for_update,
)



@api_view(["POST"])
def creat_student(request):
    result = create_student(request.data)
    if result:
        return Response(
            {"success": True, "message": "Created Successfully", "data": request.data},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response(
            {"success": False, "message": "Create Failed", "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )


# search_student_by_sid
@api_view(["GET"])
def search_student(request):
    student_id_for_searching = request.GET.get("student_id", "")
    student, errors = find_student_by_id(student_id_for_searching)

    if student:
        return Response(
            {
                "success": True,
                "message": "Student Found",
                "data": student,
                "error": errors,
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "success": False,
                "message": "Student Not Found",
                "data": None,
                "error": errors,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

# #update_student's inf
@api_view(["PUT"])
def update_student(request, student_id):
    state, student = find_student_by_id_for_update(student_id)
    if state and student:
        result, student_after = change_student_inf(request, student)

        if result:
            return Response(
                {
                    "success": True,
                    "message": "Student Updated",
                    "data": student_after,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "success": False,
                "message": "Update Failed",
                "data": None,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "success": False,
            "message": "Student Not Found",
            "data": None,
        },
        status=status.HTTP_404_NOT_FOUND,
    )


@api_view(["DELETE"])
def delete_student(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        student.delete()
        return Response(
            {"success": True, "message": "Student deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    except Student.DoesNotExist:
        return Response(
            {"success": False, "message": "Student not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
