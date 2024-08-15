from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _

#----------------------------------------------------
# MODELO PARA CLIENTES
#----------------------------------------------------

# MODELO PARA USUARIOS ADMINISTRADORES
class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, first_name=None, last_name=None, celular=None, rol=None, **extra_fields):
        
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario.')
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico.')
        
        email = self.normalize_email(email)
        
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, celular=celular, rol=rol, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        
        # Campos opcionales para crear super usuario 
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('celular', '')
        extra_fields.setdefault('rol', 'admin')
        
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# MODELO PARA USUARIOS NORMALES
class CustomUser(AbstractUser):
    
    # username = models.CharField(max_length=150, unique=True)
    # nombre = models.CharField(max_length=100)
    # apellido = models.CharField(max_length=100)
    # correo = models.EmailField(unique=True)
    # ESTOS YA ESTAN AGREGADOS EN LA TABLA PREDETERMINADA DE USER
    
    celular = models.CharField(max_length=15, blank=True, null=True)
    
    AREA_CHOICES = [
        ('admin', 'Administrador'),
        ('coordinador', 'Coordinador'),
        ('muestras', 'Muestras'),
        ('informes', 'Informes'),
        ('laboratorio', 'Laboratorio'),
        ('calidad', 'Calidad')
    ]
    rol = models.CharField(max_length=20, choices=AREA_CHOICES, blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} | {self.username}"

#----------------------------------------------------
# MODELO PARA NOTIFICACIONES
#----------------------------------------------------
class Notificacion(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True )
    tipo = models.CharField(max_length=100)
    mensaje = models.TextField()
    enlace = models.URLField()
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        
#----------------------------------------------------
# MODELO PARA EMPRESAS
#----------------------------------------------------
# MODELO PARA DIRECCION
class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=50, null=False, blank=False)
    numero = models.CharField(max_length=50, null=False, blank=False)
    colonia = models.CharField(max_length=100, null=False, blank=False)
    ciudad = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=6, null=False, blank=False)
    estado = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return f"{self.calle}, No.{self.numero}, Col. {self.colonia}, {self.ciudad}, {self.estado}, C.P. {self.codigo}"

# MODELO PARA EMPRESA
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100, null=False, blank=False)
    rfc = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    tipo_moneda = [
        ('MXN', 'MXN - Moneda Nacional Mexicana'),
        ('USD', 'USD - Dolar Estadunidense')
    ]
    moneda = models.CharField(max_length=10, choices=tipo_moneda, blank=True, null=True)
    condiciones_pago = models.CharField(max_length=200, null=False, blank=True, default='15')
    
    def __str__(self):
        return self.nombre_empresa

#----------------------------------------------------
# MODELO PARA CLIENTES
#----------------------------------------------------
# MODELO DE TITULOS
class Titulo(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50, null=False, blank=False)
    abreviatura = models.CharField(max_length=10, null=False, blank=False)
    
    def __str__(self):
        return self.titulo

# MODELO PARA INFORMACION DE CONTACTO
class InformacionContacto(models.Model):
    id = models.AutoField(primary_key=True)
    correo_electronico = models.EmailField(null=False, blank=False)
    telefono = models.CharField(max_length=120, null=True, blank=True)  # Agregando blank=True
    celular = models.CharField(max_length=20, null=True, blank=True)  # Agregando blank=True
    fax = models.CharField(max_length=20,null=True, blank=True)  # Agregando blank=True
    
    def __str__(self):
        return f"{self.correo_electronico} - {self.telefono} / {self.celular}"

# MODELO BASE PARA PERSONA
class Persona(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellidos = models.CharField(max_length=100, null=False, blank=False)
    titulo = models.ForeignKey(Titulo, on_delete=models.SET_NULL, null=True, blank=True)  # null=True
    informacion_contacto = models.ForeignKey(InformacionContacto, on_delete=models.SET_NULL, null=True, blank=True)  # null=True
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.empresa.nombre_empresa} | {self.nombre} {self.apellidos}"
    
# MODELO PARA PROSPECTO
class Prospecto(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='prospecto')

#----------------------------------------------------
# MODELO PARA COTIZACIONES
#----------------------------------------------------

# MODELO DE COTIZACION
TIPO_DE_CAMBIO = Decimal('18.0')

