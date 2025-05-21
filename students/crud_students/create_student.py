from students.crud_students.serializers import StudentSerializer


def create_student(student):
    serializer = StudentSerializer(data=student)
    if serializer.is_valid():
        serializer.save()
        return True
    else:
        return False
