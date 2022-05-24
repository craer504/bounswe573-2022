from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message, Workspace, Subject
from .forms import WorkspaceForm


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home_url')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        else:
            messages.error(request, 'Username or password does not exist.')
    context = {'page': page}
    return render(request, 'learnApp/register_login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home_url')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home_url')
        else:
            messages.error(
                request, 'An error occured during the registration process.')
    return render(request, 'learnApp/register_login.html', {'form': form})


def learnapp_home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    workspaces = Workspace.objects.filter(
        Q(workspace_subject__subject_name__icontains=q) |
        Q(workspace_name__icontains=q) |
        Q(workspace_description__icontains=q)
    )
    subjects = Subject.objects.all()
    workspace_count = workspaces.count()
    workspace_messages = Message.objects.all().order_by(
        '-message_created').filter(Q(message_workspace__workspace_subject__subject_name__icontains=q))
    context = {'workspaces': workspaces, 'subjects': subjects,
               'workspace_count': workspace_count, 'workspace_messages': workspace_messages}
    return render(request, 'learnApp/learnapp_home.html', context)


def learnapp_workspace(request, pk):
    workspace = Workspace.objects.get(id=pk)
    workspace_messages = workspace.message_set.all().order_by('-message_created')
    lecturers = workspace.workspace_lecturers.all() 
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            message_workspace=workspace,
            message_body=request.POST.get('body')
        )
        workspace.workspace_lecturers.add(request.user)
        return redirect('workspace_url', pk=workspace.id)
    context = {'workspace': workspace, 'workspace_messages': workspace_messages, 'lecturers': lecturers}
    return render(request, 'learnApp/learnapp_workspace.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    workspaces = user.workspace_set.all()
    workspace_messages = user.message_set.all()
    subjects = Subject.objects.all()
    context = {'user': user, 'workspaces': workspaces,
               'workspace_messages': workspace_messages, 'subjects': subjects}
    return render(request, 'learnApp/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    return render(request, 'learnApp/update_user.html')



@login_required(login_url='login')
def createWorkspace(request):
    form = WorkspaceForm()
    subjects = Subject.objects.all()
    if request.method == 'POST':
        subject, created = Subject.objects.get_or_create(subject_name = request.POST.get('subject'))
        Workspace.objects.create(
            workspace_host = request.user,
            workspace_subject = subject,
            workspace_name = request.POST.get('workspace_name'),
            workspace_description = request.POST.get('workspace_description'),
        )
        return redirect('home_url')
    context = {'form': form, 'subjects':subjects}
    return render(request, 'learnApp/workspace_form.html', context)


@login_required(login_url='login')
def updateWorkspace(request, pk):
    workspace = Workspace.objects.get(id=pk)
    form = WorkspaceForm(instance=workspace)
    subjects = Subject.objects.all()
    if request.user != workspace.workspace_host:
        return HttpResponse('Access restricted')
    if request.method == 'POST':
        subject, created = Subject.objects.get_or_create(subject_name = request.POST.get('subject'))
        workspace.workspace_name = request.POST.get('workspace_name')
        workspace.workspace_subject = subject
        workspace.workspace_description = request.POST.get('workspace_description')
        workspace.save()
        return redirect('home_url')
    context = {'form': form,'subjects':subjects,'workspace':workspace}
    return render(request, 'learnApp/workspace_form.html', context)


@login_required(login_url='login')
def deleteWorkspace(request, pk):
    workspace = Workspace.objects.get(id=pk)
    if request.user != workspace.workspace_host:
        return HttpResponse('Access restricted')
    if request.method == 'POST':
        workspace.delete()
        return redirect('home_url')
    return render(request, 'learnApp/delete.html', {'obj': workspace})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('Access restricted')
    if request.method == 'POST':
        message.delete()
        return redirect('home_url')
    return render(request, 'learnApp/delete.html', {'obj': message})