from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from gestor_rifa.models import Numero,Cliente
import json

class Consumirdorwebsocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.cliente = None
        await self.accept()
        await self.channel_layer.group_add(
            'numeros_disponibles',
            self.channel_name
        )
        await self.send_numeros_disponibles()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "numeros_disponibles",
            self.channel_name
        )
    
    async def recibir_seleccion(self, event):
        await self.send(text_data=json.dumps(event['content']))

    async def recibir_liberacion(self, event):
        await self.send(text_data=json.dumps(event['content']))

    async def send_numeros_disponibles(self):
        numeros = await self.get_numeros_disponibles()
        await self.send(text_data=json.dumps({'tipo': 'numeros_iniciales', 'numeros': [n['numero'] for n in numeros]}))
    
    @database_sync_to_async
    def get_numeros_disponibles(self):
        return list(Numero.objects.filter(disponible=True).values('numero'))
   
    @database_sync_to_async
    def marcar_numero_seleccionado(self, numero_id, channel_name,cliente):
        try:
            numero = Numero.objects.get(pk=numero_id, disponible=True)
            numero.disponible = False
            numero.seleccionado_por_canal = channel_name
            numero.save() # Guarda el número como no disponible y con el canal

            # Asocia el número al cliente utilizando la relación ManyToMany
            cliente.numeros.add(numero)
            return {'tipo': 'seleccionado', 'numero': numero.numero, 'canal': channel_name}
        except Numero.DoesNotExist:
            return {'tipo': 'error', 'mensaje': f'El número {numero_id} no está disponible.'}
        
    @database_sync_to_async
    def marcar_numero_liberado(self, channel_name):
        try:
            numero = Numero.objects.get(seleccionado_por_canal=channel_name)
            numero.disponible = True
            numero.seleccionado_por_canal = None
            numero.save()
            return {'tipo': 'liberado', 'numero': numero.numero}
        except Numero.DoesNotExist:
            return None 
    
    @database_sync_to_async
    def get_cliente(self, cliente_id):
        try:
            cliente = Cliente.objects.get(pk=cliente_id)
            return cliente
        except Cliente.DoesNotExist:
            return None    
    
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        tipo = data.get('tipo')
        if tipo == 'identificar_cliente':
            cliente_id = data.get('cliente_id')
            if cliente_id:
                self.cliente = await self.get_cliente(cliente_id)
            return # No necesitas enviar respuesta a este mensaje
        if tipo == 'seleccionar_numero':
            numero_id = data.get('numero_id')
            resultado = await self.marcar_numero_seleccionado(numero_id, self.channel_name,self.cliente)
            await self.channel_layer.group_send(
                "numeros_disponibles",
                {'type': 'recibir_seleccion', 'content': resultado}
            )
        elif tipo == 'liberar_numero':
            resultado = await self.marcar_numero_liberado(self.channel_name)
            if resultado:
                await self.channel_layer.group_send(
                    "numeros_disponibles",
                    {'type': 'recibir_liberacion', 'content': resultado}
                )

