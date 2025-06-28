from django.urls import path
from . import views

urlpatterns = [
    path('venta/q_cliente',views.consulta_clientes,name='lista_clientes'),
    path('venta/c_cliente',views.crear_cliente,name='crear_cliente'),
    path('venta/u_cliente',views.actualizar_cliente,name='actualizar_cliente'),  
    path('venta/d_cliente',views.borrar_cliente,name='borrar_cliente'),   
    path('venta/q_producto', views.consulta_productos, name='lista_productos'),
    path('venta/c_producto', views.crear_producto, name='crear_producto'),
    path('venta/d_producto',views.borrar_producto,name='borrar_producto'),  
]