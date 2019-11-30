from django.shortcuts import render,HttpResponse,render_to_response

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse,redirect
from lawyer.forms import LoginForm,RegisterForm,LawyerForm,Lawyer_EditForm,User_EditForm,Review_lawyer_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lawyer.models import State,Practice_area,Sub_practice_area,Lawyer_practice_area,Lawyer,Review_Lawyer
import csv
from lawyer.decorators import check_recaptcha
from django.db.models import Q,Subquery
from django.db.models import Count,Avg
from django.core.paginator import Paginator
from django.core.mail import get_connection, send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from hashlib import sha1
from django.contrib.auth.hashers import check_password
import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.admin.views.decorators import staff_member_required

# from django.core.mail.message import EmailMessage

# Create your views here.


def index(request):
    ''' Dashboard '''
    lawyer = Lawyer.objects.all()[:9]
    review_lawyer = Review_Lawyer.objects.all()
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    
    return render(request,'client/index.html',{'lawyer':lawyer,'review_lawyer':review_lawyer,'review_count':review_count})


def user_login(request):
    ''' User Login '''
    form = LoginForm()
    msg = ''

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email).username      
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active and user.is_staff:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))

                elif user.is_active and user.is_superuser:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    msg = 'Plz Login First...'
            else:
                msg = "Invalid Login details supplied."
        except:
            msg = "Invalid Login details supplied."

    return render(request,'client/login.html',{'form':form,'msg':msg})


@check_recaptcha
def client_signup(request):
    msg = ''
    form = RegisterForm()
    if request.method == 'POST':
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            if request.recaptcha_is_valid:
                if password == cpassword:
                    user = form.save(commit=False)
                    user.set_password(user.password)
                    user.is_staff = True
                    user.save()
                    return HttpResponseRedirect(reverse('login'))
                else:
                    msg = 'Password and Confirm Passwords Must be same...'
            else:
                msg= 'Invalid reCAPTCHA. Please try again.' 
    return render(request,'client/client_signup.html',{'form':form,'msg':msg})


@login_required(login_url='/login/')
def user_logout(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def view_lawyer(request):
    pname = request.GET['practice_area']
    practice_area1 = Lawyer_practice_area.objects.filter(practice_area__practice=pname)
    page = request.GET.get('page', 1)
    paginator = Paginator(practice_area1, 3)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)

    try:
        practice_area = paginator.page(page)
    except PageNotAnInteger:
        practice_area = paginator.page(1)
    except EmptyPage:
        practice_area = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':practice_area,'sub_practice_area':sub_practice_area,'pname':pname,'review_count':review_count})


@login_required(login_url='/login/')
@check_recaptcha
def send_messages(request):
    if request.method == 'POST':
        lawyer_email = request.POST.get('lawyer_email')
        client_email = request.POST.get('client_email')
       
        password = request.POST.get('password')
        message = request.POST.get('message')

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_USE_TLS = True
        EMAIL_PORT = 587
        EMAIL_HOST_USER = client_email
        EMAIL_HOST_PASSWORD = password
        connection = get_connection(host=EMAIL_HOST, 
                                    port=EMAIL_PORT, 
                                    username=EMAIL_HOST_USER, 
                                    password=EMAIL_HOST_PASSWORD, 
                                    use_tls=EMAIL_USE_TLS) 

        subject = 'Lawyer'
        message = '<h4>'+ message + '</h4>'
        recipient_list = [lawyer_email,]
        send_mail(subject, message, EMAIL_HOST_USER, recipient_list, connection=connection)
        # if request.recaptcha_is_valid:
        # else:
        #     msg= 'Invalid reCAPTCHA. Please try again.'
        #     return render(request, 'client/send_message.html', {'msg':msg})
    else:
        user_id = request.GET.get('user_id')
   
        try:
            lawyer_message = Lawyer.objects.get(user_id=user_id)
            
            return render(request, 'client/send_message.html', {'lawyer_message':lawyer_message})
        except Exception as e:
            print(e)
    return render(request, 'client/send_message.html')



@check_recaptcha
def lawyer(request):
    user_form = RegisterForm()
    lawyer_form = LawyerForm()
    msg = ''
    if request.method == 'POST':
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')
        user_form = RegisterForm(data=request.POST)
        lawyer_form = LawyerForm(request.POST, request.FILES)

        if user_form.is_valid() and lawyer_form.is_valid():
            if request.recaptcha_is_valid:
                if password == cpassword:

                    user = user_form.save(commit=False)
                    user.set_password(user.password)
                    user.is_superuser = True
                    user.save()

                    lawyer = lawyer_form.save(commit=False)
                    lawyer.user = user
                    lawyer.save()
                    return HttpResponseRedirect(reverse('login'))
                else:
                    msg = 'Password and Confirm Passwords Must be same...'
            else:
                msg= 'Invalid reCAPTCHA. Please try again.'
        
    return render(request,'lawyer/lawyer_register.html',{'user_form':user_form,'lawyer_form':lawyer_form,'msg':msg})


