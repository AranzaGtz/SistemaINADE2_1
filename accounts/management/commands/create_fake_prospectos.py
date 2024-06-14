from django.core.management.base import BaseCommand
from accounts.models import Empresa, Direccion, Prospecto, InformacionContacto, Titulo
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Genera datos falsos para prospectos'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Asumimos que tienes algunos títulos predefinidos
        titulos = Titulo.objects.all()
        
        for _ in range(10):  # Generar 10 registros falsos
            # Crear Dirección
            direccion = Direccion.objects.create(
                calle=fake.street_name(),
                numero=fake.building_number(),
                colonia=fake.city_suffix(),
                ciudad=fake.city(),
                codigo=fake.postcode(),
                estado=fake.state()
            )

            # Crear Empresa
            empresa = Empresa.objects.create(
                nombre_empresa=fake.company(),
                rfc=fake.ssn(),
                moneda=random.choice(['mxn', 'usd']),
                condiciones_pago=random.choice(['15', '30', '45']),
                direccion=direccion
            )

            # Crear Información de Contacto
            informacion_contacto = InformacionContacto.objects.create(
                correo_electronico=fake.email(),
                telefono=fake.phone_number(),
                celular=fake.phone_number(),
                fax=fake.phone_number()
            )

            # Crear Prospecto
            Prospecto.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                titulo=random.choice(titulos),
                empresa=empresa,
                informacion_contacto=informacion_contacto
            )

        self.stdout.write(self.style.SUCCESS('Datos falsos generados con éxito'))
