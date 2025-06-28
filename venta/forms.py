from django import forms
#from django.core.validators import RegexValidator
# De nuestro negocio
from .models import Cliente
from .models import Producto
# Para gestionar un error
from django.core.exceptions import ValidationError

# Clase para crear un cliente
class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'ape_nom', 'fec_reg'] # Atributos del modelo cuyos valores se agregarán
        labels = {
            'id_cliente': 'DNI', 
            'ape_nom'   : 'Apellidos y Nombres',
            'fec_reg'   : 'Fecha de Registro',
        }
        widgets = {
            'fec_reg' : forms.DateInput(attrs={'type':'date'})  # es para poner un control de calendario
        }
        error_messages = {
            'id_cliente' : {
                'max_length' : "El DNI debe tener máximo 8 caracteres",
            }
        }
# Clase para eliminar un cliente
    def clean_id_cliente(self):
        # id_cliente viene de la plantilla (html)
        id_cliente = self.cleaned_data.get('id_cliente')

        if id_cliente:
            # Verificar que existe un DNI
            if Cliente.objects.filter(id_cliente=id_cliente).exists():
                # Realiza un lanzamiento de error 
                raise ValidationError("DNI_DUPLICADO")
            return id_cliente

# Clase para modificar un cliente
class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['ape_nom', 'fec_reg'] # Atributos del modelo cuyos valores se agregarán
        labels = {
            #'id_cliente': 'DNI', 
            'ape_nom'   : 'Apellidos y Nombres',
            'fec_reg'   : 'Fecha de Registro',
        }

        widgets = {
            # 'id_cliente': forms.TextInput(
            #     attrs={
            #         'readonly':True,
            #         'class':'readonly-field'
            #     }
            # ),
            'ape_nom': forms.TextInput(
                attrs={
                    'placeholder':'Ingrese apellidos y nombres'
                }
            ),
            
            'fec_reg': forms.DateInput(
                attrs={
                    'type':'date'
                },
                format='%Y-%m-%d'
            )
                        
            # 'fec_reg': forms.DateInput(
            #     attrs={'type': 'date'}, 
            #     format=f'%d/%m/%Y'
            #     )                   
            
        }

class ProductoCreateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id_producto','nom_prod','descrip_prod','precio','stock','activo','fec_vencim','fec_reg']
        labels = {
            'id_producto' : 'ID del Producto',
            'nom_prod'    : 'Nombre del Producto',
            'descrip_prod': 'Descripción',
            'precio'      : 'Precio (S/.)',
            'stock'       : 'Cantidad en Stock',
            'activo'      : '¿Está Activo?',
            'fec_vencim'  : 'Fecha de Vencimiento',
            'fec_reg'     : 'Fecha de Registro',
        }
        widgets = {
            'fec_vencim'  : forms.DateInput(attrs={'type': 'date'}),
            'fec_reg'     : forms.DateTimeInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'nom_prod': {
                'max_length': "El nombre del producto no debe exceder los 50 caracteres.",
            },
            'descrip_prod': {
                'max_length': "La descripción es muy larga (máximo 500 caracteres).",
            },
            'precio': {
                'invalid': "Ingrese un precio válido en formato decimal.",
            },
            'stock': {
                'invalid': "El stock debe ser un número entero positivo.",
            },
        }


# Clase para modificar un producto
class ProductoUpdateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nom_prod','descrip_prod','precio','stock','activo','fec_vencim','fec_reg']
        labels = {
            'nom_prod'    : 'Nombre del Producto',
            'descrip_prod': 'Descripción',
            'precio'      : 'Precio (S/.)',
            'stock'       : 'Cantidad en Stock',
            'activo'      : '¿Está Activo?',
            'fec_vencim'  : 'Fecha de Vencimiento',
            'fec_reg'     : 'Fecha de Registro',
        }
        widgets = {
            'nom_prod'    : forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto'}),
            'descrip_prod': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3}),
            'precio'      : forms.NumberInput(attrs={'step': '0.01'}),
            'stock'       : forms.NumberInput(attrs={'min': 0}),
            'fec_vencim'  : forms.DateInput(attrs={'type': 'date'}),
            'fec_reg'     : forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'nom_prod': {
                'max_length': "El nombre del producto no debe exceder los 50 caracteres.",
            },
            'descrip_prod': {
                'max_length': "La descripción es muy larga (máximo 500 caracteres).",
            },
            'precio': {
                'invalid': "Ingrese un precio válido.",
            },
            'stock': {
                'invalid': "Ingrese una cantidad válida para el stock.",
            },
        }
