from django import forms

class DatosRegistroUsuarioChat(forms.Form):
    nombre_usuario     = forms.CharField(label='Username', max_length=254)
    password           = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password_confirmar = forms.CharField(label='Contraseña',widget=forms.PasswordInput)