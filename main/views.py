from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406409542',
        'name': 'Rafasya Muhammad Subhan',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)
