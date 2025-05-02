import json
from django.http import JsonResponse
from django.views.generic import ListView,View,FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import now
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import Cliente_form,ComprobanteForm
from .models import Vehiculo, Numero,Cliente,Cuentas_banco
from utils.validators_img import validar_formato_imagen

TIEMPO_EXPIRACION = timezone.timedelta(hours=2)

def probar_expiracion(request,timestamp_registro,cliente_id):
    try:
        tiempo_registro = timezone.datetime.fromisoformat(timestamp_registro)
        if timezone.is_naive(tiempo_registro):
            tiempo_registro = timezone.make_aware(tiempo_registro)
    except Exception as e:
        request.session.flush()
        Cliente.objects.get(pk=cliente_id).delete()
        return redirect('cliente')

        # Verifica si el tiempo ha expirado         
    tiempo_transcurrido = timezone.now() - tiempo_registro
    if tiempo_transcurrido > TIEMPO_EXPIRACION:
        try:
            Cliente.objects.get(pk=cliente_id).delete()
            print("Cliente eliminado por tiempo de espera")
        except Cliente.DoesNotExist:
            pass
            print("cliente no existe")
            
            request.session.flush()
            return redirect('cliente')
    return None 

class Presentacion(ListView):
    model = Vehiculo
    template_name = 'vehiculo/vehiculo.html'
    context_object_name = 'vehiculos'
    ordering = ['id'] 
    def get_queryset(self):
        return Vehiculo.objects.filter(rifa__activa=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imagenes = Vehiculo.objects.first().imagenes_secundarias.all() if Vehiculo.objects.exists() else None
        mensaje = "Hola, estoy interesado en comprar un boleto de la rifa. ¿Podrías ayudarme?";
        if imagenes:
            context['imagenes'] = imagenes
        return context

class VerificarNumerosDisponiblesView(View):
    def post(self, request, *args, **kwargs):
        # Obtener los números seleccionados desde el body de la solicitud
        data = json.loads(request.body)
        numeros_seleccionados = data.get('numeros', [])
        cliente_id = request.session.get('cliente_id')
        print(cliente_id)
        time = data.get('time_stamp', None)
        # Verificar si los números están disponibles
        redireccion = probar_expiracion(request,time,cliente_id)
        if redireccion:
            print(redireccion,"redireccion")
            return redireccion
        disponibles = []
        no_disponibles = []
        for numero in numeros_seleccionados:
            if Numero.objects.filter(numero=numero, disponible=True).exists():
                disponibles.append(numero)
            else:
                no_disponibles.append(numero)


        # Enviar una respuesta al cliente
        if len(disponibles) == len(numeros_seleccionados):
            self.request.session['numeros'] = disponibles
            return JsonResponse({'disponibles': True})
        else:
           self.request.session.pop('numeros', None)  # Limpiar la sesión si no están todos disponibles
           return JsonResponse({
                'disponibles': False,
                'no_disponibles': no_disponibles
            })

class ClienteFormView(FormView):
    template_name = 'view/cliente_form.html'
    form_class = Cliente_form
    success_url = reverse_lazy('seleccionar_numero')

    def get(self, request, *args, **kwargs):
        # Verifica si ya existen los datos del cliente en la sesión
        cliente_id = request.session.get('cliente_id')
        
        if cliente_id:
            try:
                # Intenta obtener el cliente por el id de la sesión y verificar que esté activo
                cliente = Cliente.objects.get(pk=cliente_id, estado=True)
            except Cliente.DoesNotExist:
                # Si no existe el cliente o no está activo
                pass                
            # Si el cliente existe y está activo, redirige al success_url
            return redirect(self.success_url)
        
        # Si no existe el cliente_id en la sesión, procede con el flujo normal
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        # Normaliza la cédula antes de validar
        cedula_limpia = form.cleaned_data['cedula'].replace('.', '').replace(',', '')

        # Verifica si ya existe otra instancia con esa cédula
        if Cliente.objects.filter(cedula=cedula_limpia).exists():
            form.add_error('cedula', 'Ya existe un cliente con esta cédula (sin importar el formato).')
            return super().form_invalid(form)

        # Asigna la cédula normalizada al objeto pero aún no se guarda en la BD
        cliente = form.save(commit=False)
        cliente.cedula = cedula_limpia
        cliente.save()

        # Guarda en sesión y continúa
        self.request.session['cliente_id'] = cliente.id
        self.request.session['timestamp_registro'] = now().isoformat()
        return super().form_valid(form)

class Busqueda_cliente(View):
    def get(self, request,dni):
        cedula = dni.replace('.', '').replace(',', '')

        if not cedula:
            return JsonResponse({'error': 'Cédula no proporcionada'}, status=400)

        try:
            cliente = get_object_or_404(Cliente, cedula=cedula)
            request.session['cliente_id'] = cliente.id
            request.session['timestamp_registro'] = now().isoformat()
            return JsonResponse({
                'id': cliente.id,
                'estado': True
            })
        except Exception as e:
            return JsonResponse({'error': 'Cliente no encontrado'}, status=404)


class SeleccionarNumeroView(View):
    template_name = 'view/tabla.html'

    def get(self, request):
        cliente_id = request.session.get('cliente_id')
        timestamp_registro = request.session.get('timestamp_registro')
        numeros = request.session.get('numeros')
        numero_post = request.GET.get('numeros')
        if numeros and numero_post == None:
            request.session.pop('numeros', None)  # Limpiar la sesión si no están todos disponibles
        # Si no hay cliente, redirige a crear cliente
        if not cliente_id:
            return redirect('cliente')

        # Si no hay timestamp, también redirige (algo falló en el registro)
        if not timestamp_registro:
            request.session.flush()
            return redirect('cliente')

        # Intenta convertir el timestamp en fecha
        redireccion = probar_expiracion(request,timestamp_registro,cliente_id)

        if redireccion:
            return redireccion
        # Si todo está bien, muestra los números disponibles
        numeros = Numero.objects.all().order_by('numero')
        paginator = Paginator(numeros, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'numeros': page_obj})

    
    def post(self, request):
        cliente_id = request.session.get('cliente_id')
        timestamp_registro = request.session.get('timestamp_registro')
        if not cliente_id:
            return redirect('cliente')

        # Si no hay timestamp, también redirige (algo falló en el registro)
        if not timestamp_registro:
            request.session.flush()
            return redirect('cliente')
        
        redireccion = probar_expiracion(request,timestamp_registro,cliente_id)
        
        if redireccion:
            return redireccion
        numeros_seleccionados = request.POST.get('numeros')
        if numeros_seleccionados:
            lista_numeros = [int(n) for n in numeros_seleccionados.split(',') if n.isdigit()]
            print(lista_numeros,"lista numeros")
        return redirect('subir_comprobante')

