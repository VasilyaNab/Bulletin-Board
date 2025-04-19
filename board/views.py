from django.shortcuts import render, redirect
from .models import Announcements
from django.contrib.auth.decorators import login_required

def announcement_list(request):
    announcements = Announcements.objects.all()
    return render(request, 'board/ListBoard.html', {'announcements': announcements})

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        return redirect('board:profile')
    
    announcements = Announcements.objects.filter(author=request.user).order_by('-date_publication')
    return render(request, 'profile/profile.html', {'announcements': announcements})