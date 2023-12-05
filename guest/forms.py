from django import forms
from .models import MelonTest
class MelonTestForm(forms.Form):
    image = forms.ImageField(label="masukan gambar melon")
    actual_class = forms.MultipleChoiceField(choices=MelonTest.CLASS_MELON)

