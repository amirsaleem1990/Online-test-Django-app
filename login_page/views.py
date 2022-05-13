from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Q_A, multiple_choices
import random
from questions.views import next_quest as next_quest_question
import datetime as dt
from django.contrib.auth.decorators import login_required
import pytz

@login_required
def dashboard(request):
	print('................ login_page.dashboard called')
	
	# open("start_time.txt", 'w').write(str(dt.datetime.now()))
	open("start_time.txt", 'w').write(
		str(dt.datetime.now(pytz.timezone('Asia/Karachi')))
		)
	# try:
		# selected_option = request.POST["selected_option"]
		# q_id = request.POST["custId"]
		# print(request.POST)
		# print(f"\n\n\n--------------------------------{selected_option}\t{q_id}")
	# except:
		# print("----------------EEEEEEEEE")
		# pass
	params_ = next_quest(request)
	return render(request, 'questions/q_page.html', params_)

def index_2(request):
	print("................. login_page.index_2 called")
	return render(request, 'login_page/index.html')

def get_multiple_choices(q_id):	
	print(".............. login_page.get_multiple_choices called")
	raw_query = f"SELECT * FROM multiple_choices WHERE Q_id = '{q_id}'"
	x = list(multiple_choices.objects.raw(raw_query))
	options = [i.option for i in x]
	return options

def next_quest(request):
	# if dict(request.POST).get("selected_option") != None:
	print("................... login_page.next_quest called")
	raw_query = "SELECT * FROM Q_A WHERE dificulty_level = '1'"
	x = list(Q_A.objects.raw(raw_query))
	random.shuffle(x)
	q_id, question, answer, dificulty_level =  x[0].id, x[0].Q, x[0].A, x[0].dificulty_level
	params_ = {
		"score" : 0,
		"quiestion_number" : 1,
		'Question' : question, 
		"answer" : answer, # it is dangoures
		"q_id" : q_id,
		"dificulty_level" : dificulty_level,
		"correct_answers_qty" : 0,
		"L" : get_multiple_choices(q_id)
		}
	return params_




# -----------------------
# https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):    
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get('REMOTE_ADDR')

    log.debug('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs): 
    ip = request.META.get('REMOTE_ADDR')

    log.debug('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))

@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    log.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))
# ----------------------------