from django.shortcuts import render
from .forms import UsersForm
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
