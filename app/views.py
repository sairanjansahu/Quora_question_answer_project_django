from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView
from django.urls import reverse

# Create your views here.




#def home(request):
 #   qd=Question.objects.all()
  #  d1={'qd':qd}
   # if request.session.get('username'):
    #     username=request.session.get('username')
     #    d={'username':username,'qd':qd}
      #   return render(request,'home.html',d)
    #return render(request,'app/home.html')


def user_registeration(request):
    ufo=UserForm()
    d={'ufo':ufo}
    if request.method=='POST':
        ufd=UserForm(request.POST)
        if ufd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()
            

            return HttpResponseRedirect(reverse('QuestionList'))
        else:
            return HttpResponse('registration is not successful')
    return render(request,'app/user_registeration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('QuestionList'))
        else:
            return HttpResponse('data is invalid')
        
    return render(request,'app/user_login.html')

class QuestionList(ListView):
    model = Question
    context_object_name='questions'

class QuestionDetail(DetailView):
    model =Question
    context_object_name='Qcl'


@login_required
def ask_question(request):
    qfo= QuestionForm()
    d={'qfo':qfo}
    if request.method == 'POST':
        qfd = QuestionForm(request.POST)
        if  qfd.is_valid():
            username=request.session['username']
            UO=User.objects.get(username=username)

            NSAQO = qfd.save(commit=False)
            NSAQO.user = UO
            NSAQO.save()
            return HttpResponseRedirect(reverse('QuestionList'))
        else:
            return HttpResponse('quiestion not asked successfully')
        
    return render(request, 'app/ask_question.html',d)

@login_required
def answer_question(request):
    aqo = AnswerForm()
    d={'aqo':aqo}
    question = Question.objects.all()
    if request.method == 'POST':
        aqd= AnswerForm(request.POST)
        if aqd.is_valid():
            username=request.session['username']
            UO=User.objects.get(username=username)
            NSAQO = aqd.save(commit=False)
            NSAQO.user = UO
            NSAQO.save()
            Q=NSAQO.question
            AO=Answer.objects.filter(question=Q)
            d1={'AO':AO}
            return HttpResponseRedirect(reverse('QuestionList'))
        else:
            return HttpResponse('quiestion not asked successfully')
        
    return render(request, 'app/answer_question.html',d)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('QuestionList'))

@login_required
def like_post(request):
    if request.method == 'POST':
        cb=request.POST['cb']
        AO=Answer.objects.get(pk=cb)
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        LO=Like.objects.get_or_create(answer=AO,user=UO,value='Like')[0]
        LO.save()
        return HttpResponseRedirect(reverse('QuestionList'))
