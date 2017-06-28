# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt, datetime

# Create your models here.
#------------------------------------User & Manager--------------------------
class UserManager(models.Manager):
	def register(self, data):
		errors = []
		name = data['name']
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		for item in data:
			if len(data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		if len(data['name']) < 3:
			errors.append("Name must be at least 3 characters long")
		if any (x.isalpha() for x in name) and any(x.isspace() for x in name):
			pass
		else:
			errors.append("Name can only contain letters and spaces")
		if len(data['username']) < 3:
			errors.append("Username must be at least 3 characters long")
		try:
			User.objects.get(username = data['username'])
			errors.append("That username is already taken")
		except:
			pass
		if len(data['password']) < 8:
			errors.append("Password must be at least 8 characters long")
		elif data['password'] != data['pw_confirm']:
			errors.append("Passwords don't match!")
		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(name=data['name'], username=data['username'], password=hashed_pw)
			return user
		else:
			return errors

	def login(self, data):
		errors = []
		for item in data:
			if len(data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		try:
			user = User.objects.get(username = data['username'])
		except:
			errors.append("Username not found")
			return errors
		if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password:
			pass
		else:
			errors.append("Incorrect password")
		if len(errors) == 0:
			return user
		else:
			return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.username

	objects = UserManager()

#------------------------------------Trip & Manager--------------------------
class TripManager(models.Manager):
	def trip_validate(self, data, user):
		today = datetime.datetime.now()
		errors = []
		for item in data:
			if len(data[item]) < 1:
				errors.append(item.replace("_", " ").title() + " is a required field")
		try:
			if datetime.datetime.strptime(data['departure_date'], "%Y-%m-%d") < today:
				errors.append("Departure Date must be in the future.")
		except:
			pass
		if data['departure_date'] > data['return_date']:
			errors.append('Departure Date must be before Return Date:')
		if len(errors) > 0:
			return errors
		else:
			new_trip = Trip.objects.create(destination=data['destination'], description=data['description'], departure_date=data['departure_date'], return_date=data['return_date'], created_by=user)
			return new_trip


class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField()
	departure_date = models.DateField()
	return_date = models.DateField()
	created_by = models.ForeignKey(User, related_name='trips_created')
	joined_users = models.ManyToManyField(User, related_name='trips_joined')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.destination

	objects=TripManager()
