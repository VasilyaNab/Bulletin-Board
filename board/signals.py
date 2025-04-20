from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Response

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