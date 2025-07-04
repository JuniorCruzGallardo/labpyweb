from django.contrib import admin

from .models import Cliente, Producto, Proveedor,Venta

# Agregar el modelo Cliente al Admin
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Venta)