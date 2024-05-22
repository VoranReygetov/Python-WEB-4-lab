from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'nameBook', 'yearBook', 'availableBook', 'category', 'author']
        widgets = {
            'nameBook': forms.TextInput(attrs={'class': 'form-control', }),
            'yearBook': forms.NumberInput(attrs={'class': 'form-control'}),
            'availableBook': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control',}),
        }
