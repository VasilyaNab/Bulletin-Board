from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Announcements(models.Model):
    header = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='board_images', null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-date_publication']

class ResponseStatus(models.Model):
    status = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус отклика'
        verbose_name_plural = 'Статусы откликов'

class Response(models.Model):
    announcements = models.ForeignKey(Announcements, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(ResponseStatus, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Отклик на {self.announcements} от {self.user}"
    
    def accept(self):
        accepted_status = ResponseStatus.objects.get_or_create(status='Принят')[0]
        self.status = accepted_status
        self.save()
    
    def reject(self):
        rejected_status = ResponseStatus.objects.get_or_create(status='Отклонен')[0]
        self.status = rejected_status
        self.save()
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_date']
        unique_together = ['announcements', 'user']