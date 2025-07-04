from django.shortcuts import render
# En la vista se debe considera el modelo que se va usar
from .models import Cliente
from .models import Producto
from .forms import ProductoCreateForm
from .models import Proveedor
from .forms import ProveedorCreateForm, ProveedorUpdateForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

#=============================================

from .forms import CompraForm
from .models import Compra
from django.shortcuts import get_object_or_404

#=============================================
def handle_undefined_url(request):
    """
    Gestiona los urls no definidos
    """
    if not request.user.is_authenticated:
        messages.warning(request,'Debe iniciar sesión para acceder al sistema')
        return redirect('login')
    else:
        messages.info(request,'La página solicitada no existe. Se redirigirá al inicio')
    return redirect('home')    

def user_login(request):
    #Si ya esta autentica enviar a home
    if request.user.is_authenticated:
        return redirect('home')
    # Si no lo esta pedir usuario y clave
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user =authenticate(request, username = username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Error de usuario o clave')
        else:
            messages.error(request,'Ingrese sus datos')
    return render(request,'venta/login.html')



#Vista Principal del sistema
@login_required
def home(request):
    #Obtener los permisos
    user_permissions={
        'can_manage_clients':(
            request.user.is_superuser or
            request.user.groups.filter(name='grp_cliente').exists() or
            request.user.has_perm('venta.add_cliente')
        ),
        'can_manage_products':(
            request.user.is_superuser or
            request.user.groups.filter(name='grp_producto').exists()
        ),
        'can_manage_providers':(
            request.user.is_superuser or
            request.user.groups.filter(name='grp_proveedor').exists()
        ),
        'is_admin':request.user.is_superuser

    }
    context = {
        'user_permissions': user_permissions,
        'user': request.user
    }

    return render(request, 'venta/home.html', context)

#Implementar el logout

def user_logout(request):
    logout(request)
    messages.success(request, 'sesion cerrada corectamente')
    return redirect('login')

from django.http import HttpResponseForbidden
@login_required
@permission_required('venta.view_cliente', raise_exception=True)
# consulta_clientes es la vista que muestra la lista
def consulta_clientes(request):
    if not(request.user.is_superuser or
           request.user.group.filter(name='grp_cliente').exists() or
           request.user.has_perm('venta.view_cliente')
           ):
        return HttpResponseForbidden('No tienes permisos para ingressar aqui')
    # Se requiere obtner los datos a gestionar
    #clientes = Cliente.objects.all().order_by('ape_nom') # la data es la que se requiera 
    clientes = Cliente.objects.all().order_by('id_cliente') # la data es la que se requiera 
    # Estos datos deben estar disponibles para una plantilla (Template)
    # Se crea un diccionario llamado context (será accesible desde la plantilla)
    context = { # en el template será objetos y valores
        'clientes' : clientes,
        'titulo'   : 'Lista de Clientes',
        'mensaje'  : 'Hola'
    }
    # Se devolverá el enlace entre la plantilla y el contexto
    return render(request, 'venta/lista_clientes.html', context)


from .forms import ClienteCreateForm, ClienteUpdateForm
from django.contrib import messages
from django.shortcuts import redirect


@login_required
@permission_required('venta.add_cliente', raise_exception=True)

def crear_cliente(request):
    #Verificar permisos
    if not(request.user.is_superuser or
           request.user.groups.filter(name='grp_cliente').exists() or
           request.user.has_perm('venta.add_cliente')
           ):
        return HttpResponseForbidden('No tiene permisos para crear clientes')
    dni_duplicado = False

    if request.method == 'POST':
        form = ClienteCreateForm(request.POST)
        if form.is_valid():
            form.save() # salvar los datos
            messages.success(request, 'Cliente registrado correctamente')
            print('Se guardó bien')
            return redirect('crear_cliente') # se redirecciona a la misma página
        else:
            if 'id_cliente' in form.errors:
                for error in form.errors['id_cliente']:
                    if str(error) == "DNI_DUPLICADO": # se recibe del raise de forms
                        dni_duplicado = True
                        # Limpiar los errores 
                        form.errors['id_cliente'].clear()
                        print('DNI Duplicado!')
                        break

    else:
        form = ClienteCreateForm() # No hace nada, devuelve la misma pantalla

    context = {
        'form':form,
        'dni_duplicado':dni_duplicado # Enviar el estado del dni duplicado
    }
    return render(request, 'venta/crear_cliente.html', context)    



from django.http import HttpResponseForbidden
@login_required
@permission_required('venta.change_cliente', raise_exception=True)
def actualizar_cliente(request):
    if not (
        request.user.is_superuser or
        request.user.groups.filter(name='grp_cliente').exists() or
        request.user.has_perm('venta.change_cliente')
    ):
        return HttpResponseForbidden('No tiene permisos para actualizar cliente')

    cliente = None
    dni_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            # Buscar el cliente por DNI
            dni_buscado = request.POST.get('dni_busqueda')
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    form = ClienteUpdateForm(instance=cliente)
                    messages.success(request, f'Cliente con DNI {dni_buscado} encontrado')
                except Cliente.DoesNotExist:
                    messages.error(request, 'No se encontró Cliente con ese DNI')
            else:
                messages.error(request, 'Por favor ingrese el DNI para buscar')

        elif 'guardar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda') or request.POST.get('id_cliente')
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    form = ClienteUpdateForm(request.POST, instance=cliente)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Cliente actualizado correctamente')
                        cliente.refresh_from_db()
                        form = ClienteUpdateForm(instance=cliente)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado')
            else:
                messages.error(request, 'No se puede identificar al cliente para actualizar')

    context = {
        'form': form,
        'dni_buscado': dni_buscado,
        'cliente_encontrado': cliente is not None,
        'cliente': cliente
    }
    return render(request, 'venta/u_cliente.html', context)
                     