def state_data():
    data = State.objects.all()
    if data.count() == 0:
        with open('states.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                s = State(state_name=row['State'])
                s.save()
    return data
state_data()


def subarea_dependent_dropdown(request):
    value = request.GET['value']
    sub_area = Sub_practice_area.objects.filter(practice_id=value)
    return render(request,'lawyer/sub_area.html',{'sub_area':sub_area})


@login_required(login_url='/login/')
def add_practice_area(request):
    practice_area = Practice_area.objects.all()
    sub_practice_area = Sub_practice_area.objects.all()
    if request.method == 'POST':
        uid = request.POST.get('uid')
        pid = request.POST['practice_area']
        sub_practice_area = request.POST.getlist('sub_practice_area')
    
        lawyer = Lawyer.objects.get(user_id=uid)
        practice_area_add = Practice_area.objects.get(id=pid)

        lawyer_practice_area = Lawyer_practice_area.objects.all()

        if lawyer_practice_area.count() == 0:
            lawyer_sub_area = Lawyer_practice_area()
            lawyer_sub_area.lawyer_id=lawyer
            lawyer_sub_area.practice_area = practice_area_add
            lawyer_sub_area.sub_practice_area = sub_practice_area
            lawyer_sub_area.save()
        else:
            if Lawyer_practice_area.objects.filter(practice_area_id=pid,lawyer_id__user_id=uid):
                lawyer_sub_area = Lawyer_practice_area.objects.get(practice_area_id=pid,lawyer_id__user_id=uid)
                lawyer_sub_area.lawyer_id=lawyer
                lawyer_sub_area.practice_area = practice_area_add
                lawyer_sub_area.sub_practice_area = sub_practice_area
                lawyer_sub_area.save()
            else:
                lawyer_sub_area = Lawyer_practice_area()
                lawyer_sub_area.lawyer_id=lawyer
                lawyer_sub_area.practice_area = practice_area_add
                lawyer_sub_area.sub_practice_area = sub_practice_area
                lawyer_sub_area.save()
    return render(request,'lawyer/add_practice_area.html',{'practice_area':practice_area,'sub_practice_area':sub_practice_area})


@login_required(login_url='/login/')
@check_recaptcha
def lawyer_edit_profile(request):
    uid = request.user.id
    user = User.objects.get(id=uid)
    lawyer = Lawyer.objects.get(user_id=uid)

    lawyer_editform = Lawyer_EditForm(instance=lawyer)
    user_editform = User_EditForm(instance=user)
    msg=''

    if request.method == 'POST':
        user_form = User_EditForm(data=request.POST,instance=user)
        lawyer_form = Lawyer_EditForm(request.POST, request.FILES,instance=lawyer)
        if user_form.is_valid() and lawyer_form.is_valid():
            if request.recaptcha_is_valid:
            
                user_edit = user_form.save(commit=False)
                user_edit.save()

                lawyer_edit = lawyer_form.save(commit=False)
                lawyer_edit.user = user
                lawyer_edit.save()
                return HttpResponseRedirect(reverse('lawyer_profile', kwargs={'lid':uid}))
            else:
                msg= 'Invalid reCAPTCHA. Please try again.'
        else:
            msg = 'Form is invalid'
    return render(request,'lawyer/edit_profile.html',{'lawyer_editform':lawyer_editform,'user_editform':user_editform,'msg':msg})


def state_list(request):
    state = State.objects.all()
    return render(request,'client/state.html',{'state':state})

def practice_area_for_state(request):
    state = request.GET['state']
    practice_area = Practice_area.objects.all()
    return render(request,'client/practice_area_for_state.html',{'practice_area':practice_area,'state':state})

def view_lawyer_by_state(request):
    state = request.GET['state']
    practice = request.GET['practice_area']
    
    lawyer_state = State.objects.get(id=state)
    parea = Practice_area.objects.get(practice=practice)
    state_wise_lawyer1 = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,practice_area=parea)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=practice)
    page = request.GET.get('page', 1)
    paginator = Paginator(state_wise_lawyer1, 5)
    try:
        state_wise_lawyer = paginator.page(page)
    except PageNotAnInteger:
        state_wise_lawyer = paginator.page(1)
    except EmptyPage:
        state_wise_lawyer = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':state_wise_lawyer,'review_count':review_count,'pname':practice,'sub_practice_area':sub_practice_area,'state':state,'lawyer_state':lawyer_state})


