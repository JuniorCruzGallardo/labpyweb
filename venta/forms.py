from django import forms
#from django.core.validators import RegexValidator
# De nuestro negocio
from .models import Cliente, Producto, Proveedor, Compra, DetalleCompra

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


# Clase para crear un proveedor
class ProveedorCreateForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['id_proveedor', 'razon_social', 'ruc', 'direccion', 'telefono', 'email', 'fec_reg']
        labels = {
            'id_proveedor': 'ID del Proveedor',
            'razon_social': 'Razón Social',
            'ruc'         : 'RUC',
            'direccion'   : 'Dirección',
            'telefono'    : 'Teléfono',
            'email'       : 'Correo Electrónico',
            'fec_reg'     : 'Fecha de Registro',
        }
        widgets = {
            'direccion' : forms.Textarea(attrs={'rows': 2, 'placeholder': 'Dirección del proveedor'}),
            'telefono'  : forms.TextInput(attrs={'placeholder': 'Ej. 987654321'}),
            'email'     : forms.EmailInput(attrs={'placeholder': 'Ej. proveedor@empresa.com'}),
            'fec_reg'   : forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'id_proveedor': {
                'max_length': "El ID no debe exceder los 8 caracteres.",
            },
            'ruc': {
                'max_length': "El RUC debe tener 11 dígitos.",
                'unique': "Este RUC ya está registrado.",
            },
        }

    def clean_id_proveedor(self):
        id_proveedor = self.cleaned_data.get('id_proveedor')
        if id_proveedor and Proveedor.objects.filter(id_proveedor=id_proveedor).exists():
            raise ValidationError("ID_DUPLICADO")
        return id_proveedor

# Clase para modificar un proveedor
class ProveedorUpdateForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social', 'ruc', 'direccion', 'telefono', 'email', 'fec_reg']
        labels = {
            'razon_social': 'Razón Social',
            'ruc'         : 'RUC',
            'direccion'   : 'Dirección',
            'telefono'    : 'Teléfono',
            'email'       : 'Correo Electrónico',
            'fec_reg'     : 'Fecha de Registro',
        }
        widgets = {
            'razon_social': forms.TextInput(attrs={'placeholder': 'Ej. Inversiones ABC S.A.C.'}),
            'ruc'         : forms.TextInput(attrs={'placeholder': '11 dígitos'}),
            'direccion'   : forms.Textarea(attrs={'rows': 2}),
            'telefono'    : forms.TextInput(attrs={'placeholder': 'Ej. 987654321'}),
            'email'       : forms.EmailInput(attrs={'placeholder': 'proveedor@empresa.com'}),
            'fec_reg'     : forms.DateInput(attrs={'type': 'date'}),
        }

#===========================
# Formulario Principal de Compra

from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
#===========================
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['id_compra', 'proveedor', 'fecha_compra']
        labels = {
            'id_compra': 'ID de la Compra',
            'proveedor': 'Proveedor',
            'fecha_compra': 'Fecha de Compra',
        }
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_id_compra(self):
        id_compra = self.cleaned_data.get('id_compra')
        if id_compra and Compra.objects.filter(id_compra=id_compra).exists():
            raise ValidationError("ID_COMPRA_DUPLICADO")
        return id_compra

#===========================
# Formulario de DetalleCompra (inline)
#===========================
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario (S/.)',
        }

#===========================
# InlineFormset de Detalles de Compra
#===========================
DetalleCompraFormSet = inlineformset_factory(
    Compra,
    DetalleCompra,
    form=DetalleCompraForm,
    extra=1,
    can_delete=True
)

#===========================
# Formulario para actualizar la compra (cuando ya existe y tiene total)
#===========================
class CompraUpdateForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'fecha_compra', 'total']
        labels = {
            'proveedor'    : 'Proveedor',
            'fecha_compra' : 'Fecha de Compra',
            'total'        : 'Total de la Compra (S/.)',
        }
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'type': 'date'}),
            'total'       : forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
        error_messages = {
            'total': {
                'required': "Debe ingresar el total de la compra.",
                'invalid': "Ingrese un número válido para el total.",
            },
        }