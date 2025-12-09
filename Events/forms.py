from django import forms
from .models import Event, Category, Participant

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 rounded border border-blue-400 bg-blue-100 text-black focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 rounded border border-green-400 bg-green-100 text-black focus:outline-none focus:ring-2 focus:ring-green-500',
                'rows': 4
            }),
        }



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
        }


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-3/4 form-input bg-blue-100 text-black border-blue-400'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-3/4 form-input bg-blue-100 text-black border-blue-400'
            }),
            'events': forms.SelectMultiple(attrs={
                'class': 'w-3/4 form-input bg-blue-100 text-black border-blue-400'
            }),
            
        }