@login_required(login_url='/login/')
def lawyer_profile(request,lid):
    lawyer1 = Lawyer.objects.get(user_id=lid) 
    lawyer2 = Lawyer_practice_area.objects.filter(lawyer_id__user_id=lid)
    review_lawyer = Review_Lawyer.objects.filter(lawyer_id__user_id=lid).first()
    review_count = Review_Lawyer.objects.filter(lawyer_id__user_id=lid).values('lawyer_id__user_id').annotate(dcount=Count('review'))
    return render(request,'lawyer/lawyer_profile.html',{'lawyer1':lawyer1,'lawyer2':lawyer2,'review_lawyer':review_lawyer,'review_count':review_count})



@login_required(login_url='/login/')
@check_recaptcha
def review_lawyer(request,lid):
    review_form = Review_lawyer_form()
    lawyer1 = Lawyer.objects.get(user_id=lid) 
    lawyer_practicearea = Lawyer_practice_area.objects.filter(lawyer_id__user_id=lid)
    msg = ''
    if request.method == 'POST':
        review_form = Review_lawyer_form(data=request.POST)
        lawyer = Lawyer.objects.get(user_id=request.POST.get('lawyer')) 
        user = User.objects.get(id=request.POST.get('client'))
        try:

            if Review_Lawyer.objects.get(user_id=request.POST.get('client'),lawyer_id__user_id=request.POST.get('lawyer')):
                l = Review_Lawyer.objects.get(user_id=request.POST.get('client'),lawyer_id__user_id=request.POST.get('lawyer'))
                review_form = Review_lawyer_form(request.POST,instance=l)
        except:
            review_form = Review_lawyer_form(data=request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.lawyer_id = lawyer
            review.user = user
            
            if request.recaptcha_is_valid:
                review.save()
                return HttpResponseRedirect(reverse('viewall_review_lawyer', kwargs={'lid':lid}))
            else:
                msg= 'Invalid reCAPTCHA. Please try again.'
    return render(request,'client/review_lawyer.html',{'lawyer1':lawyer1,'lawyer_practicearea':lawyer_practicearea,'review_form':review_form,'msg':msg})


@login_required(login_url='/login/')
def viewall_review_lawyer(request,lid):
    lawyer = Lawyer.objects.get(user_id=lid) 
    review_lawyer = Review_Lawyer.objects.filter(lawyer_id__user_id=lid).order_by('-rating')
    review_count = Review_Lawyer.objects.filter(lawyer_id__user_id=lid).values('lawyer_id__user_id').annotate(dcount=Count('review'))
    page = request.GET.get('page', 1)
    paginator = Paginator(review_lawyer, 5)
    
    try:
        review_lawyer = paginator.page(page)
    except PageNotAnInteger:
        review_lawyer = paginator.page(1)
    except EmptyPage:
        review_lawyer = paginator.page(paginator.num_pages)
    return render(request,'client/viewall_review_lawyer.html',{'lawyer':lawyer,'review_lawyer':review_lawyer,'review_count':review_count})



@login_required(login_url='/login/')
def change_password(request):   
    status =''
    msg = ''
    status = 0
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if check_password(old_password, request.user.password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                status = 1
                msg = 'Password change successfully.. \n You have to login again with new password..'
            else:
                status = 0
                msg = 'Password and Confirm Password must be same..'
        else:
            status = 0
            msg = 'Enter Valid Current Password..'     
    return render(request,'client/change_password.html',{'status':status,'msg':msg})


def fitler_by_subarea_rating_experience(request):
    pname = ''
    sub_area = ''
    rating = ''
    experience_id = ''
    r1 = ''
    r2 = ''
    state = ''
    lawyer_state = ''
    rate1 = ''
    rate2 = ''
    try:
        pname = request.GET['practice_area']
        sub_area = request.GET['sub_area']
        experience_id = request.GET['range']
        rating = request.GET['rating']
        if rating != '0':
            status = 1
        else:
            status = 0
        state = request.GET['state']
        
    except Exception as e:
        print(e)
   
    if state:
        lawyer_state = State.objects.get(id=state)

    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    if experience_id == '>0':
        r1 = 0
        r2 = 100
    elif experience_id == '>20':
        r1 = 20
        r2 = 100
    elif experience_id == '10-20':
        r1 = 10
        r2 = 20
    elif experience_id == '5-10':
        r1 = 5
        r2 = 10
    elif experience_id == '0-5':
        r1 = 0
        r2 = 5

    today = datetime.date.today()
    range1 = (today - relativedelta(years=r1)).year
    range2 = (today - relativedelta(years=r2)).year


    if state:
        if sub_area == 'ALL':
            lawyer_filter_data = Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__state=lawyer_state,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1,lawyer_id__user_id__in=Subquery(Review_Lawyer.objects.filter(rating__gte=rating).values('lawyer_id__user_id')))
        else:
            lawyer_filter_data = Lawyer_practice_area.objects.filter(practice_area__practice=pname,sub_practice_area__contains=sub_area,lawyer_id__state=lawyer_state,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1,lawyer_id__user_id__in=Subquery(Review_Lawyer.objects.filter(rating__gte=rating).values('lawyer_id__user_id')))
    else:
        if sub_area == 'ALL':
            lawyer_filter_data = Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1,lawyer_id__user_id__in=Subquery(Review_Lawyer.objects.all().values('lawyer_id__user_id')))
        else:
            lawyer_filter_data = Lawyer_practice_area.objects.filter(practice_area__practice=pname,sub_practice_area__contains=sub_area,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1,lawyer_id__user_id__in=Subquery(Review_Lawyer.objects.all().values('lawyer_id__user_id')))
          
    if status == 1:
        if rating == '5':
            rate1 = 5.0
            rate2 = 6.0
        elif rating == '4':
            rate1 = 4.0
            rate2 = 5.0
        elif rating == '3':
            rate1 = 3.0
            rate2 = 5.0
        elif rating == '2':
            rate1 = 1.0
            rate2 = 5.0
        elif rating == '1':
            rate1 = 0.0
            rate2 = 5.0
        if state:
            if sub_area == 'ALL':
                lawyer_filter_data = Review_Lawyer.objects.all().filter(lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__state=lawyer_state,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1).values('lawyer_id__user_id'))).values('lawyer_id__user_id','lawyer_id__user__first_name','lawyer_id__user__last_name','lawyer_id__state__state_name','lawyer_id__city','lawyer_id__year_admitted','lawyer_id__address1','lawyer_id__profile_image').annotate(avg=Avg('rating')).filter(avg__gte=rate1,avg__lte=rate2)
            else:
                lawyer_filter_data = Review_Lawyer.objects.all().filter(lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__state=lawyer_state,sub_practice_area__contains=sub_area,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1).values('lawyer_id__user_id'))).values('lawyer_id__user_id','lawyer_id__user__first_name','lawyer_id__user__last_name','lawyer_id__state__state_name','lawyer_id__city','lawyer_id__year_admitted','lawyer_id__address1','lawyer_id__profile_image').annotate(avg=Avg('rating')).filter(avg__gte=rate1,avg__lte=rate2)
        else:
            if sub_area == 'ALL':
                lawyer_filter_data = Review_Lawyer.objects.all().filter(lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1).values('lawyer_id__user_id'))).values('lawyer_id__user_id','lawyer_id__user__first_name','lawyer_id__user__last_name','lawyer_id__state__state_name','lawyer_id__city','lawyer_id__year_admitted','lawyer_id__address1','lawyer_id__profile_image').annotate(avg=Avg('rating')).filter(avg__gte=rate1,avg__lte=rate2)
            else:
                lawyer_filter_data = Review_Lawyer.objects.all().filter(lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname,sub_practice_area__contains=sub_area,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1).values('lawyer_id__user_id'))).values('lawyer_id__user_id','lawyer_id__user__first_name','lawyer_id__user__last_name','lawyer_id__state__state_name','lawyer_id__city','lawyer_id__year_admitted','lawyer_id__address1','lawyer_id__profile_image').annotate(avg=Avg('rating')).filter(avg__gte=rate1,avg__lte=rate2)

      

    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
       
    ############### PAGINATION   ###############
    page = request.GET.get('page',1)
    paginator = Paginator(lawyer_filter_data, 10)
    try:
        lawyer_filter_data = paginator.page(page)
    except PageNotAnInteger:
        lawyer_filter_data = paginator.page(1)
    except EmptyPage:
        lawyer_filter_data = paginator.page(paginator.num_pages)
    ###############   END   ###############
  
    return render(request,'client/view_lawyers.html',{'lawyer':lawyer_filter_data,'pname':pname,'sub_practice_area':sub_practice_area,'sub_area':sub_area,'rating':rating,'experience_id':experience_id,'review_count':review_count,'lawyer_state':lawyer_state,'state':state,'status':status,'rate1':rate1,'rate2':rate2,})


