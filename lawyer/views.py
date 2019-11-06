from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from lawyer.forms import LoginForm,RegisterForm,LawyerForm,Lawyer_EditForm,User_EditForm,Review_lawyer_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lawyer.models import State,Practice_area,Sub_practice_area,Lawyer_practice_area,Lawyer,Review_Lawyer
import csv
from lawyer.decorators import check_recaptcha
from django.db.models import Q,Subquery
from django.db.models import Count
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    lawyer = Lawyer.objects.all()
    review_lawyer = Review_Lawyer.objects.all()
    # list1 = []
    # for r in review_lawyer:
       
    #     for l in lawyer:
    #         if r.lawyer_id.user.id == l.user.id:
    #             if r.lawyer_id.user.id not in list1:
                    

    # print(list1)
    
    return render(request,'client/index.html',{'lawyer':lawyer,'review_lawyer':review_lawyer})


def user_login(request):
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
                msg = "Invalid login details supplied."
        except:
            msg = "Invalid login details supplied."

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


def user_logout(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def view_lawyer(request):
    pname = request.GET['practice_area']
    practice_area1 = Lawyer_practice_area.objects.filter(practice_area__practice=pname)
    page = request.GET.get('page', 1)
    paginator = Paginator(practice_area1, 3)
    review = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
                Lawyer.objects.all().values('user_id')))

    review1 = Review_Lawyer.objects.filter(lawyer_id__user_id__in=Subquery(
                Lawyer_practice_area.objects.filter(practice_area__practice=pname).values('lawyer_id__user_id')))
    print(review1)
    sub_practice_area = Sub_practice_area.objects.filter(practice_id__practice=pname)

    try:
        practice_area = paginator.page(page)
    except PageNotAnInteger:
        practice_area = paginator.page(1)
    except EmptyPage:
        practice_area = paginator.page(paginator.num_pages)
    return render(request,'client/view_lawyers.html',{'practice_area':practice_area,'sub_practice_area':sub_practice_area,'pname':pname,'review':review})


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

#Update Code
# def dropdown(request):
#     sarea2=''
#     if request.method == 'POST':
#         uid = request.POST.get('uid')
        
#         pid = request.POST.get('practice_area')
#         # select = request.POST.getlist('sub_area')
#         select = request.POST.getlist('sub_area[]')
#         ganga = request.POST.getlist('area')
#         print('--- Ganga ---',ganga)
#         # u = User.objects.get(id=uid)
#         # s = Lawyer.objects.get(user_id=uid)

    
#         sarea = request.POST['s_area']
#         print(sarea)
#         # sarea2 = Lawyer_practice_area.objects.filter(lawyer_id__user=uid)
#         sarea2 = Lawyer_practice_area.objects.filter(sub_practice_area__contains=sarea)
#         print(sarea2)
#     srea = Sub_practice_area.objects.all()
#     practice = Practice_area.objects.all()
#     return render(request,'lawyer/dropdown.html',{'practice':practice,'sarea':srea,'sarea2':sarea2})


def subarea_dependent_dropdown(request):
    value = request.GET['value']
    sub_area = Sub_practice_area.objects.filter(practice_id=value)
    return render(request,'lawyer/sub_area.html',{'sub_area':sub_area})



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
    state1 = State.objects.all().order_by('state_name')[1:12]
    state2 = State.objects.all().order_by('state_name')[13:24]
    state3 = State.objects.all().order_by('state_name')[25:]
    return render(request,'client/state.html',{'state1':state1,'state2':state2,'state3':state3})

def practice_area_for_state(request):
    state = request.GET['state']
    practice_area = Practice_area.objects.all()
    return render(request,'client/practice_area_for_state.html',{'practice_area':practice_area,'state':state})

