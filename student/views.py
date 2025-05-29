from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from student.forms import Registration, New_Profile_form,forget_password_form
from student.models import Profile, New_Profile, WorkLog
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password,check_password
import random
def home(req):
    return render(req, 'student/home.html')
def register(req):
    if req.method == 'POST':
        form = Registration(req.POST)
        if form.is_valid():
            nm = form.cleaned_data['name']
            em = form.cleaned_data['email']
            pw = form.cleaned_data['password']

            # Try to match a user exactly
            matched_user = Profile.objects.filter(name=nm, email=em).first()
            if matched_user and check_password(pw,matched_user.password):
                req.session['employee_id']=matched_user.id
                return redirect('work_board')  # Insecure: better to use ID or session
            else:
                alert = "You are not an employee"
                return render(req, 'student/register.html', {'form': form, 'alert': alert})
    else:
        form = Registration()

    return render(req, 'student/register.html', {'form': form})


def reg_success(req):
    return render(req, 'student/success.html')


def new_login(req):
    if req.method == 'POST':
        form = New_Profile_form(req.POST, req.FILES)
        if form.is_valid():
            nm = form.cleaned_data['name']
            em = form.cleaned_data['email']
            pw = make_password(form.cleaned_data['password'])
            res_file = form.cleaned_data['resume_file']
            im_file = form.cleaned_data['image_file']

            New_Profile.objects.create(
                name=nm,
                email=em,
                password=pw,
                resume_file=res_file,
                image_file=im_file,
            )
            Profile.objects.create(
                name=nm,
                email=em,
                password=pw,
            )
            send_mail(
                subject='Registration Successful',
                message=f'Hi {nm},\n\nThank you for registering. Your account has been created successfully!',
                from_email='your_email@gmail.com',   # Same as EMAIL_HOST_USER
                recipient_list=[em],
                fail_silently=False,
            )
            return HttpResponseRedirect('/student/register/')
            # return HttpResponseRedirect('/student/thanks/')
    else:
        form = New_Profile_form()

    return render(req, 'student/new_login.html', {'form': form})


def thanks(req):
    return render(req, 'student/thanks.html')


def work_board(req):
    employee_id = req.session.get('employee_id')

    if not employee_id:
        return HttpResponse("Please login first", status=401)

    try:
        employee = Profile.objects.get(id=employee_id)
    except Profile.DoesNotExist:
        return HttpResponse("Invalid employee credentials", status=404)

    today = timezone.now().date()
    log, _ = WorkLog.objects.get_or_create(employee=employee, date=today)

    if req.method == 'POST':
        log.morning_work = req.POST.get('morning_work', log.morning_work)
        log.evening_work = req.POST.get('evening_work', log.evening_work)
        log.save()
        return redirect('work_board')  # No need for args

    return render(req, 'student/work_board.html', {
        'employee': employee,
        'log': log,
    })
def forget_password(req):
    if req.method == 'POST':
        form = forget_password_form(req.POST)
        if form.is_valid():
            nm = form.cleaned_data['name']
            em = form.cleaned_data['email']
            # pw = form.cleaned_data['password']

            # Try to match a user exactly
            matched_user = Profile.objects.filter(name=nm, email=em).first()
            
            if matched_user :
                num=random.randint(0,100)
                send_mail(
                subject='Registration Successful',
                message=f'Hi {nm}, Your new password is {num} \n\nThank you for registering. Your account has been created successfully!',
                from_email='your_email@gmail.com',   # Same as EMAIL_HOST_USER
                recipient_list=[em],
                fail_silently=False,
                )
                obj=Profile.objects.get(name=nm,email=em)
                obj.password=make_password(str(num))
                obj.save()
                return HttpResponseRedirect('/student/register/')
                # req.session['employee_id']=matched_user.id
                # return redirect('work_board')  # Insecure: better to use ID or session
            else:
                alert = "Please enter your correct name and email"
                return render(req, 'student/forget_password_file.html', {'form': form, 'alert': alert})
    else:
        form = forget_password_form()

    return render(req, 'student/forget_password_file.html', {'form': form})

