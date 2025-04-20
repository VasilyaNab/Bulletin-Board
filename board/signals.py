from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .models import Response, Announcements, CategorySubscription

@receiver(post_save, sender=Response)
def notify_on_response_status_change(sender, instance, created, **kwargs):
    if created:
        return
    
    if instance.status.status == 'Принят':
        send_response_email(
            instance,
            'emails/response_accepted.html',
            f'Ваш отклик принят на объявление "{instance.announcements.header}"'
        )
    elif instance.status.status == 'Отклонен':
        send_response_email(
            instance,
            'emails/response_rejected.html',
            f'Ваш отклик отклонен на объявление "{instance.announcements.header}"'
        )

def send_response_email(response, template_name, subject):
    html_content = render_to_string(template_name, {
        'response': response,
        'announcement': response.announcements,
        'author': response.announcements.author,
    })
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[response.user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Announcements)
def send_new_announcement_notification(sender, instance, created, **kwargs):
    if created:
        subscriptions = CategorySubscription.objects.filter(
            category=instance.category,
            subscribed=True
        ).select_related('user')
        
        for subscription in subscriptions:
            subject = f'Новое объявление в категории {instance.category.name}'
            message = render_to_string('emails/new_announcement.html', {
                'announcement': instance,
                'user': subscription.user
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [subscription.user.email],
                html_message=message
            )