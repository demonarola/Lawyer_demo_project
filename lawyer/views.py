from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from lawyer.forms import LoginForm,RegisterForm,LawyerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lawyer.models import State,Data,Practice_area,Sub_practice_area,Lawyer_practice_area,Lawyer
import csv
from lawyer.decorators import check_recaptcha



# Create your views here.
def index(request):
    return render(request,'client/index.html')


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = User.objects.get(email=email).username      
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active and user.is_staff:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            elif user.is_active and user.is_superuser:
                login(request,user)
                return HttpResponse('Lawyer')
            else:
                return HttpResponse('Plz Login First...')
        else:
            return HttpResponse("Invalid login details supplied.")
    # else:
    #     # return HttpResponse("Invalid login details supplied.")       
    #     form = LoginForm()
    return render(request,'client/login.html',{'form':form})


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
                else:
                    msg = 'Password and Confirm Passwords Must be same...'
            else:
                msg= 'Invalid reCAPTCHA. Please try again.' 
    return render(request,'client/signup.html',{'form':form,'msg':msg})


def user_logout(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def view_lawyer(request):
    practice_area = request.GET['practice_area']
    d1 = Lawyer_practice_area.objects.filter(practice_area__practice=practice_area)
    return render(request,'client/view_lawyers.html',{'practice_area':practice_area,'d1':d1})


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
def dropdown(request):
    sarea2=''
    if request.method == 'POST':
        uid = request.POST.get('uid')
        
        pid = request.POST.get('practice_area')
        # select = request.POST.getlist('sub_area')
        select = request.POST.getlist('sub_area[]')
        ganga = request.POST.getlist('area')
        print('--- Ganga ---',ganga)
        u = User.objects.get(id=uid)
        s = Lawyer.objects.get(user_id=uid)
       
        # for i in range(0,len(select)):
        #     print(select[i])
        #     p = Practice_area.objects.get(id=pid)
        #     d = Lawyer_practice_area()
        #     d.lawyer_id=s
        #     d.practice_area = p
        #     d.sub_practice_area = select[i]
        #     d.save()

        # p = Practice_area.objects.get(id=pid)
        # d = Lawyer_practice_area()
        # d.lawyer_id=s
        # d.practice_area = p
        # d.sub_practice_area = select
        # d.save()
    
        sarea = request.POST['s_area']
        # sarea2 = Lawyer_practice_area.objects.filter(lawyer_id__user=uid)
        sarea2 = Lawyer_practice_area.objects.filter(sub_practice_area__contains=sarea)
    
    srea = Sub_practice_area.objects.all()
    practice = Practice_area.objects.all()
    return render(request,'lawyer/dropdown.html',{'practice':practice,'sarea':srea,'sarea2':sarea2})

def area_dropdown(request):
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
            if Lawyer_practice_area.objects.filter(practice_area_id=pid):
                lawyer_sub_area = Lawyer_practice_area.objects.get(practice_area_id=pid)
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