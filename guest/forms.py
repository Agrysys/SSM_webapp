from django import forms
from .models import MelonTest

class MelonTestForm(forms.ModelForm):
    class Meta:
        model = MelonTest
        fields = ['kode_melon', 'image', 'crop', 'edge', 'edge_resize', 'predicted_class', 'actual_class', 'pub_date']