# Eliminar clientes
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden

@login_required
@permission_required('venta.delete_producto', raise_exception=True)
def borrar_producto(request):
    
    # Verificar permisos personalizados
    if not (
        request.user.is_superuser or
        request.user.groups.filter(name='grp_producto').exists() or
        request.user.has_perm('venta.delete_producto')
    ):
        return HttpResponseForbidden('No tiene permisos para eliminar productos')

    productos_encontrados = []
    tipo_busqueda = 'id'
    termino_busqueda = ''  # pa dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            # Realizar la búsqueda
            tipo_busqueda = request.POST.get('tipo_busqueda', 'id')
            termino_busqueda = request.POST.get('termino_busqueda', '').strip()

            if termino_busqueda:
                if tipo_busqueda == 'id':
                    try:
                        producto = Producto.objects.get(id_producto=termino_busqueda)
                        productos_encontrados = [producto]
                    except Producto.DoesNotExist:
                        messages.error(request, 'No se encontró producto con ese id')
                elif tipo_busqueda == 'nombre':
                    productos_encontrados = Producto.objects.filter(
                        nom_prod__icontains=termino_busqueda
                    ).order_by('id_producto')

                    if not productos_encontrados:
                        messages.error(request, 'No se encontraron productos con ese nombre')

                total_registros = len(productos_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')
            else:
                messages.error(request, 'Ingrese un término de búsqueda')

        elif 'eliminar' in request.POST:
            id_eliminar = request.POST.get('id_eliminar')

            if id_eliminar:
                try:
                    producto = Producto.objects.get(id_producto=id_eliminar)
                    producto.delete()
                    messages.success(request, f'Producto con ID {id_eliminar} eliminado correctamente')

                    # Actualizar lista tras eliminación
                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'id')
                    termino_busqueda = request.POST.get('termino_busqueda_actual', '')

                    if termino_busqueda:
                        if tipo_busqueda == 'id':
                            productos_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            productos_encontrados = Producto.objects.filter(
                                nom_prod__icontains=termino_busqueda
                            ).order_by('id_producto')

                        total_registros = len(productos_encontrados)
                except Producto.DoesNotExist:
                    messages.error(request, 'Producto no encontrado')

    context = {
        'productos_encontrados': productos_encontrados,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda,
        'total_registros': total_registros
    }

    return render(request, 'venta/borrar_producto.html', context)


def consulta_productos(request):
    # Se requiere obtener los datos a gestionar
    productos = Producto.objects.all().order_by('id_producto')  # La data es la que se requiera

    # Estos datos deben estar disponibles para una plantilla (Template)
    # Se crea un diccionario llamado context (será accesible desde la plantilla)
    context = {  # en el template será objetos y valores
        'productos': productos,
        'titulo': 'Lista de Productos',
        'mensaje': 'Consulta de productos'
    }

    # Se devolverá el enlace entre la plantilla y el contexto
    return render(request, 'venta/lista_productos.html', context)



