from django.shortcuts import render


def login(request):
    if request.method == 'GET':
        return render(request,'login/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if password == 'password':
            return render(request,'index/a_index.html')
        else:
            return render(request,'login/login.html')