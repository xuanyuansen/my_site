from django import forms
from .models import XysUser


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    # 确认输入的密码
    password = forms.CharField()
    password2 = forms.CharField()
    register_key = forms.CharField()

    class Meta:
        model = XysUser
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重新输入")

    def check_valid(self):
        data = self.cleaned_data
        if data.get('register_key') == 'loveyuting':
            return True
        else:
            return False
