from allauth.account.forms import SignupForm
from django import forms
from .models import Announcements, Categories

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class AnnouncementForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        label='Категория',
        empty_label="Выберите категорию"
    )
    
    class Meta:
        model = Announcements
        fields = ['header', 'category', 'text', 'image']
        widgets = {
            'header': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }