from students.crud_students.serializers import StudentSerializer

def save_student(student):
    serializer = StudentSerializer(data=student)
    if serializer.is_valid():
        serializer.save()
        return True
    else:
        return False