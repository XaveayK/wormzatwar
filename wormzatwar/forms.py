from django import forms
from .models import WormUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class newUserForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['username']

    error_messages = {
        "username_exists": ("Username already present")
    }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.username == username: return username
        try: User._default_manager.get(username=username)
        except User.DoesNotExist: return username

        raise forms.ValidationError(
            self.error_messages['username_exists'],
            code='username_exists',
        )

    def save(self, commit=True):
        user = super(newUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user