class SubirComprobanteView(View):
    template_name = 'view/pago.html'

    def get(self, request):
        # or 'numero_id' not in request.session
        if 'cliente_id' not in request.session:
            return redirect('cliente')
        if 'numeros' not in request.session:
            return redirect('seleccionar_numero')
        print(request.session['numeros'], 'comprobante')
        timestamp_registro = request.session.get('timestamp_registro')
        redirecion = probar_expiracion(request,timestamp_registro,request.session['cliente_id'])
        if redirecion:
            return redirecion
        
        cuentas = Cuentas_banco.objects.all()
        form = ComprobanteForm()
        
        
        return render(request, self.template_name, {'form': form, 'cuentas':cuentas})

    def post(self, request):
        if 'cliente_id' not in request.session or 'numeros' not in request.session:
            return redirect('cliente')
        form = ComprobanteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente_id = request.session.get('cliente_id')
            numeros = request.session.get('numeros')
            
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                request.session.flush()
                return redirect('cliente')
            imagen_comprobante = request.FILES.get('imagen_comprobante')
            if imagen_comprobante:
                try:
                    validar_formato_imagen(imagen_comprobante)
                except ValidationError as e:
                    # Si la validación falla, agrega el error al formulario y vuelve a renderizar
                    form.add_error('imagen_comprobante', e)
                    return self.form_invalid(form) # Re-renderiza el formulario con errores
            comprobante = form.save(commit=False)
            comprobante.cliente = cliente
            comprobante.estado = 'pendiente' 
            try:
                primer_numero = Numero.objects.get(numero=numeros[0])
                comprobante.rifa = primer_numero.rifa
            except (IndexError, Numero.DoesNotExist):
                request.session.flush()
                return redirect('cliente')
            comprobante.save()
            form.save_m2m()
            with transaction.atomic():
                for numero_id in numeros:
                    try:
                        numero = Numero.objects.get(numero=numero_id)
                        cliente.numeros.add(numero)
                        numero.disponible = False
                        numero.save()
                    except Numero.DoesNotExist:
                        # Loggear o manejar el caso en que un número desapareció
                        pass
            # Limpiar la sesión
            cliente.activo = True
            cliente.save() 
            request.session.flush()

            messages.success(request, "se ha subido el comprobante de pago correctamente espera a que sea verificado")
            
            return redirect('inicio')
        else:
            messages.error(request, "Error al subir el comprobante de pago. Verifica los datos e intenta nuevamente.")
            return render(request, 'errors/404.html', {'form': form})
    
