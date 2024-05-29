from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from .models import CoinData

class EarningsForm(forms.Form):
    hourly_earnings = forms.FloatField(label="Saatlik Kazanç")

class CoinUpdateForm(forms.ModelForm):
    coin_name = forms.ModelChoiceField(
        queryset=CoinData.objects.none(),
        empty_label="Bir coin seçin",
        label="Coin Adı",
        widget=forms.Select(attrs={'style': 'color: blue;'}))
    
    class Meta:
        model = CoinData
        fields = ['coin_name', 'sbk_value', 'price']

    def __init__(self, user, *args, **kwargs):
        super(CoinUpdateForm, self).__init__(*args, **kwargs)
        self.fields['coin_name'].queryset = CoinData.objects.filter(user=user, is_default=False)