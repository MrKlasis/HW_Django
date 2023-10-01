from django.shortcuts import render


def home(request):
    return render(request, 'main/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        message = request.POST.get('message')
        print(f'{name} ({number}): {message}')
    return render(request, 'main/contacts.html')

