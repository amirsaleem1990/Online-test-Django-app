from django.db import models
# from countdowntimer_model.models import CountdownTimer


# class DoomsdayCountdownTimer(CountdownTimer):
#     duration_in_minutes = models.IntegerField();
#     state


class multiple_choices(models.Model):
    Q_id   = models.IntegerField()
    option = models.TextField(max_length=255)
    class Meta:
        db_table = "multiple_choices"

class Q_A(models.Model):
    Q = models.TextField(max_length=255)
    A = models.TextField(max_length=255)
    dificulty_level = models.IntegerField()
    class Meta:
        db_table = "Q_A"
# class users(models.Model):
#     name          = models.TextField(max_length=255)
#     email_address = models.TextField(max_length=255)
#     password      = models.TextField(max_length=255)
#     class Meta:
#         db_table = "users"

class interview_info(models.Model):
    user_id                    = models.IntegerField()
    start_time                 = models.TextField(max_length=255)
    time_spent_in_minutes      = models.IntegerField()
    correct_answers_qty        = models.IntegerField()
    incorrect_answers_qty      = models.IntegerField()
    total_questions            = models.IntegerField()
    time_provided_in_minutes   = models.IntegerField()
    score                      = models.IntegerField()
    is_completed_all_questions = models.IntegerField()
    ending_reason              = models.TextField(max_length=255)
    class Meta:
        db_table = "interview_info"


class interview_logs(models.Model):
    interview_id  = models.IntegerField()
    user_id = models.IntegerField()
    Question_number = models.IntegerField()
    Q_id  = models.IntegerField()
    time = models.TextField(max_length=255)
    Question = models.TextField(max_length=255)
    dificulty_level = models.IntegerField()
    Selected_option = models.TextField(max_length=255)
    is_correct = models.BooleanField()
    Options = models.TextField(max_length=255)
    Correct_answer = models.TextField(max_length=255)
    score = models.IntegerField()
    class Meta:
        db_table = "interview_logs"


# -----------------------
# https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django

from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    time = models.TextField(max_length=250)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    import datetime
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username, time=str(datetime.datetime.now()))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    import datetime
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username, time=str(datetime.datetime.now()))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    import datetime
    AuditEntry.objects.create(action='user_login_failed', username=credentials.get('username', None), time=str(datetime.datetime.now()))
# -----------------------