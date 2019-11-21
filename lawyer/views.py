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

# from django.core.mail.message import EmailMessage

# Create your views here.


def base(request):
    practice = Practice_area.objects.all()
    return render_to_response('client/base.html',{'practice':practice})

def index(request):
    ''' Dashboard '''
    lawyer = Lawyer.objects.all()
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
                    request.session['id'] = user.id
                    return HttpResponseRedirect(reverse('index'))

                elif user.is_active and user.is_superuser:
                    login(request,user)
                    request.session['id'] = user.id
                    return HttpResponseRedirect(reverse('lawyer_edit_profile'))
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
    paginator = Paginator(practice_area1, 5)
    # review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
    #             Lawyer.objects.all().values('user_id')))

    # review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
    #             Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id')))
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)

    try:
        practice_area = paginator.page(page)
    except PageNotAnInteger:
        practice_area = paginator.page(1)
    except EmptyPage:
        practice_area = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':practice_area,'sub_practice_area':sub_practice_area,'pname':pname,'review_count':review_count})



def filter_by_sub_area(request): 
    sub_area = request.GET['sub_area']
    pname = request.GET['practice_area']
    page = request.GET.get('page', 1)
    # review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
    #             Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id'))).count()

    if sub_area == 'all':
        filter_sub_area1 = Lawyer_practice_area.objects.filter(practice_area__practice=pname)
       
    else:
        filter_sub_area1 = Lawyer_practice_area.objects.filter(sub_practice_area__contains=sub_area)
    
    paginator = Paginator(filter_sub_area1, 3)
    try:
        filter_sub_area = paginator.page(page)
    except PageNotAnInteger:
        filter_sub_area = paginator.page(1)
    except EmptyPage:
        filter_sub_area = paginator.page(paginator.num_pages)
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))

    return render(request,'client/view_lawyers.html',{'lawyer':filter_sub_area,'sub_area':sub_area,'pname':pname,'sub_practice_area':sub_practice_area,'review_count':review_count})


@login_required(login_url='/login/')
@check_recaptcha
def send_messages(request):
    if request.method == 'POST':
        lawyer_email = request.POST.get('lawyer_email')
        client_email = request.POST.get('client_email')
        lawyer_first_name = request.POST.get('lawyer_first_name')
        lawyer_last_name = request.POST.get('lawyer_last_name')
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
        message = message
        recipient_list = [lawyer_email,]
        # send_mail(subject, message, EMAIL_HOST_USER, recipient_list, connection=connection)
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
    uid = request.session.get('id')
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
    practice = request.GET['practice']
    
    lawyer_state = State.objects.get(id=state)
    parea = Practice_area.objects.get(practice=practice)
    state_wise_lawyer1 = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,practice_area=parea)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=practice)
    page = request.GET.get('page', 1)
    paginator = Paginator(state_wise_lawyer1, 3)
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




def filter_by_experience(request):
    pname = request.GET['practice_area']
    experience_id = request.GET['range']
   
    r1 = ''
    r2 = ''
    
    if experience_id == '>20':
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

    # lawyer = Lawyer_practice_area.objects.filter(practice_area__practice=pname)

    today = datetime.date.today()
    range1 = (today - relativedelta(years=r1)).year
    range2 = (today - relativedelta(years=r2)).year

    lawyer = Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1)
    page = request.GET.get('page',1)
    paginator = Paginator(lawyer,5)
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    
    try:
        lawyer_experience = paginator.page(page)
    except PageNotAnInteger:
        lawyer_experience = paginator.page(1)
    except EmptyPage:
        lawyer_experience = paginator.page(paginator.num_pages)

    # review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
    #             Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id')))
   
    return render(request,'client/view_lawyers.html',{'lawyer':lawyer_experience,"experience_id":experience_id,'pname':pname,'sub_practice_area':sub_practice_area})


def filter_by_sub_area_state(request): 
    state = request.GET['state']
    sub_area = request.GET['sub_area']
    practice = request.GET['practice_area']
    lawyer_state = State.objects.get(id=state)
    parea = Practice_area.objects.get(practice=practice)
    
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=practice)

    if sub_area == 'all':
        state_wise_lawyer = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,practice_area=parea)
       
    else:
        state_wise_lawyer = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,sub_practice_area__contains=sub_area)
       
    page = request.GET.get('page', 1)
    paginator = Paginator(state_wise_lawyer, 5)
    try:
        state_wise_lawyer = paginator.page(page)
    except PageNotAnInteger:
        state_wise_lawyer = paginator.page(1)
    except EmptyPage:
        state_wise_lawyer = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':state_wise_lawyer,'review_count':review_count,'pname':practice,'sub_practice_area':sub_practice_area,'state':state,'sub_area':sub_area,'lawyer_state':lawyer_state})


