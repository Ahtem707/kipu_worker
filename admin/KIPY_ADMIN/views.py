from django.shortcuts import render
from .forms import UsersForm
from .models import Users
# Create your views here.
# from KIPY_ADMIN.forms import UserForm


def reg_view(request):
    error = ''
    if request.method == 'POST':
        form = UsersForm(request.POST)
        for i in form:
            print(i)
        if form.is_valid():
            form.save()
            print(123)
        else:
            error = 'Не корректные данные'
            print(error)
    else:
        form = UsersForm()
        
        # user = Users.objects.filter(telegram_id="965047706")
        # if user.exists:
        #     user = user.get()
        #     form = UsersForm(instance=user)
        # else:
        #     form = UsersForm()
    return render(request, 'reg.html', {'form': form})


def instr_view(request):
    error = ''
    if request.method == 'POST':
        form = UsersForm(request.POST)
        for i in form:
            print(i)
        if form.is_valid():
            form.save()
            print(123)
        else:
            error = 'Не корректные данные'
            print(error)
    else:
        form = UsersForm()
    return render(request, 'instruction.html', {'form': form})