class Cotizacion(models.Model):
    id_personalizado = models.CharField(max_length=4, unique=True, null=True, blank=True)
    fecha_solicitud = models.DateField(null=True, blank=True)
    fecha_caducidad = models.DateField(null=True, blank=True)
    tipo_moneda = [
        ('MXN', 'MXN - Moneda Nacional Mexicana'),
        ('USD', 'USD - Dolar Estadunidense')
    ]
    metodo_pago = models.CharField(max_length=100, choices=tipo_moneda)
    opciones_iva = [
        ('0.08', '8%'),
        ('0.16', '16%')
    ]
    tasa_iva = models.CharField(max_length=4, choices=opciones_iva)
    notas = models.TextField(blank=True, null=True)
    correos_adicionales = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    iva = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # CLIENTE
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, blank=True, null=True)
    estado = models.BooleanField(default=False)  # False para "No Aceptado", True para "Aceptado"
    cotizacion_pdf = models.FileField(upload_to='cotizaciones_pdfs/', null=True, blank=True)
    orden_pedido_pdf = models.FileField(upload_to='ordenes_pedido_pdfs/', null=True, blank=True)

    def calculate_subtotal(self):
        factor = Decimal('1.0') if self.metodo_pago == 'MXN' else TIPO_DE_CAMBIO
        return sum(Decimal(concepto.cantidad_servicios) * Decimal(concepto.precio) * factor for concepto in self.conceptos.all())

    def calculate_iva(self):
        # Convert tasa_iva to Decimal before multiplying
        tasa_iva_decimal = Decimal(self.tasa_iva)
        return self.subtotal * tasa_iva_decimal

    def calculate_total(self):
        return self.subtotal + self.iva

    def save(self, *args, **kwargs):
        if not self.id_personalizado:
            self.id_personalizado = self.generate_new_id_personalizado()
        if not self.fecha_solicitud:
            self.fecha_solicitud = timezone.now()
        if not self.fecha_caducidad:
            self.fecha_caducidad = self.fecha_solicitud + timezone.timedelta(days=1)
        # Save the instance first to get the primary key
        super(Cotizacion, self).save(*args, **kwargs)
        # Now that the instance has a primary key, calculate the derived values
        self.subtotal = self.calculate_subtotal()
        self.iva = self.calculate_iva()
        self.total = self.calculate_total()
        # Save again to update the calculated values
        super(Cotizacion, self).save(*args, **kwargs)

    def generate_new_id_personalizado(self, formato):
        last_cotizacion = Cotizacion.objects.order_by('id').last()
        new_id = '0001' if not last_cotizacion else str(int(last_cotizacion.id_personalizado) + 1).zfill(4)
        year = timezone.now().year
        return formato.format(year=year, seq=new_id)

    def save(self, *args, **kwargs):
        configuracion = ConfiguracionSistema.objects.first()
        
        if configuracion:
            if not self.tipo_moneda:
                self.tipo_moneda = configuracion.moneda_predeterminada
            if not self.tasa_iva:
                self.tasa_iva = configuracion.tasa_iva_default
            if not self.id_personalizado:
                self.id_personalizado = self.generate_new_id_personalizado(configuracion.formato_numero_cotizacion)
        
        if not self.fecha_solicitud:
            self.fecha_solicitud = timezone.now()
        if not self.fecha_caducidad:
            self.fecha_caducidad = self.fecha_solicitud + timezone.timedelta(days=1)

        super(Cotizacion, self).save(*args, **kwargs)
        
        # Calcular y guardar los valores derivados
        self.subtotal = self.calculate_subtotal()
        self.iva = self.calculate_iva()
        self.total = self.calculate_total()
        
        super(Cotizacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_personalizado
    
    
#----------------------------------------------------
# MODELO PARA CONCEPTOS
#----------------------------------------------------

# MODELO PARA METODO
class Metodo(models.Model):
    metodo = models.CharField(max_length=50,unique=True)# REPRESENNTA EL METODO
    def __str__(self):
        return self.metodo

# MODELO PARA SERVICIO
class Servicio(models.Model):
    metodo = models.ForeignKey(Metodo,on_delete=models.SET_NULL, null=True)
    nombre_servicio = models.CharField(max_length=100)# REPRESENTA EL NOMBRE DEL SERVICIO
    precio_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()#MUESTRA UNA DESCRIPCION DEL SERVICIO
    subcontrato = models.BooleanField(default=False) # False para "No sub contrato", True para "sub contrato"
    acreditado = models.BooleanField(default=True) # False para "No acreditado", Ture para "Acreditado"

    def save(self, *args, **kwargs):
        if self.precio_sugerido <= 0:
            self.precio_sugerido = 1
        super(Servicio, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre_servicio} / {self.metodo}"
    
# MODELO PARA CONCEPTO
class Concepto(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, related_name='conceptos', on_delete=models.CASCADE)
    cantidad_servicios = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.TextField(null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT)
    subcontrato = models.BooleanField(default=False) # False para "No sub contrato", True para "sub contrato"
    
    def save(self, *args, **kwargs):
        if self.precio <= 0:
            self.precio = self.servicio.precio_sugerido
        if self.cantidad_servicios <= 0:
            self.cantidad_servicios = 1
        super(Concepto, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.cotizacion} - {self.cantidad_servicios} - {self.servicio} - {self.precio} - {self.notas}"

#----------------------------------------------------
# MODELO PARA ORDENES DE TRABAJO
#----------------------------------------------------

class OrdenTrabajo(models.Model):
    id_personalizado = models.CharField(max_length=20, unique=True, blank=True, primary_key=True)  
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='orden_trabajo')
    receptor = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='ordenes_trabajo')
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, null=True, blank=True, related_name='ordenes_trabajo')
    estado = models.BooleanField(default=False)  # False para "No terminado", True para "Terminado"
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    gestion = models.BooleanField(default=False) # False para "No gestion", True para "Gestion"
    orden_trabajo_pdf = models.FileField(upload_to='ordenes_trabajo_pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id_personalizado:
            self.id_personalizado = self.generate_id_personalizado()
        super(OrdenTrabajo, self).save(*args, **kwargs)

    def generate_id_personalizado(self):
        today = datetime.today()
        date_str = today.strftime('%y%m%d')
        count = OrdenTrabajo.objects.filter(fecha_creacion__date=today.date()).count() + 1
        return f'{date_str}-{str(count).zfill(2)}'

    def __str__(self):
        return f'Orden de Trabajo {self.id_personalizado} para Cotización {self.cotizacion.id_personalizado}'
    
class OrdenTrabajoConcepto(models.Model):
    orden_de_trabajo = models.ForeignKey(OrdenTrabajo, related_name='conceptos', on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)

#----------------------------------------------------
# MODELO PARA MI ORGANIZACIÓN
#----------------------------------------------------

# MODELO PARA FORMATO DE COTIZACIÓN
class FormatoCotizacion (models.Model):
    nombre_formato = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    emision = models.DateField(default=timezone.now)
    terminos = models.TextField(blank=True)  # Campo para términos
    avisos = models.TextField(blank=True)    # Campo para avisos
    
# MODELO PARA FORMATO DE ORDEN DE TRABAJO
class FormatoOrden (models.Model):
    nombre_formato = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    emision = models.DateField(default=timezone.now)

# MODELO PARA ORGANIZACION
class Organizacion(models.Model):
    nombre = models.CharField(max_length=255, default='Ingenieria y Administración Estratégica, S.A. de C.V.')
    slogan = models.CharField(max_length=255, blank=True, null=True)  # Slogan opcional
    direccion = models.CharField(max_length=255, default='Calle Puebla, No. 4990, col. Guillen, Tijuana BC, México, C.P. 22106')
    telefono = models.CharField(max_length=20, default='(664) 104 51 44')
    pagina_web = models.URLField()
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # Campo para el logo
    f_cotizacion = models.ForeignKey(FormatoCotizacion, related_name='formatos', on_delete=models.CASCADE, null=True)
    f_orden = models.ForeignKey(FormatoOrden, related_name='formatos', on_delete=models.CASCADE, null=True)
    
    
    def __str__(self):
        return self.nombre

#----------------------------------------------------
# MODELO PARA CONFIGURACIÓN GENERAL DEL SISTEMA
#----------------------------------------------------

class ConfiguracionSistema(models.Model):
    moneda_predeterminada = models.CharField(
        max_length=10,
        choices=[
            ('MXN', 'MXN - Moneda Nacional Mexicana'),
            ('USD', 'USD - Dolar Estadunidense')
        ],
        default='MXN',
        verbose_name=_("Moneda Predeterminada")
    )
    opciones_iva = [
        ('0.08', '8%'),
        ('0.16', '16%')
    ]
    tasa_iva_default = models.CharField(
        max_length=4, 
        choices=opciones_iva, 
        default='0.08',
        verbose_name=_("Tasa de IVA Predeterminada")
    )
    formatos_cotizacion = [
        ('COT-{year}-{seq}', 'COT-{year}-{seq}'),
        ('{year}-COT-{seq}', '{year}-COT-{seq}'),
        ('COT-{seq}', 'COT-{seq}'),
        ('{seq}', '{seq}')
    ]
    formato_numero_cotizacion = models.CharField(
        max_length=50, 
        choices=formatos_cotizacion,
        default='{seq}',
        verbose_name=_("Formato de Número de Cotización")
    )
    
    def __str__(self):
        return "Configuración General del Sistema"

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"

#----------------------------------------------------
# MODELO PARA QUEJAS
#----------------------------------------------------

# MODELO PARA QUEJAS
class Queja(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asunto