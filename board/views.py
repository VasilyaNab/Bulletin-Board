from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Announcements, Response, ResponseStatus, Categories, CategorySubscription

def announcement_list(request):
    announcements = Announcements.objects.all().order_by('-date_publication')
    return render(request, 'board/ListBoard.html', {'announcements': announcements})

@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcements, pk=pk)
    responses = Response.objects.filter(announcements=announcement).select_related('user', 'status')
    
    return render(request, 'board/detail.html', {
        'announcement': announcement,
        'responses': responses,
    })

@login_required
def create_response(request, announcement_id):
    announcement = get_object_or_404(Announcements, id=announcement_id)
    
    if request.user == announcement.author:
        return HttpResponseForbidden("Вы не можете оставить отклик на свое объявление")
    
    if Response.objects.filter(announcements=announcement, user=request.user).exists():
        messages.warning(request, "Вы уже оставляли отклик на это объявление")
        return redirect('board:announcement-detail', pk=announcement_id)
    
    Response.objects.create(
        announcements=announcement,
        user=request.user,
        status=ResponseStatus.objects.get_or_create(status='На рассмотрении')[0]
    )
    
    messages.success(request, "Ваш отклик успешно отправлен!")
    return redirect('board:announcement-detail', pk=announcement_id)

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        messages.success(request, 'Профиль успешно обновлен')
        return redirect('profile')
    
    announcements = Announcements.objects.filter(author=request.user).order_by('-date_publication')
    responses = Response.objects.filter(announcements__author=request.user).select_related('announcements', 'user', 'status')
    
    context = {
        'announcements': announcements,
        'responses': responses[:5],
        'responses_count': responses.count(),
    }
    return render(request, 'profile/profile.html', context)

@login_required
def response_list(request):
    responses = Response.objects.filter(
        announcements__author=request.user
    ).select_related('announcements', 'user', 'status').order_by('-created_date')
    
    # Фильтрация
    announcement_id = request.GET.get('announcement')
    status_id = request.GET.get('status')
    
    if announcement_id:
        responses = responses.filter(announcements_id=announcement_id)
    if status_id:
        responses = responses.filter(status_id=status_id)
    
    context = {
        'responses': responses,
        'user_announcements': Announcements.objects.filter(author=request.user),
        'statuses': ResponseStatus.objects.all(),
        'selected_announcement': int(announcement_id) if announcement_id else None,
        'selected_status': int(status_id) if status_id else None,
    }
    return render(request, 'profile/responses.html', context)

@login_required
def response_action(request, pk, action):
    response = get_object_or_404(Response, pk=pk, announcements__author=request.user)
    
    if action == 'accept':
        response.accept()
        messages.success(request, 'Отклик принят. Отправитель получил уведомление.')
    elif action == 'reject':
        response.reject()
        messages.success(request, 'Отклик отклонен. Отправитель получил уведомление.')
    elif action == 'delete':
        response.delete()
        messages.success(request, 'Отклик удален')
    
    return redirect('board:response-list')

@login_required
def newsletter_view(request):
    categories = Categories.objects.all()
    subscriptions = CategorySubscription.objects.filter(user=request.user)
    subscribed_ids = list(subscriptions.values_list('category_id', flat=True))
    
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        action = request.POST.get('action')
        
        try:
            category = Categories.objects.get(id=category_id)
            if action == 'subscribe':
                CategorySubscription.objects.get_or_create(
                    user=request.user,
                    category=category,
                    defaults={'subscribed': True}
                )
            elif action == 'unsubscribe':
                CategorySubscription.objects.filter(
                    user=request.user,
                    category=category
                ).delete()
        except Categories.DoesNotExist:
            messages.error(request, "Категория не найдена")
        
        return redirect('board:newsletter')

    context = {
        'categories': categories,
        'subscribed_ids': subscribed_ids,
    }
    return render(request, 'board/newsletter.html', context)