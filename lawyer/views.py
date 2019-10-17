from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from lawyer.forms import LoginForm,RegisterForm,LawyerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from lawyer.models import State
import csv
# from lawyer.decorators import check_recaptcha

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



def client_signup(request):
    msg = ''
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.is_staff = True
            created = User.objects.get_or_create(**form.cleaned_data)
            form.save()
        # else:
        #     msg = 'Invalid reCAPTCHA. Please try again.'
    return render(request,'client/signup.html',{'form':form,'msg':msg})

def user_logout(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def view_lawyer(request):
    practice_area = request.GET['practice_area']
    return render(request,'client/view_lawyers.html',{'practice_area':practice_area})


def lawyer(request):
    user_form = RegisterForm()
    lawyer_form = LawyerForm()
    # lawyer_form.fields["state"].queryset = State.objects.all()
    # if request.method == 'POST':
    #     form1 = RegisterForm(data=request.POST)
    #     form2 = LawyerForm(data=request.POST)
    #     if form1.is_valid() and form2.is_valid():
    #         user = form1.save()
    #         user.set_password(user.password)
    #         user.is_superuser = True
    #         user.save()

    #         lawyer = form2.save(commit=False)
    #         lawyer.user = user
    #         lawyer.save()
            
    return render(request,'lawyer/lawyer_register.html',{'user_form':user_form,'lawyer_form':lawyer_form})


def state_data():
    data = State.objects.all()
    if data.count() == 0:
        with open('states.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                s = State(state_name=row['State'])
                s.save()
                print(row['State'])
    
    return data
state_data()