def crear_producto(request):
    if request.method == 'POST':
        form = ProductoCreateForm(request.POST)
        if form.is_valid():
            form.save() # salvar los datos
            messages.success(request, 'producto registrado correctamente')
            return redirect('crear_producto') # se redirecciona a la misma página
    else:
        form = ProductoCreateForm() # No hace nada, devuelve la misma pantalla

    return render(request, 'venta/crear_producto.html', {'form':form})  


def borrar_cliente(request):
    clientes_encontrados = []
    tipo_busqueda = 'dni'
    termino_busqueda = '' # pa dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        #
        if 'consultar' in request.POST:
            # Realizar la búsqueda
            tipo_busqueda = request.POST.get('tipo_busqueda', 'dni')
            termino_busqueda = request.POST.get('termino_busqueda','').strip()

            if termino_busqueda:
                # procesar
                if tipo_busqueda == 'dni':
                    try:
                        cliente = Cliente.objects.get(id_cliente = termino_busqueda)
                        clientes_encontrados = [cliente]
                    except Cliente.DoesNotExist:
                        messages.error(request, 'No se encontró cliente con ese DNI')    

                elif tipo_busqueda == 'nombre':
                    clientes_encontrados = Cliente.objects.filter(
                        ape_nom__icontains = termino_busqueda # obtener las coincidencias
                    ).order_by('id_cliente') # debe estar ordenado

                    if not clientes_encontrados:
                        messages.error(request, 'No se encontraron clientes con ese nombre')

                total_registros = len(clientes_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')        

            else:
                messages.error(request, 'Ingrese un término de búsqueda')    

        elif 'eliminar' in request.POST:
            # Eliminar cliente
            dni_eliminar = request.POST.get('dni_eliminar')

            if dni_eliminar:
                try:
                    # buscar al cliente a eliminar
                    cliente = Cliente.objects.get(id_cliente = dni_eliminar)
                    cliente.delete()
                    messages.success(request, f'Cliente con DNI {dni_eliminar} eliminado correctamente')

                    # Volver a hacer la búsqueda para actualizar la lista
                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'dni')
                    termino_busqueda = request.POST.get('termino_busqueda_actual','')

                    if termino_busqueda:
                        if tipo_busqueda == 'dni':
                            # Para DNI, no mostrar nada porque ya se eliminó
                            clientes_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            # En este caso hay que buscar nuevamente lo que queda
                            clientes_encontrados = Cliente.objects.filter(
                                ape_nom__icontains = termino_busqueda
                            ).order_by('id_cliente')

                        total_registros = len(clientes_encontrados)
                

                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado')
    
    context = {
        'clientes_encontrados' : clientes_encontrados,
        'tipo_busqueda' : tipo_busqueda,
        'termino_busqueda' : termino_busqueda,
        'total_registros' : total_registros
    }

    return render(request, 'venta/borrar_cliente.html', context)


from .forms import ProductoUpdateForm  # Asegúrate de haber creado esta clase en forms.py

def actualizar_producto(request):
    producto = None
    id_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            id_buscado = request.POST.get('id_busqueda')
            if id_buscado:
                try:
                    producto = Producto.objects.get(id_producto=id_buscado)
                    form = ProductoUpdateForm(instance=producto)
                    messages.success(request, f'Producto con ID {id_buscado} encontrado')
                except Producto.DoesNotExist:
                    messages.error(request, 'No se encontró producto con ese ID')
            else:
                messages.error(request, 'Ingrese el ID del producto para buscar')
        
        elif 'guardar' in request.POST:
            id_buscado = request.POST.get('id_busqueda') or request.POST.get('id_producto')
            if id_buscado:
                try:
                    producto = Producto.objects.get(id_producto=id_buscado)
                    form = ProductoUpdateForm(request.POST, instance=producto)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Producto actualizado correctamente')
                        producto.refresh_from_db()
                        form = ProductoUpdateForm(instance=producto)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Producto.DoesNotExist:
                    messages.error(request, 'Producto no encontrado')
            else:
                messages.error(request, 'No se puede identificar el producto para actualizar')

    context = {
        'form': form,
        'id_buscado': id_buscado,
        'producto_encontrado': producto is not None,
        'producto': producto
    }
    return render(request, 'venta/u_producto.html', context)

