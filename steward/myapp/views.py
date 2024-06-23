from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import OrganizationSignUpForm, WorkerSignUpForm, ProfileForm, FeedbackForm, RecognitionForm, GrievanceForm
from .models import Profile, Feedback, Recognition, Grievance, CommunityEntry, Organization, WorkAddress

def home(request):
    return render(request, 'home.html')

def organization_signup(request):
    if request.method == 'POST':
        form = OrganizationSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('organization_dashboard')
    else:
        form = OrganizationSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Organization'})

def organization_login(request):
    return render(request, 'login.html', {'user_type': 'Organization'})

def worker_signup(request):
    if request.method == 'POST':
        form = WorkerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully registered. Please log in.')
            return redirect('worker_login')
    else:
        form = WorkerSignUpForm()
    return render(request, 'signup.html', {'form': form, 'user_type': 'Worker'})

def worker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if not profile.is_profile_complete:  # Check if profile is incomplete
                return redirect('complete_profile')
            return redirect('worker_dashboard')  # Redirect to dashboard if profile is complete
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html', {'user_type': 'Worker'})

@login_required
def complete_profile(request):
    if hasattr(request.user, 'profile'):
        profile_instance = request.user.profile
    else:
        profile_instance = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.work_address = form.cleaned_data['address']
            organization_name = form.cleaned_data['organization_name']
            organization, created = Organization.objects.get_or_create(name=organization_name)
            profile.organization = organization
            profile.is_profile_complete = True  # Mark profile as complete
            profile.save()
            return redirect('worker_dashboard')
    else:
        form = ProfileForm(instance=profile_instance)

    return render(request, 'complete_profile.html', {'form': form})

@login_required
def worker_dashboard(request):
    work_address = request.user.profile.work_address

    context = {
        'work_address': work_address,
    }

    return render(request, 'worker_dashboard.html', context)

@login_required
def community_board(request, work_address):
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback_entry = feedback_form.save(commit=False)
            feedback_entry.work_address = work_address
            if request.POST.get('anonymous'):
                feedback_entry.user = None
            else:
                feedback_entry.user = request.user
            feedback_entry.save()
            return redirect(reverse('community_board', args=[work_address]))
    else:
        feedback_form = FeedbackForm()

    feedback_entries = Feedback.objects.filter(work_address=work_address)
    context = {
        'work_address': work_address,
        'feedback_form': feedback_form,
        'feedback_entries': feedback_entries,
    }
    return render(request, 'community_board.html', context)
