from django.shortcuts import render

from .forms import MelonTestForm

def melon_test_view(request):
    if request.method == 'POST':
        form = MelonTestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = MelonTestForm()
    return render(request, 'melon_test.html', {'form': form})