#Consulta proveedores
@login_required
@permission_required('venta.view_proveedor', raise_exception=True)
def consulta_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('id_proveedor')
    context = {
        'proveedores': proveedores,
        'titulo': 'Lista de Proveedores',
        'mensaje': 'Consulta de proveedores'
    }
    return render(request, 'venta/lista_proveedores.html', context)

#Crear proveedor
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado correctamente')
            return redirect('crear_proveedor')
    else:
        form = ProveedorCreateForm()

    return render(request, 'venta/crear_proveedor.html', {'form': form})

#Actualizar proveedor
def actualizar_proveedor(request):
    proveedor = None
    id_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            id_buscado = request.POST.get('id_busqueda')
            if id_buscado:
                try:
                    proveedor = Proveedor.objects.get(id_proveedor=id_buscado)
                    form = ProveedorUpdateForm(instance=proveedor)
                    messages.success(request, f'Proveedor con ID {id_buscado} encontrado')
                except Proveedor.DoesNotExist:
                    messages.error(request, 'No se encontró proveedor con ese ID')
            else:
                messages.error(request, 'Ingrese el ID del proveedor para buscar')
        
        elif 'guardar' in request.POST:
            id_buscado = request.POST.get('id_busqueda') or request.POST.get('id_proveedor')
            if id_buscado:
                try:
                    proveedor = Proveedor.objects.get(id_proveedor=id_buscado)
                    form = ProveedorUpdateForm(request.POST, instance=proveedor)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Proveedor actualizado correctamente')
                        proveedor.refresh_from_db()
                        form = ProveedorUpdateForm(instance=proveedor)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Proveedor.DoesNotExist:
                    messages.error(request, 'Proveedor no encontrado')
            else:
                messages.error(request, 'No se puede identificar el proveedor para actualizar')

    context = {
        'form': form,
        'id_buscado': id_buscado,
        'proveedor_encontrado': proveedor is not None,
        'proveedor': proveedor
    }
    return render(request, 'venta/u_proveedor.html', context)

#Eliminar o borrar proveedor

