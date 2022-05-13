from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from login_page.models import Q_A, multiple_choices, interview_info
import random
from django.contrib.auth.decorators import login_required
import pytz


lst = []
q_id_to_skip = []
dificulty_level_ = 1
score = 0
quiestion_number = 1
correct_answers_qty = 0
max_dificulty_level = list(Q_A.objects.raw("SELECT *, max(dificulty_level) FROM Q_A;"))[0].dificulty_level

# def index(request):
#     return HttpResponse("<h1>Login page</h1>")

# def index(request):
# 	print(".............. questions.index called")
# 	return render(request, 'questions/q_page.html', {"name" : "Amir"})

# def auth(request):
# 	print(".............. questions.auth called")
# 	auth_result = authenticaion(request)
# 	if auth_result:
# 		next_quest(request)

# def tr(request):
# 	return HttpResponse("<h1>TR</h1>")


def get_multiple_choices(q_id):	
	print(".............. questions.get_multiple_choices called")
	raw_query = f"SELECT * FROM multiple_choices WHERE Q_id = '{q_id}'"
	x = list(multiple_choices.objects.raw(raw_query))
	options = [i.option for i in x]
	return options

def next_quest_2(selected_option, q_id):
	global dificulty_level_
	global score
	global quiestion_number
	global correct_answers_qty
	import datetime as dt_
	# lst.append([q_id, selected_option, dt_.datetime.now(), dificulty_level_])
	lst.append([q_id, selected_option, dt_.datetime.now(pytz.timezone('Asia/Karachi')), dificulty_level_])

	q_id_to_skip.append(q_id)

	x = Q_A.objects.raw(f"select * from Q_A where id = '{q_id}'")
	id_, Q, A, dificulty_level = [(i.id, i.Q, i.A, i.dificulty_level) for i in x][0]
	quiestion_number += 1
	# print(f"q_id: {q_id}\nid_: {id_}\nQ: {Q}\nA: {A}\ndificulty_level: {dificulty_level}")
	if A == selected_option:
		correct_answers_qty += 1
		score += dificulty_level_
		if dificulty_level_ < max_dificulty_level:
			dificulty_level_ += 1
	else:
		if dificulty_level_ > 1:
			dificulty_level_ -= 1 
	lst[-1].append(score)
	while True:
		raw_query = f"select * from Q_A WHERE dificulty_level = '{dificulty_level_}' AND id NOT IN {str(tuple(q_id_to_skip)).replace(',)', ')')};"
		x = list(Q_A.objects.raw(raw_query))
		random.shuffle(x)
		if len(x) > 0:
			q_id, question, answer, dificulty_level =  x[0].id, x[0].Q, x[0].A, x[0].dificulty_level
			break
		else:
			return "Questions ended in DB"

	params_ = {
			"score" : score,
			"quiestion_number" : quiestion_number,
			'Question' : question, 
			"answer" : answer,
			"q_id" : q_id,
			"dificulty_level" : dificulty_level,
			"correct_answers_qty" : correct_answers_qty,
			"L" : get_multiple_choices(q_id)
			}
	return params_


@login_required
def thank_you(request):
	user_name = request.user
	from django.contrib.auth import logout
	logout(request)
	log_interview(request, quiestion_number, correct_answers_qty, score, lst, 'loged out', user_name=user_name)
	return render(request, 'questions/thank_you.html')

def next_quest(request):
	print(".............. questions.next_quest called")
	try:
		selected_option = request.POST["selected_option"]
		q_id = request.POST["custId"]
	except:
		return HttpResponse("<h1>No option selected</h1>")
	
	params_ = next_quest_2(selected_option, q_id)
	if params_ == "ERROR":
		return render(request, 'questions/thank_you.html')
	return render(request, 'questions/q_page.html', params_)
	# else:
		# return HttpResponse("<h1>Incorrect email or password</h1>")

