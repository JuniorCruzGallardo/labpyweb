from django.shortcuts import render
# En la vista se debe considera el modelo que se va usar
from .models import Cliente
from .models import Producto
from .forms import ProductoCreateForm

# consulta_clientes es la vista que muestra la lista
def consulta_clientes(request):
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
    return render(request, 'venta\lista_clientes.html', context)

from .forms import ClienteCreateForm, ClienteUpdateForm
from django.contrib import messages
from django.shortcuts import redirect

def crear_cliente(request):
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

def actualizar_cliente(request):
    cliente = None
    dni_buscado = None
    form = None

    if request.method == 'POST':
        if 'buscar' in request.POST:
            # Buscar el cliente por DNI
            dni_buscado = request.POST.get('dni_busqueda')
            if dni_buscado:
                try: # intentar considerar la busqueda del cliente
                    # Obtener un objeto del tipo cliente
                    cliente = Cliente.objects.get(id_cliente=dni_buscado)
                    # Crear un formulario con los datos del objeto cliente
                    form = ClienteUpdateForm(instance=cliente)
                    messages.success(request, f'Cliente con DNI {dni_buscado} encontrado')
                except Cliente.DoesNotExist: # execepcion de dato no existente
                    messages.error(request, 'No se encontró Cliente con ese DNI')    
            else:
                messages.error(request, 'Por favor ingrese el DNI para buscar') 
        elif 'guardar' in request.POST:
            dni_buscado = request.POST.get('dni_busqueda') or request.POST.get('id_cliente')
            if dni_buscado:
                try:
                    cliente = Cliente.objects.get(id_cliente = dni_buscado)
                    form = ClienteUpdateForm(request.POST, instance=cliente)
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'Cliente actualizado correctamente')
                        # formulario con datos actualizados
                        cliente.refresh_from_db()
                        # devolver al formulario
                        form = ClienteUpdateForm(instance=cliente)
                    else:
                        messages.error(request, 'Error en los datos del formulario')
                except Cliente.DoesNotExist:
                    messages.error(request, 'Cliente no encontrado')
                    

            else:
                messages.error(request, 'No se puede identificar al cliente para actaualizar')
    context = {
        'form':form,
        'dni_buscado': dni_buscado,
        'cliente_encontrado': cliente is not None,
        'cliente':cliente
    }
    return render(request,'venta/u_cliente.html', context)
                     
# Eliminar clientes
def borrar_producto(request):
    productos_encontrados = []
    tipo_busqueda = 'id'
    termino_busqueda = '' # pa dentro de las cajas
    total_registros = 0

    if request.method == 'POST':
        #
        if 'consultar' in request.POST:
            # Realizar la búsqueda
            tipo_busqueda = request.POST.get('tipo_busqueda', 'id')
            termino_busqueda = request.POST.get('termino_busqueda','').strip()

            if termino_busqueda:
                # procesar
                if tipo_busqueda == 'id':
                    try:
                        producto = Producto.objects.get(id_producto = termino_busqueda)
                        productos_encontrados = [producto]
                    except Producto.DoesNotExist:
                        messages.error(request, 'No se encontró producto con ese id')    

                elif tipo_busqueda == 'nombre':
                    productos_encontrados = Producto.objects.filter(
                        nom_prod__icontains = termino_busqueda # obtener las coincidencias
                    ).order_by('id_producto') # debe estar ordenado

                    if not productos_encontrados:
                        messages.error(request, 'No se encontraron productos con ese nombre')

                total_registros = len(productos_encontrados)

                if total_registros > 0:
                    messages.success(request, f'Se encontraron {total_registros} registro(s)')        

            else:
                messages.error(request, 'Ingrese un término de búsqueda')    

        elif 'eliminar' in request.POST:
            # Eliminar cliente
            id_eliminar = request.POST.get('id_eliminar')

            if id_eliminar:
                try:
                    # buscar al cliente a eliminar
                    producto = Producto.objects.get(id_producto = id_eliminar)
                    producto.delete()
                    messages.success(request, f'producto con id {id_eliminar} eliminado correctamente')

                    # Volver a hacer la búsqueda para actualizar la lista
                    tipo_busqueda = request.POST.get('tipo_busqueda_actual', 'id')
                    termino_busqueda = request.POST.get('termino_busqueda_actual','')

                    if termino_busqueda:
                        if tipo_busqueda == 'id':
                            # Para DNI, no mostrar nada porque ya se eliminó
                            productos_encontrados = []
                        elif tipo_busqueda == 'nombre':
                            # En este caso hay que buscar nuevamente lo que queda
                            productos_encontrados = Producto.objects.filter(
                                nom_prod__icontains = termino_busqueda
                            ).order_by('id_producto')

                        total_registros = len(productos_encontrados)
                

                except Producto.DoesNotExist:
                    messages.error(request, 'producto no encontrado')
    
    context = {
        'productos_encontrados' : productos_encontrados,
        'tipo_busqueda' : tipo_busqueda,
        'termino_busqueda' : termino_busqueda,
        'total_registros' : total_registros
    }

    return render(request, 'venta/borrar_producto.html', context)


def consulta_productos(request):
    # Se requiere obtnr los datos a gestionar
    #clientes = Cliente.objects.all().order_by('ape_nom')#Data que se la que se requira
    productos = Producto.objects.all().order_by('id_producto')#Data que se la que se requira
    
    # Estos datos deben estar disponibles para una plantilla (Template)
    # Se crea un diccionario llamado context (será accesible desde la plantilla)
    context = {# en el template será objeto valor
        'productos' : productos,
        'titulo' : 'Lista de Productos'
    }
    # Se devolverá el enlace entre la plantilla y el contexto
    return render(request, 'venta\lista_productos.html', context)



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
