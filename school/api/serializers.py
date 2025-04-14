from rest_framework import serializers
from .models import Student,Class,Teacher,School
from django.shortcuts import get_object_or_404


class SchoolSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = (
            'id',
            'name',
            'shotname',
            'address',
            'classroom_count',
            'teacher_count',
            'student_count',
        )

    def get_classroom_count(self, obj):
        return obj.class_set.count()

    def get_teacher_count(self, obj):
        # Get all unique teachers from all classes in the school
        teacher_ids = set()
        for class_instance in obj.class_set.all():
            teacher_ids.update(class_instance.teachers.values_list('id', flat=True))
        return len(teacher_ids)

    def get_student_count(self, obj):
        # Get all students from all classes in the school
        return Student.objects.filter(schoolclass__school=obj).count()

class StudentSerializer(serializers.ModelSerializer):
    schoolclass_id = serializers.IntegerField(write_only=True, required=False)
    schoolclass = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Student
        fields = (
            'id',
            'firstname',
            'lastname',
            'gender',
            'schoolclass',
            'schoolclass_id'
        )

    def create(self, validated_data):
        schoolclass_id = validated_data.pop('schoolclass_id', None)
        if schoolclass_id:
            schoolclass = get_object_or_404(Class, id=schoolclass_id)
            validated_data['schoolclass'] = schoolclass
        return super().create(validated_data)

    def update(self, instance, validated_data):
        schoolclass_id = validated_data.pop('schoolclass_id', None)
        if schoolclass_id:
            schoolclass = get_object_or_404(Class, id=schoolclass_id)
            instance.schoolclass = schoolclass
        return super().update(instance, validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'id',
            'firstname',
            'lastname',
            'gender',
        )

class ClassSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    teacher_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    school_id = serializers.IntegerField(write_only=True)
    school = serializers.StringRelatedField(read_only=True)
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = (
            'id',
            'grade',
            'room',
            'school',
            'school_id',
            'teachers',
            'teacher_ids',
            'teacher_count',
            'student_count',
        )

    def get_teacher_count(self, obj):
        return obj.teachers.count()
    
    def get_student_count(self, obj):
        return obj.student_set.count()

    def create(self, validated_data):
        teacher_ids = validated_data.pop('teacher_ids', [])
        school_id = validated_data.pop('school_id')
        
        # Get the school instance
        school = get_object_or_404(School, id=school_id)
        validated_data['school'] = school
        
        class_instance = super().create(validated_data)
        
        # Add teachers to the class
        if teacher_ids:
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            class_instance.teachers.add(*teachers)
        
        return class_instance

    def update(self, instance, validated_data):
        teacher_ids = validated_data.pop('teacher_ids', [])
        school_id = validated_data.pop('school_id', None)
        
        # Update school if provided
        if school_id:
            school = get_object_or_404(School, id=school_id)
            instance.school = school
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update teachers
        instance.teachers.clear()
        if teacher_ids:
            teachers = Teacher.objects.filter(id__in=teacher_ids)
            instance.teachers.add(*teachers)
        
        return instance