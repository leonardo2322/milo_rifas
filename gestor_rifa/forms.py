# forms.py
from django import forms
from .models import Rifa, Cliente, Comprobantes_de_pago

class SeleccionRifaForm(forms.Form):
    rifa = forms.ModelChoiceField(queryset=Rifa.objects.all(), label="Selecciona la rifa")

class Cliente_form(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'cedula','direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo', 'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'cedula','class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono','class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Direccion exacta','class': 'form-control'}),
        }

class ComprobanteForm(forms.ModelForm):
    class Meta:
        model = Comprobantes_de_pago
        fields = ['ultimos_digitos', 'comprobante']
        widgets = {
            'ultimos_digitos': forms.TextInput(attrs={
                'placeholder': 'Últimos dígitos del pago',
                'class': 'form-control mt-3 mb-5'
            }),
            'comprobante': forms.ClearableFileInput(attrs={
                'class': 'd-none',
                'accept': 'image/*'  # Aceptar solo imágenes
            }),
        }

        labels = {
            'ultimos_digitos': 'Dígitos del comprobante de pago',  # Aquí lo colocas
            'comprobante': 'Comprobante de pago',  # Aquí lo colocas
        }