from __future__ import unicode_literals

from django.db import models

class Professions(models.Model):
	grade = models.IntegerField()
	college = models.CharField(max_length=100)
	profession = models.CharField(max_length=100)
	def __unicode__(self):
		return str(grade) + college + " " + profession

class Plan(models.Model):
	professionId = models.IntegerField()
	publicRequired = models.FloatField()
	professionalRequired = models.FloatField()
	elective = models.FloatField()
	professionalElective = models.FloatField()
	artsStream = models.FloatField(null=True, blank=True)
	scienceStream = models.FloatField(null=True, blank=True)
	practice = models.FloatField()

class Courses(models.Model):
	professionId = models.IntegerField()
	courseNum = models.CharField(max_length=50)
	courseName = models.CharField(max_length=200)
	courseNameEN = models.CharField(max_length=200)
	courseType = models.CharField(max_length=50)
	credit = models.FloatField()
	suggestion = models.IntegerField()
	creditType = models.CharField(max_length=10)
	remark = models.CharField(max_length=300)

class MCCourses(models.Model):
	courseNum = models.CharField(max_length=100)
	courseName = models.CharField(max_length=200)
	credit = models.FloatField()
	creditType = models.CharField(max_length=10)
	remark = models.CharField(max_length=300)