def view_lawyer_by_state(request):
    state = request.GET['state']
    practice_id = request.GET['pid']
   

    lawyer_state = State.objects.get(id=state)
    parea = Practice_area.objects.get(id=practice_id)
    state_wise_lawyer = Lawyer_practice_area.objects.filter(lawyer_id__state=lawyer_state,practice_area=parea)
    return render(request,'client/view_lawyer_by_state.html',{'state_wise_lawyer':state_wise_lawyer})


def lawyer_profile(request,lid):
    lawyer1 = Lawyer.objects.get(user_id=lid) 
    lawyer2 = Lawyer_practice_area.objects.filter(lawyer_id__user_id=lid)
    return render(request,'lawyer/lawyer_profile.html',{'lawyer1':lawyer1,'lawyer2':lawyer2})

def filter_by_sub_area(request):
    sub_area = request.GET['value']
    page = request.GET.get('page', 1)
    pname = request.GET['practice_area']
    review = Review_Lawyer.objects.filter(practice_area__practice=pname,lawyer_id__user_id__in=Subquery(
                Lawyer.objects.all().values('user_id')))
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
    return render(request,'client/filter_by_sub_area.html',{'practice_area':filter_sub_area,'sub_area':sub_area,'pname':pname,'review':review})


# def paginator_page(request):
    # sub_area = request.GET['value']
    # pname = request.GET['practice_area']
 
    # if sub_area == 'all':
    #     practice_area1 = Lawyer_practice_area.objects.filter(practice_area__practice=pname)
    # else:
    #     practice_area1 = Lawyer_practice_area.objects.filter(sub_practice_area__contains=sub_area)
       
    # paginator = Paginator(practice_area1, 3)
    # page = request.GET.get('page', 1)
    
    # try:
    #     practice_area = paginator.page(page)
    # except PageNotAnInteger:
    #     practice_area = paginator.page(1)
    # except EmptyPage:
    #     practice_area = paginator.page(paginator.num_pages)
    # return render(request,'client/paginator_page.html',{'sub_area':sub_area,'practice_area':practice_area})

# @check_recaptcha
def review_lawyer(request,lid):
    review_form = Review_lawyer_form()
    lawyer1 = Lawyer.objects.get(user_id=lid) 
    msg = ''
    if request.method == 'POST':
        print(request.POST.get('lawyer'))
        review_form = Review_lawyer_form(data=request.POST)
        lawyer = Lawyer.objects.get(user_id=request.POST.get('lawyer')) 
        user = User.objects.get(id=request.POST.get('client'))
        try:

            if Review_Lawyer.objects.get(user_id=request.POST.get('client')):
                l = Review_Lawyer.objects.get(user_id=request.POST.get('client'))
                review_form = Review_lawyer_form(request.POST,instance=l)
        except:
            review_form = Review_lawyer_form(data=request.POST)

        if review_form.is_valid():
            print('-- yes---')
            review = review_form.save(commit=False)
            review.lawyer_id = lawyer
            review.user = user


        
        # if review_form.is_valid():
        #     review = review_form.save(commit=False)
        #     review.lawyer_id = lawyer
        #     review.user = user

            if request.recaptcha_is_valid:
                review.save()
                return HttpResponseRedirect(reverse('viewall_review_lawyer'))
            else:
                msg= 'Invalid reCAPTCHA. Please try again.'
    return render(request,'client/review_lawyer.html',{'lawyer1':lawyer1,'review_form':review_form,'msg':msg})



def viewall_review_lawyer(request,lid):
    lawyer = Lawyer.objects.get(user_id=lid) 
    review_lawyer = Review_Lawyer.objects.filter(lawyer_id__user_id=lid).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(review_lawyer, 3)
    
    try:
        review_lawyer = paginator.page(page)
    except PageNotAnInteger:
        review_lawyer = paginator.page(1)
    except EmptyPage:
        review_lawyer = paginator.page(paginator.num_pages)
    return render(request,'client/viewall_review_lawyer.html',{'lawyer':lawyer,'review_lawyer':review_lawyer})