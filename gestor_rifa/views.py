import json
from django.http import JsonResponse
from django.views.generic import ListView,View,FormView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db import transaction
from .forms import Cliente_form,ComprobanteForm
from .models import Vehiculo, Numero,Cliente,Cuentas_banco

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
        if imagenes:
            context['imagenes'] = imagenes
        return context

class VerificarNumerosDisponiblesView(View):
    def post(self, request, *args, **kwargs):
        # Obtener los números seleccionados desde el body de la solicitud
        data = json.loads(request.body)
        numeros_seleccionados = data.get('numeros', [])

        # Verificar si los números están disponibles
        disponibles = []
        no_disponibles = []
        for numero in numeros_seleccionados:
            if Numero.objects.filter(numero=numero, disponible=True).exists():
                disponibles.append(numero)
            else:
                no_disponibles.append(numero)


        # Enviar una respuesta al cliente
        if len(disponibles) == len(numeros_seleccionados):
            return JsonResponse({'disponibles': True})
        else:
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
        cliente = form.save()
        self.request.session['cliente_id'] = cliente.id
        return super().form_valid(form)
    
class SeleccionarNumeroView(View):
    template_name = 'view/tabla.html'

    def get(self, request):
        if 'cliente_id' not in request.session:
            return redirect('cliente')
        
        numeros = Numero.objects.filter(disponible=True).order_by('numero')

        paginator = Paginator(numeros, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'numeros': page_obj})
    
    def post(self, request):
        numeros_seleccionados = request.POST.get('numeros_seleccionados', '')
        
        if numeros_seleccionados:
            lista_numeros = [int(n) for n in numeros_seleccionados.split(',') if n.isdigit()]
        return redirect('subir_comprobante')

class SubirComprobanteView(View):
    template_name = 'view/pago.html'

    def get(self, request):
        # or 'numero_id' not in request.session
        if 'cliente_id' not in request.session :
            return redirect('cliente')
        cuentas = Cuentas_banco.objects.all()
        form = ComprobanteForm()
        return render(request, self.template_name, {'form': form, 'cuentas':cuentas})

    # def form_valid(self, form):
    #     cliente_id = self.request.session.get('cliente_id')
    #     numero_id = self.request.session.get('numero_id')

    #     if not cliente_id or not numero_id:
    #         return redirect('cliente_form')

    #     cliente = Cliente.objects.create(**cliente_id)
    #     numero = Numero.objects.get(id=numero_id)
    #     cliente.numeros.add(numero)
    #     numero.disponible = False
    #     numero.save()

    #     comprobante = form.save(commit=False)
    #     comprobante.cliente = cliente
    #     comprobante.rifa = numero.rifa
    #     comprobante.save()

    #     # Limpiar la sesión
    #     self.request.session.pop('cliente_id')
    #     self.request.session.pop('numero_id')

    #     return super().form_valid(form)