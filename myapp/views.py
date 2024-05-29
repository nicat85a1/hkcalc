from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import CoinData
from django.contrib.auth.decorators import login_required
from .forms import EarningsForm, CoinUpdateForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CoinData
from .forms import EarningsForm, CoinUpdateForm
from prettytable import PrettyTable
from.models import UserProfile

@login_required(login_url="login")
def index(request):
    user = request.user
    coindata = CoinData.objects.filter(user=user, is_default=False)
    update_form = CoinUpdateForm(user=user)
    if request.method == 'POST':
        earnings_form = EarningsForm(request.POST)
        if earnings_form.is_valid():
            hourly_earnings = earnings_form.cleaned_data['hourly_earnings']
            
            profitability_ratios = []
            for coin in coindata:
                if coin.price != 0:
                    wait_time_hours = coin.price / hourly_earnings
                    wait_time_minutes = wait_time_hours * 60
                    total_earnings = wait_time_hours * hourly_earnings
                    profitability = coin.sbk_value / total_earnings
                    profitability_ratios.append((coin.coin_name, f"{profitability:.4f}", coin.price, wait_time_minutes, coin.sbk_value))

            sorted_profitability = sorted(profitability_ratios, key=lambda x: x[0])
            sorted_profitability_sp = sorted(profitability_ratios, key=lambda x: (x[1], -x[3]))

            table = PrettyTable(['Coin Adı', 'Saat basi kar+', 'Ödenecek Tutar'])
            for coin in sorted_profitability:
                table.add_row([coin[0], f"{coin[4]:.0f}", f"{coin[2]:.0f}"])
            table_html = table.get_html_string()
            print(sorted_profitability[-1][0])
            
            context = {
                'coindata': coindata,
                'earnings_form': earnings_form,
                'table_html': table_html,
                'update_form': update_form,
                'show_results': True,
                'user': user,
                'spresult':sorted_profitability_sp[-1][0],
                'heresult':f"{sorted_profitability_sp[-1][4]:.0f}",
                'bsresult':f"{sorted_profitability_sp[-1][3]:.0f}"
            }
            
            return render(request, 'index.html', context)
    else:
        earnings_form = EarningsForm()

    context = {
        'coindata': coindata,
        'earnings_form': earnings_form,
        'update_form': update_form,
        'show_results': False,
        'user': user
    }
    
    return render(request, 'index.html', context)

@login_required(login_url="login")
def update_coin(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    post_request_limit = user_profile.post_request_limit
    if request.method == 'POST':
        if post_request_limit > 0:
            user_profile.post_request_limit -= 1
            user_profile.save()
            form = CoinUpdateForm(user=user, data=request.POST)
            print(form)
            if form.is_valid():
                coin = form.cleaned_data['coin_name']
                coin.sbk_value = form.cleaned_data['sbk_value']
                coin.price = form.cleaned_data['price']
                coin.save()
                return redirect('index')
        else:
            return render(request, 'index.html', {'error_message': 'limitiniz aşıldı.'})
    return redirect('index')