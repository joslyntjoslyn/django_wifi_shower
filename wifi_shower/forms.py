from .models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


