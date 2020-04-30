from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

class WanttoReadForm(forms.Form):
    want_to_read = forms.CharField(max_length=255)

class BookProgressForm(forms.Form):
    book_progress_input = forms.IntegerField()
    book_progress_note_input = forms.CharField(max_length=300, required=False)
    book_progress_id = forms.CharField(max_length=100)