from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()
    # check if the method is POST
    if (request.method == 'POST'):
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # athenticate the user
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Your have been logged in!!')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong. Please try again!!')
            return redirect('home')

    else:
        
        return render(request, 'home.html',{'records':records})


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, 'See you soon again!!')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username, password=password)
            login(request=request, user=user)
            messages.success(request, 'User registered successfully')
            return redirect( 'home')
    else:
        form = SignUpForm()
        return render(request, 'register.html',{'form':form})
    
    return render(request, 'register.html',{'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html',{'record':record})
        
    else:
        messages.error(request, 'You must be authenticated to view this page...')
        return redirect('home')
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, 'Record deleted...')
        return redirect('home')
        
    else:
        messages.error(request, 'You must be Login...')
        return redirect('home')
def add_record(request):
    form = AddRecordForm(request.POST or None)

    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record Added')
                return redirect('home')
    
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, 'You must be Login...')
        return redirect('home')
def update_record(request,pk):

    if request.user.is_authenticated:
        current_user = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None,instance=current_user)
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Record updated')
                return redirect('home')
    
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.error(request, 'You must be Login...')
        return redirect('home')