from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.user_login, name="login"),
    path("home/",views.home, name="home"),
    path("logout/",views.user_logout, name="logout"),
    #path('',views.home, name="home"),#Pagina principal
    path('venta/q_cliente',views.consulta_clientes,name='lista_clientes'),
    path('venta/c_cliente',views.crear_cliente,name='crear_cliente'),
    path('venta/u_cliente',views.actualizar_cliente,name='actualizar_cliente'),  
    path('venta/d_cliente',views.borrar_cliente,name='borrar_cliente'),   
      # Producto
    path('venta/q_producto', views.consulta_productos, name='lista_productos'),
    path('venta/c_producto', views.crear_producto, name='crear_producto'),
    path('venta/d_producto',views.borrar_producto,name='borrar_producto'),  
    path('venta/u_producto', views.actualizar_producto, name='actualizar_producto'),
    # Proveedor
    path('venta/q_proveedor', views.consulta_proveedores, name='lista_proveedores'),
    path('venta/c_proveedor', views.crear_proveedor, name='crear_proveedor'),
    path('venta/u_proveedor', views.actualizar_proveedor, name='actualizar_proveedor'),
    path('venta/d_proveedor', views.borrar_proveedor, name='borrar_proveedor'),


    # Ventas
    path('venta/q_venta', views.venta_list, name='lista_ventas'),
    path('venta/c_venta', views.venta_create, name='crear_venta'),
    path('venta/u_venta/<str:cod_venta>/', views.venta_update, name='actualizar_venta'),
    path('venta/d_venta/<str:cod_venta>/', views.venta_delete, name='eliminar_venta'),





]