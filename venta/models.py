from django.db import models

'''
  Definir la entidad (el nombre de la tabla y sus atributos (con tipos y validaciones))
  Cliente
     id_cliente, texto numérico de 8 caracteres, clave principal
     ape_nom, texto, max 80 caracteres
     fec_reg, Fecha (formato dd/mm/aaaa)
     fec_sis, Fecha y hora en que se registre el dato (timestamp)
'''
class Cliente(models.Model):
    # Creación de los atributos de Cliente
    id_cliente = models.CharField(primary_key=True, max_length=8, error_messages='El texto debe tener max 8 digitos')
    ape_nom = models.CharField(max_length=80)
    fec_reg = models.DateField() # solo es fecha
    fec_sis = models.DateTimeField(auto_now=True) # es fecha y hora actual

    def __str__(self):
        return f"Nombres : {self.ape_nom}, DNI : {self.id_cliente}"


'''
  Crear el modelo Producto
  Producto
     id_producto, numero entero autocorrelativo que comienza en 1, será clave principal
     nom_prod, texto de 50 caracteres como máximo
     des_prod, texto de 500 caracteres multilineas
     precio, numero real positivo de dos decimales
     stock, numero entero mayor o igual que cero
     activo, valor lógico (True si esta activo, de otra forma false)
     fec_vencim, tipo fecha (aaaa-mm-dd)
     fec_reg, tipo fecha y hora (registro del momento de guardado - timestamp)
'''  

'''
   Enviar al chat grupal la captura de la imagen de la tabla Producto en el Admin
   Pongan sus nombres y apellidos para reconocerlos
   https://chat.whatsapp.com/LirsKMPB8UAEkE6ZfqJQnA

   Puntaje: 7 puntos para la nota 1
   Plazo: 12/06/2025 23:59 hrs
'''  
from django.core.validators import MinValueValidator

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)  # entero autocorrelativo, clave primaria
    nom_prod = models.CharField(max_length=50)
    descrip_prod = models.TextField(max_length=500)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.PositiveIntegerField()  # entero >= 0
    activo = models.BooleanField(default=True)
    fec_vencim = models.DateField()
    fec_reg = models.DateTimeField()  # timestamp al guardar

    def __str__(self):
        return f'{self.nom_prod} - S/. {self.precio} (Stock: {self.stock}) | Vence: {self.fec_vencim} | Activo: {"Sí" if self.activo else "No"}'
    

  
  


from django.core.validators import MinLengthValidator

'''
  Modelo: Proveedor
  Tabla: venta_proveedor
  Atributos:
    - id_proveedor: texto numérico de 8 caracteres, clave primaria
    - razon_social: texto, máximo 100 caracteres
    - ruc: texto de 11 caracteres, único
    - direccion: texto libre, opcional
    - telefono: texto hasta 15 caracteres, opcional
    - email: correo electrónico, opcional
    - fec_reg: fecha manual de registro (formato aaaa-mm-dd)
    - fec_sis: fecha y hora del sistema (timestamp)
'''

class Proveedor(models.Model):
    id_proveedor = models.CharField(
        primary_key=True,
        max_length=8,
        validators=[MinLengthValidator(1)],
        error_messages={'max_length': 'Máximo 8 caracteres'}
    )
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11, unique=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    fec_reg = models.DateField()  # fecha registrada manualmente
    fec_sis = models.DateTimeField(auto_now=True)  # fecha-hora del sistema


    def __str__(self):
        return f'ID: {self.id_proveedor} | {self.razon_social} | RUC: {self.ruc}'


class Compra(models.Model):
    id_compra = models.CharField(max_length=10, primary_key=True)
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.id_compra} - {self.proveedor.nom_proveedor}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey('Compra', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.producto.nom_prod} x {self.cantidad} (Compra {self.compra.id_compra})"