@login_required
def create_post(request):
	print("#################################### 1")
	print("\n.............. questions.create_post called")
	global dificulty_level_
	global score
	global quiestion_number
	global correct_answers_qty
	import json
	if request.is_ajax():
		print("#################################### 2")
		try:
			if str(request.POST['time_out']) == "true":
				params_ = 'Time out'
		except:
			selected_option = request.POST["selected_option"]
			q_id = request.POST["q_id"] #custId
			params_ = next_quest_2(selected_option, q_id)

		if isinstance(params_, dict):
			print("#################################### 3")
			params_['sucess'] = "True"
		else:
			if params_ == "Questions ended in DB":
				print("#################################### 4")
				log_interview(request, quiestion_number, correct_answers_qty, score, lst, 'Questions ended in DB')
				params_ = {"sucess" : "False"}
				# interview khatam hony par ye log karna h, magar interview khatam hony ka ye 1 synario h (k questions ki qty baqi ho magar ksi bhi 1 dificulty level k sary question ho gay hon)
				# user khud logout kar day      ?????????? is ki impelementation baqi h
			elif (quiestion_number > 20):
				print("#################################### 5")
				log_interview(request, quiestion_number, correct_answers_qty, score, lst, 'Questions ended')
				params_ = {"sucess" : "False"}
			elif params_ == 'Time out':
				log_interview(request, quiestion_number, correct_answers_qty, score, lst, 'Time out')
				params_ = {"sucess" : "False"}
			# return HttpResponse("<h1>No question left</h1>")\
			# redirect("http://127.0.0.1:8000/accounts/login/")
			# return JsonResponse({})
			# return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}),content_type="application/json")
			# return render(request, template_name="No_question_left.html")
		# print (json.dumps(params_, indent=2, default=str))
		# {'score': 0, 'quiestion_number': 7, 'Question': 'Question 11', 'answer': 'Answer 11', 'q_id': 11, 'dificulty_level': 1, 'correct_answers_qty': 0, 'L': ['Answer 11', 'b', 'p', 'x']}
		# return HttpResponse(json.dumps(params_),content_type="application/json")
		# print(params_)
		print("#################################### 6")
		return JsonResponse(params_)
		# return redirect('account') # path('account/', views.userAccount, name="account"),

		# return HttpResponse("<h1>No option selected</h1>")

		# if selected_option and q_id: #cheking if first_name and last_name have value
		# 	response = {'msg':'Your form has been submitted successfully'} # response message}
		# 	return JsonResponse(response) # return response as JSON




def log_interview(request, quiestion_number, correct_answers_qty, score, lst, ending_reason, user_name=None):
	from login_page.models import Q_A, multiple_choices, interview_logs, interview_info
	import datetime
	from django.contrib.auth.models import User 
	if user_name is None:
		user_id = User.objects.get(username=request.user).id 
	else:
		user_id = User.objects.get(username=user_name   ).id
	total_questions = 20 # hard coded, should be replaced
	
	start_time = open("start_time.txt", 'r').read().strip()
	start_time = datetime.datetime.fromisoformat(start_time)

	# end_time = datetime.datetime.now()
	end_time = datetime.datetime.now(pytz.timezone('Asia/Karachi'))
	time_spent_in_minutes = (end_time - start_time).total_seconds() // 60

	incorrect_answers_qty = quiestion_number - correct_answers_qty

	interview_info.objects.create(
		user_id = user_id,
		start_time = str(start_time),
		time_spent_in_minutes = time_spent_in_minutes,
		correct_answers_qty = correct_answers_qty,
		incorrect_answers_qty = incorrect_answers_qty,
		total_questions = total_questions,
		time_provided_in_minutes = 20,
		score = score,
		is_completed_all_questions = (1 if (correct_answers_qty + incorrect_answers_qty) == total_questions else 0),
		ending_reason = ending_reason
		).save()

	from django.core.mail import send_mail
	from interview_app.settings import EMAIL_HOST_USER
	subject = "Subject"
	message = "Message"
	if user_name is None:
		recepient = User.objects.get(username=request.user).email
	else:
		recepient = User.objects.get(username=user_name   ).email
	send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)

	for e, i in enumerate(lst):
		Q_id, selected_option, time_, dificulty_level_, score = i
		Q_id = int(Q_id)
		q = Q_A.objects.get(id=Q_id)
		Q = q.Q
		A = q.A

		interview_logs.objects.create(
			# interview_id = interview_info.objects.get(user_id=user_id).id,
			interview_id = interview_info.objects.filter(user_id=user_id).last().id,
			user_id = user_id,
			Question_number = e,
			Q_id = Q_id,
			time = time_,
			Question = Q,
			dificulty_level = dificulty_level_,
			Selected_option = selected_option,
			is_correct = (A == selected_option),
			Options = '|  ' + '\n|  '.join([f"{e}- {i.option}" for e,i in enumerate(multiple_choices.objects.filter(Q_id=Q_id), 1)]),
			Correct_answer = A,
			score = score
			).save()




