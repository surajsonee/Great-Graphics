from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    """testimonial form"""
    class Meta:
        """meta variables"""
        model = Testimonial
        fields = ['stars', 'text', 'author']
