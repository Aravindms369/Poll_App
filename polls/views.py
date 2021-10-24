# import all packages and modules here
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from json import dumps
from .models import User,Question,Choice, Vote_count
from .forms import PostForm, ChoiceForm, Choice_edit_Form, Voted_count
from django.utils import timezone
#global que
#Pollapp homepage function
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list,}
    return render(request, 'polls/index.html', context)
#User login function
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return HttpResponseRedirect(reverse('polls:user_home'))
        else:
            return render(request, "polls/login.html", {
            "errmessage": "Invalid username and/or password."
            })
    else:
        return render(request, "polls/login.html")

#User logout function
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("polls:index"))

#User Register function
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        # Attempt to create new user and ensure all fields are filled
        if username and email and password and confirmation is not None:
            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "polls/register.html", {
                    "errmessage": "Passwords must match."
                })
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "polls/register.html", {
                    "errmessage": "Username already taken."
                })
            login(request, user)
            messages.success(request, 'Login Successful')
            return HttpResponseRedirect(reverse('polls:user_home')) 
        # if error then display error
        else:
            return render(request, "polls/register.html", {
                "errmessage": "Fill all fields"
            })
    else:
        return render(request, "polls/register.html")
#View after user login
def user_home(request):
    question_list = Question.objects.all().order_by('-pub_date')
    return render(request,'polls/userhome.html',{'question_list':question_list})

#view for userhome in case already voted
def error_user_home(request):
    question_list = Question.objects.all().order_by('-pub_date')
    error_message="Sorry, but you have already voted."
    return render(request,'polls/userhome.html',{'question_list':question_list,'error_message':error_message})
#View for adding new poll
def addpoll(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.username = request.user
            post.save()
            return redirect("polls:addpoll")
    else:
        form = PostForm()
        return render(request=request, template_name="polls/addpoll.html", context={'form': form})
# view for adding choices
def addchoice(request):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect("polls:addchoice")
    else:
        form = ChoiceForm()
        return render(request=request, template_name="polls/addchoice.html", context={'form': form})

#To edit poll question and category
def editpoll(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:user_home')
    else:
        form = PostForm()
        return render(request,'polls/editpoll.html',{'form':form,'question':question,})

#To edit choice list
def editchoice(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = Choice_edit_Form(request.POST, instance=question)
        if form.is_valid():
            old_choice = form.cleaned_data['choice_text']
            new_choice = form.cleaned_data['new_choice']
            Choice.objects.filter(choice_text=old_choice).update(choice_text=new_choice)
            return redirect('polls:user_home')
    else:
        form = Choice_edit_Form()
        return render(request,'polls/editchoice.html',{'form':form,'question':question,})
# delete a poll
def deletepoll(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('polls:user_home')
# delete a choice from poll
def deletechoice(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=question)
        if form.is_valid():
            old_choice = form.cleaned_data['choice_text']
            Choice.objects.filter(choice_text=old_choice).delete()
            return redirect('polls:user_home')
    else:
        form = ChoiceForm()
        return render(request,'polls/deletechoice.html',{'form':form,'question':question,})
#View for displaying full poll view
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #to ensure only owner of the poll can edit the poll
    if str(request.user) == question.username:
        var=1
    else:
        var=0
    return render(request, 'polls/detail.html', {'question': question,'var':var})
#Display vote count in the form of charts
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #To display result chart get all choices and their count
    l=question.choice_set.all()
    xval=[item.choice_text for item in l]
    yval = [item.votes for item in l]
    #save the ids of user voted to ensure vote only once
    form = Voted_count()
    my_obj = form.save(commit=False)
    my_obj.question_voted = question_id
    my_obj.voter = request.user.id
    my_obj.save()
    return render(request, 'polls/results.html', {'question': question, 'xval':dumps(xval), 'yval':dumps(yval)})
#View for counting the votes for each choice
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    #check whether user already voted
    if Vote_count.objects.filter(question_voted=question_id, voter=request.user.id).exists():
        messages.error(request, 'already voted')
        return redirect('polls:error_user_home')
    #if not voted increase the vote count
    else:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


#search method
def search(request):        
    if request.method == 'GET': # this will be GET now      
        que_name =  request.GET.get('poll_instance') # get the input value 
        print(que_name)    
        try:
            status = Question.objects.filter(question_text__icontains=que_name) # filter returns a  matching list 
            print(status)
        except Exception as e:     #exception handling
            messages.error(request, e)
            return redirect('polls:error_user_home')
        else:
            return render(request,"polls/search.html",{"poll":status})
    else:
        return render(request,"polls/search.html",{})
