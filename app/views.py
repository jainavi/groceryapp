from django import http
from django.template import loader
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.db import IntegrityError
from django.http import JsonResponse
from app.models import Customer
from app.models import Item
from app.models import OnlineOrder
from app.models import ForgotPassword
from app.utils import prepare_order_description
import json
import os
import binascii

def index(request):
	return render_to_response("index.html")

def contact(request):
	return render_to_response("contact.html")

@csrf_exempt
def login(request):
	if request.method == 'GET':
		return render(request, "login.html")
	elif request.method == 'POST':
		email = request.POST['email'].strip()
		password = request.POST['password']

		customer = Customer.objects.get(email=email)

		response_data = {
			'status': "OK",
			'errors': [],
			'data': {}
		}

		if customer is None:
			response_data['status'] = 'FAIL'
			response_data['errors'] = 'Invalid email id!'
		elif check_password(password, customer.password) == False:
			response_data['status'] = 'FAIL'
			response_data['errors'] = 'Invalid password!'
		else:
			response_data['data'] = str(customer)

		return JsonResponse(response_data)

	else:
		raise SuspiciousOperation('Bad Request!')

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		response_data = {
			'status': "OK",
			'errors': [],
			'data': {}
		}
		data = request.POST.dict()
		data['password'] = make_password(data['password'])
		customer = Customer(**data)
		customer.clean()
		try:
			customer.save()
		except Exception, e:
			response_data['status'] = 'FAIL'
			response_data['errors'] = [str(e)]
		return JsonResponse(response_data)
	else:
		raise SuspiciousOperation('Bad Request!')

@csrf_exempt
def order(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		order_summary_data = data['order_summary']
		order_description_data = data['order_description']

		if order_summary_data is None or order_description_data is None:
			raise SuspiciousOperation('Bad Request!')

		online_order = OnlineOrder(**order_summary_data)
		online_order.status = str(1)

		if not online_order.check_essentials():
			raise SuspiciousOperation('Bad Request!')

		sequence = 1
		net_bill = 0.00
		order_descriptions = []

		response_data = {
			'status': 'OK',
			'errors': [],
			'data': {}
		}

		for description in order_description_data:
			item = Item.objects.get(pk=description['item_id'])

			if item is None:
				raise SuspiciousOperation(description['item_id'] + ' does not exist!')

			description['item_id'] = item
			order_description = prepare_order_description(description, sequence)
			if order_description is None:
				raise SuspiciousOperation('Bad Request!')

			if item.price != order_description.price or item.discount != order_description.discount:
				response_data['status'] = 'FAIL'
				response_data['errors'].append('Price is not matching for item ' + item.name)
			else:
				net_bill += (item.price - item.discount) * order_description.qty
				order_descriptions.append(order_description)

			sequence += 1

		if net_bill != online_order.net_bill:
			response_data['status'] = 'FAIL'
			response_data['errors'].append('Inconsistency in net bill price!')

		if len(response_data['errors']) == 0:
			try:
				with transaction.atomic():
					online_order.save()
					for order_description in order_descriptions:
						order_description.order_id = online_order
						order_description.save()
			except IntegrityError, e:
				response_data['status'] = 'FAIL'
				response_data['errors'] = [str(e)]

		return JsonResponse(response_data)

@csrf_exempt
def checkout(request):
	if request.method == 'GET':
		return render_to_response("checkout.html")
	elif request.method == 'POST':
		return {}

@csrf_exempt
def trackmyorder(request):
	if request.method == 'GET':
		return render_to_response("trackmyorder.html")
	elif request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))

		customer_email = data['email']
		order_id = data['order_id']

		if customer_email is None or order_id is None:
			raise SuspiciousOperation('Bad Request!')

		response_data = {
			'status': 'OK',
			'errors': [],
			'data': {}
		}

		order = OnlineOrder.objects.filter(id=order_id, customer_email=customer_email).first()
		if order is None:
			response_data['status'] = 'FAIL'
			response_data['errors'] = ['We could not find any order with the above parameters']
		else:
			response_data['data'] = order.as_json()

		return JsonResponse(response_data)

def forgotpassword(request):
	if request.method == 'POST':
		email = request.POST.get('email', "").strip()

		response_data = {
			'status': 'OK',
			'errors': [],
			'data': {}
		}

		if Customer.objects.filter(email=email).exists():
			access_token = str(binascii.hexlify(os.urandom(20)))
			attr = {}
			attr['email'] = email
			attr['access_token'] = access_token
			forgot_password = ForgotPassword(**attr)
			try:
				ForgotPassword.objects.filter(email=email, is_expired=0).update(is_expired=1)
				forgot_password.save()
			except Exception, e:
				response_data['status'] = 'FAIL'
				response_data['errors'] = [str(e)]
		else:
			response_data['status'] = 'FAIL'
			response_data['errors'] = 'You are not registered with us. Please sign up!'

		return JsonResponse(response_data)
	else:
		raise SuspiciousOperation('Bad Request!')
