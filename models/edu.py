from django.db import models
from mongoengine import *

connect('lcdb',host='127.0.0.1',port=27017)


class Grade(Document):
        meta = {'collection':'grade'}

        _id = StringField()
        id = StringField(max_length=4)
        label = StringField(max_length=20)

class WaUsers(Document):
	
	meta = {'collection':'waUsers'}
	_id = StringField()
	id = StringField(max_length=20)
	name = StringField(max_length=30)
	age = StringField(max_length=3)
	nickname = StringField(max_length=30)
	#grade reference
	grade = ReferenceField('Grade')


class Subject(Document):
	meta = {'collection':'subject'}

	_id = StringField()
	id = StringField(max_length=4)
	label = StringField(max_length=20)
	
	
class QuestionType(Document):
	meta = {'collection':'questionType'}

	_id = StringField()
	id = StringField(max_length=4)
	label = StringField(max_length=30)


class Question(Document):
	meta = {'collection':'question','strict':False}

	_id = StringField()
	id = StringField(max_length=30)
	label = StringField(max_length=120)
	answera = StringField(max_length=45)
	answerb = StringField(max_length=45)
	answerc = StringField(max_length=45)
	answerd = StringField(max_length=45)

	answer = StringField(max_length=45)

	questionType = ReferenceField(QuestionType)


class Test(Document):
	meta = {'collection':'test'}

	_id = StringField()
	id = StringField(max_length=30)
	label = StringField(max_length=30)
	#waUser
	waUsers = ReferenceField('WaUsers')
	totalScore = IntField()
	totalIndex = IntField()

class TestDetails(Document):
	meta = {'collection':'testDetails'}

	_id = StringField()
	#test
	test = ReferenceField('Test')
	index = IntField()
	question = ReferenceField('Question')
	totalScore = IntField()
	infaceScore = IntField()
	

class User(Document):
	meta = {'collection':'User','strict':False}
	name = StringField()

class Page(Document):
	meta = {'collection':'Page','strict':False}
	content = StringField()
	author = ReferenceField(User)


