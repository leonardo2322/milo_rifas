from django.views.generic import ListView,View,FormView
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



class ConfirmarNumerosView(View):
    def post(self, request):
        numero_ids = request.session.get('numeros_seleccionados', [])

        if not numero_ids:
            # No hay selección
            return redirect('seleccionar_numero')

        try:
            with transaction.atomic():
                # Bloqueamos solo los registros seleccionados
                numeros = Numero.objects.select_for_update().filter(id__in=numero_ids)

                # Verificamos que todos estén disponibles
                for numero in numeros:
                    if not numero.disponible:
                        raise Exception(f"El número {numero.numero} ya fue tomado")

                # Si todo va bien, los marcamos como no disponibles
                for numero in numeros:
                    numero.disponible = False
                    numero.save()

                # Aquí podrías guardar en la base de datos la relación con el cliente

        except Exception as e:
            # Puedes mostrar un mensaje o redirigir con feedback
            print(e)
            return redirect('seleccionar_numero')

        return redirect('subir_comprobante')


class ClienteFormView(FormView):
    template_name = 'view/cliente_form.html'
    form_class = Cliente_form
    success_url = reverse_lazy('seleccionar_numero')

    def get(self, request, *args, **kwargs):
        # Verifica si ya existen los datos del cliente en la sesión
        if 'cliente_data' in request.session:
            try:
                cliente = Cliente.objects.get(pk=request.session['cliente_id'])
            except Cliente.DoesNotExist:
                print("error el usuario no existe: ", request.session['cliente_id'])
            # Si existen, redirige al success_url
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        cliente = form.save()
        self.request.session['cliente_data'] = cliente.id
        return super().form_valid(form)
    
class SeleccionarNumeroView(View):
    template_name = 'view/tabla.html'

    def get(self, request):
        if 'cliente_data' not in request.session:
            return redirect('cliente')
        numeros = Numero.objects.filter(disponible=True).order_by('numero')

        paginator = Paginator(numeros, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'numeros': page_obj})
    
    def post(self, request):
        numero_id = request.POST.get('pk')
        request.session['numero_id'] = numero_id
        return redirect('subir_comprobante')

class SubirComprobanteView(View):
    template_name = 'view/pago.html'

    def get(self, request):
        # or 'numero_id' not in request.session
        if 'cliente_data' not in request.session :
            return redirect('cliente')
        cuentas = Cuentas_banco.objects.all()
        form = ComprobanteForm()
        return render(request, self.template_name, {'form': form, 'cuentas':cuentas})

    # def form_valid(self, form):
    #     cliente_data = self.request.session.get('cliente_data')
    #     numero_id = self.request.session.get('numero_id')

    #     if not cliente_data or not numero_id:
    #         return redirect('cliente_form')

    #     cliente = Cliente.objects.create(**cliente_data)
    #     numero = Numero.objects.get(id=numero_id)
    #     cliente.numeros.add(numero)
    #     numero.disponible = False
    #     numero.save()

    #     comprobante = form.save(commit=False)
    #     comprobante.cliente = cliente
    #     comprobante.rifa = numero.rifa
    #     comprobante.save()

    #     # Limpiar la sesión
    #     self.request.session.pop('cliente_data')
    #     self.request.session.pop('numero_id')

    #     return super().form_valid(form)