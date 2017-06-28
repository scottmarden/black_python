# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import User, Trip

# Create your views here.
#-------------------------------Login, Registration & Logout--------------------------
def index(request):
	if 'user_id' in request.session:
		return redirect ('/travels')
	return render(request, 'belt/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['username'] = result.username
		return redirect('/travels')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['username'] = result.username
		return redirect('/travels')

def logout(request):
	request.session.flush()
	return redirect('/')

#-------------------------------Homepage/Dashboard----------------------------------
def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	context = {
		'my_trips': Trip.objects.filter(Q(created_by__id=request.session['user_id']) | Q(joined_users__id=request.session['user_id'])),
		'other_trips': Trip.objects.exclude(Q(created_by__id=request.session['user_id'])| Q(joined_users__id=request.session['user_id'])),
	}
	return render(request, 'belt/travels.html', context)

#-------------------------------Adding Trips----------------------------------
def add_trip(request):
	return render(request, 'belt/add_trip.html')

def new_trip(request):
	user = User.objects.get(id=request.session['user_id'])
	result = Trip.objects.trip_validate(request.POST, user)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/travels/add')
	else:
		return redirect('/travels')

def join_trip(request):
	user = User.objects.get(id=request.session['user_id'])
	trip = Trip.objects.get(id=request.POST['trip_id'])
	trip.joined_users.add(user)
	return redirect('/travels')

#-------------------------------Adding Trips----------------------------------
def trip_details(request, id):
	trip = Trip.objects.get(id=id)
	context = {
		'trip': trip,
		'other_users': trip.joined_users.all()
	}
	return render(request, 'belt/destination.html', context)