def filter_by_experience_state(request):
    pname = request.GET['practice_area']
    state = request.GET['state']
    experience_id = request.GET['range']
    lawyer_state = State.objects.get(id=state)
    parea = Practice_area.objects.get(practice=pname)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    r1 = ''
    r2 = ''
    
    if experience_id == '>20':
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

    lawyer = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,practice_area__practice=pname,lawyer_id__year_admitted__gte=range2,lawyer_id__year_admitted__lte=range1)
    page = request.GET.get('page',1)
    paginator = Paginator(lawyer,5)
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    
    try:
        lawyer_experience = paginator.page(page)
    except PageNotAnInteger:
        lawyer_experience = paginator.page(1)
    except EmptyPage:
        lawyer_experience = paginator.page(paginator.num_pages)

    # review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
    #             Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id')))
   
    return render(request,'client/view_lawyers.html',{'lawyer':lawyer_experience,"experience_id":experience_id,'state':state,'pname':pname,'sub_practice_area':sub_practice_area,'review_count':review_count,'r1':r1,'r2':r2,'lawyer_state':lawyer_state})


def filter_by_rating(request):
    pname = request.GET['practice_area']
    rating = request.GET['rating']

    lawyer_rating_wise_unique = Review_Lawyer.objects.filter(rating__gte=rating,lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id'))).order_by('-rating')
    
    lawyer_rating_wise = []
    lawyer_exists_ids = []
  
    for item in lawyer_rating_wise_unique:
        if item.lawyer_id.user_id not in lawyer_exists_ids:
            lawyer_rating_wise.append(item)
            lawyer_exists_ids.append(item.lawyer_id.user_id)
  
    
    page = request.GET.get('page',1)
    paginator = Paginator(lawyer_rating_wise,5)
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    try:
        lawyer_rating_wise = paginator.page(page)
    except PageNotAnInteger:
        lawyer_rating_wise = paginator.page(1)
    except EmptyPage:
        lawyer_rating_wise = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':lawyer_rating_wise,'pname':pname,'sub_practice_area':sub_practice_area,'review_count':review_count,'rating':rating})


def filter_by_rating_state(request):
    pname = request.GET['practice_area']
    rating = request.GET['rating']
    state = request.GET['state']
    lawyer_state = State.objects.get(id=state)
    lawyer_rating_wise_unique = Review_Lawyer.objects.filter(rating__gte=rating,lawyer_id__user_id__in=Subquery(Lawyer_practice_area.objects.filter(practice_area__practice=pname,lawyer_id__state=state).values('lawyer_id__user_id'))).order_by('-rating')
    
    lawyer_rating_wise = []
    lawyer_exists_ids = []
  

    for item in lawyer_rating_wise_unique:
        if item.lawyer_id.user_id not in lawyer_exists_ids:
            lawyer_rating_wise.append(item)
            lawyer_exists_ids.append(item.lawyer_id.user_id)

    page = request.GET.get('page',1)
    paginator = Paginator(lawyer_rating_wise,5)
    
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)
    review_count = Review_Lawyer.objects.values('lawyer_id__user_id').annotate(dcount=Count('review'))
    try:
        lawyer_rating_wise = paginator.page(page)
    except PageNotAnInteger:
        lawyer_rating_wise = paginator.page(1)
    except EmptyPage:
        lawyer_rating_wise = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'lawyer':lawyer_rating_wise,'pname':pname,'sub_practice_area':sub_practice_area,'review_count':review_count,'rating':rating,'state':state,'lawyer_state':lawyer_state})


@login_required(login_url='/login/')
def change_password(request):   
    status =''
    mag = ''
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if check_password(old_password, request.user.password):
            if new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
            else:
                msg = 'Password and Confirm Password must be same..'
        else:
            msg = 'Enter Valid Old Password..'     
    return render(request,'client/change_password.html')

