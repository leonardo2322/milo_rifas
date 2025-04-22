# forms.py
from django import forms
from .models import Rifa

class SeleccionRifaForm(forms.Form):
    rifa = forms.ModelChoiceField(queryset=Rifa.objects.all(), label="Selecciona la rifa")
