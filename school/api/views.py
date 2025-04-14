from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Student,Teacher,Class,School
from .serializers import StudentSerializer,ClassSerializer,TeacherSerializer,SchoolSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def student_list(request):
    # Get filter parameters
    school_name = request.query_params.get('school_name', None)
    firstname = request.query_params.get('firstname', None)
    lastname = request.query_params.get('lastname', None)
    gender = request.query_params.get('gender', None)
    class_id = request.query_params.get('class_id', None)
    
    # Start with all students
    students = Student.objects.all()
    
    # Apply filters if provided
    if school_name:
        # Get students from classes in the specified school
        students = students.filter(schoolclass__school__name__icontains=school_name).distinct()
    if firstname:
        students = students.filter(firstname__icontains=firstname)
    if lastname:
        students = students.filter(lastname__icontains=lastname)
    if gender:
        students = students.filter(gender=gender)
    if class_id:
        students = students.filter(schoolclass_id=class_id)
    
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_student(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def student_details(request,pk):
    student = get_object_or_404(Student,pk=pk)
    serializer = StudentSerializer(student)
    return Response(serializer.data)

@api_view(['GET'])
def school_list(request):
    # Get the name filter from query parameters
    name = request.query_params.get('name', None)
    
    # Start with all schools
    schools = School.objects.all()
    
    # Apply name filter if provided
    if name:
        schools = schools.filter(name__icontains=name)
    
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_school(request):
    serializer = SchoolSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def school_details(request,pk):
    student = get_object_or_404(School,pk=pk)
    serializer = SchoolSerializer(student)
    return Response(serializer.data)

@api_view(['PUT'])
def school_update(request,pk):
    school = get_object_or_404(School, pk=pk)
    serializer = SchoolSerializer(school, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def school_delete(request,pk):
    try:
        school = School.objects.get(pk=pk)
        school.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except School.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_class(request):
    serializer = ClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def class_list(request):
    # Get filter parameters
    school_name = request.query_params.get('school_name', None)
    
    # Start with all classes
    classes = Class.objects.all()
    
    # Apply school name filter if provided
    if school_name:
        classes = classes.filter(school__name__icontains=school_name)
    
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def class_details(request,pk):
    clas = get_object_or_404(Class,pk=pk)
    serializer = ClassSerializer(clas)
    return Response(serializer.data)

@api_view(['GET'])
def teacher_list(request):
    # Get filter parameters
    school_name = request.query_params.get('school_name', None)
    firstname = request.query_params.get('firstname', None)
    lastname = request.query_params.get('lastname', None)
    gender = request.query_params.get('gender', None)
    
    # Start with all teachers
    teachers = Teacher.objects.all()
    
    # Apply filters if provided
    if school_name:
        # Get teachers from classes in the specified school
        teachers = teachers.filter(classes__school__name__icontains=school_name).distinct()
    if firstname:
        teachers = teachers.filter(firstname__icontains=firstname)
    if lastname:
        teachers = teachers.filter(lastname__icontains=lastname)
    if gender:
        teachers = teachers.filter(gender=gender)
    
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def teacher_details(request,pk):
    teacher = get_object_or_404(Teacher,pk=pk)
    serializer = TeacherSerializer(teacher)
    return Response(serializer.data)

@api_view(['POST'])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def class_update(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    serializer = ClassSerializer(class_instance, data=request.data)
    if serializer.is_valid():
        teacher_ids = request.data.get('teacher_ids', [])
        
        class_instance.teachers.clear()
        if teacher_ids:
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            class_instance.teachers.add(*teachers)

        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def class_delete(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)
    class_instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    serializer = TeacherSerializer(teacher, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


   



