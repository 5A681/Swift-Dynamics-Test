from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    shotname = models.CharField(max_length=100)
    address = models.TextField()
    class Meta:
        db_table = 'school'

class Class(models.Model):
    grade = models.IntegerField()
    room = models.IntegerField()
    teachers = models.ManyToManyField('Teacher', related_name='classes')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'class'
        verbose_name_plural = 'classes'

class Student(models.Model):
    gender_type = (
        (1,"male"),
        (2,"female"),
        (3,"other")
    )
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    gender = models.IntegerField(choices=gender_type,default=3)
    schoolclass = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)


    class Meta:
        db_table = 'student'

class Teacher(models.Model):
    gender_type = (
        (1,"male"),
        (2,"female"),
        (3,"other")
    )
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    gender = models.IntegerField(choices=gender_type,default=3)

    class Meta:
        db_table = 'teacher'

    