def borrar_proveedor(request):
    proveedores_encontrados = []
    tipo_busqueda = 'id'
    termino_busqueda = ''
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            tipo_busqueda = request.POST.get('tipo_busqueda', 'id')
            termino_busqueda = request.POST.get('termino_busqueda','').strip()

            if termino_busqueda:
                if tipo_busqueda == 'id':
                    try:
                        proveedor = Proveedor.objects.get(id_proveedor=termino_busqueda)
                        proveedores_encontrados = [proveedor]
                    except Proveedor.DoesNotExist:
                        messages.error(request, 'No se encontró proveedor con ese ID')
                elif tipo_busqueda == 'nombre':
                    proveedores_encontrados = Proveedor.objects.filter(
                        nom_proveedor__icontains=termino_busqueda
                    ).order_by('id_proveedor')

                    if not proveedores_encontrados:
                        messages.error(request, 'No se encontraron proveedores con ese nombre')

                total_registros = len(proveedores_encontrados)
                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')
            else:
                messages.error(request, 'Ingrese un término de búsqueda')

        elif 'eliminar' in request.POST:
            id_eliminar = request.POST.get('id_eliminar')
            if id_eliminar:
                try:
                    proveedor = Proveedor.objects.get(id_proveedor=id_eliminar)
                    proveedor.delete()
                    messages.success(request, f'Proveedor con ID {id_eliminar} eliminado correctamente')

                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'id')
                    termino_busqueda = request.POST.get('termino_busqueda_actual', '')

                    if termino_busqueda:
                        if tipo_busqueda == 'id':
                            proveedores_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            proveedores_encontrados = Proveedor.objects.filter(
                                nom_proveedor__icontains=termino_busqueda
                            ).order_by('id_proveedor')

                        total_registros = len(proveedores_encontrados)
                except Proveedor.DoesNotExist:
                    messages.error(request, 'Proveedor no encontrado')

    context = {
        'proveedores_encontrados': proveedores_encontrados,
        'tipo_busqueda': tipo_busqueda,
        'termino_busqueda': termino_busqueda,
        'total_registros': total_registros
    }

    return render(request, 'venta/borrar_proveedor.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Compra
from .forms import CompraForm, CompraUpdateForm, DetalleCompraFormSet

# Crear compra con detalles
def crear_compra(request):
    if request.method == 'POST':
        form_compra = CompraForm(request.POST)
        formset_detalles = DetalleCompraFormSet(request.POST)

        if form_compra.is_valid() and formset_detalles.is_valid():
            compra = form_compra.save(commit=False)
            compra.total = 0  # Inicializamos en cero

            # Guardamos primero la compra para tener un ID
            compra.save()

            total_general = 0
            detalles = formset_detalles.save(commit=False)

            for detalle in detalles:
                detalle.compra = compra
                detalle_total = detalle.cantidad * detalle.precio_unitario
                total_general += detalle_total
                detalle.save()

            # Actualizamos el total de la compra
            compra.total = total_general
            compra.save()

            messages.success(request, "Compra registrada correctamente con sus productos.")
            return redirect('crear_compra')
        else:
            messages.error(request, "Corrige los errores en el formulario.")
    else:
        form_compra = CompraForm()
        formset_detalles = DetalleCompraFormSet()

    return render(request, 'venta/crear_compra.html', {
        'form_compra': form_compra,
        'formset_detalles': formset_detalles,
        'titulo': 'Registrar Compra con Detalles'
    })

# Actualizar compra (solo campos básicos)
def actualizar_compra(request,):
    compra = None
    id_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            id_buscado = request.POST.get('id_busqueda')
            if id_buscado:
                try:
                    compra = Compra.objects.get(id_compra=id_buscado)
                    form = CompraUpdateForm(instance=compra)
                    messages.success(request, f'Compra con ID {id_buscado} encontrada')
                except Compra.DoesNotExist:
                    messages.error(request, 'No se encontró compra con ese ID')
            else:
                messages.error(request, 'Ingrese el ID de la compra para buscar')

        elif 'guardar' in request.POST:
            id_buscado = request.POST.get('id_busqueda') or request.POST.get('id_compra')
            if id_buscado:
                try:
                    compra = Compra.objects.get(id_compra=id_buscado)
                    form = CompraUpdateForm(request.POST, instance=compra)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Compra actualizada correctamente')
                        compra.refresh_from_db()
                        form = CompraUpdateForm(instance=compra)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Compra.DoesNotExist:
                    messages.error(request, 'Compra no encontrada')
            else:
                messages.error(request, 'No se puede identificar la compra para actualizar')

    context = {
        'form': form,
        'id_buscado': id_buscado,
        'compra_encontrada': compra is not None,
        'compra': compra,
        'titulo': 'Actualizar Compra'
    }
    return render(request, 'venta/u_compra.html', context)

# Consultar compras
def consulta_compras(request):
    compras = Compra.objects.all().order_by('id_compra')
    return render(request, 'venta/lista_compras.html', {
        'compras': compras,
        'titulo': 'Lista de Compras',
        'mensaje': 'Consulta de compras'
    })

# Eliminar compra
def borrar_compra(request):
    compras_encontradas = []
    termino_busqueda = ''
    total_registros = 0

    if request.method == 'POST':
        if 'consultar' in request.POST:
            termino_busqueda = request.POST.get('termino_busqueda', '').strip()
            if termino_busqueda:
                try:
                    compra = Compra.objects.get(id_compra=termino_busqueda)
                    compras_encontradas = [compra]
                    messages.success(request, 'Compra encontrada')
                except Compra.DoesNotExist:
                    messages.error(request, 'No se encontró compra con ese ID')
                total_registros = len(compras_encontradas)
            else:
                messages.error(request, 'Ingrese un ID de compra para buscar')

        elif 'eliminar' in request.POST:
            id_eliminar = request.POST.get('id_eliminar')
            if id_eliminar:
                try:
                    compra = Compra.objects.get(id_compra=id_eliminar)
                    compra.delete()
                    messages.success(request, f'Compra con ID {id_eliminar} eliminada correctamente')
                    compras_encontradas = []
                except Compra.DoesNotExist:
                    messages.error(request, 'Compra no encontrada')

    return render(request, 'venta/borrar_compra.html', {
        'compras_encontradas': compras_encontradas,
        'termino_busqueda': termino_busqueda,
        'total_registros': total_registros,
        'titulo': 'Eliminar Compra'
    })