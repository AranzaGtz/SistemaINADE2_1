from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractUser

# En accounts/models.py, define el modelo de usuario personalizado que tenga campos adicionales para los diferentes roles.

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

# MODELO PARA CLIENTES 
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
        return self.username

#----------------------------------------------------
# MODELO PARA PROSPECTOS
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
        return f"{self.calle} {self.numero}, {self.colonia}, {self.ciudad}, {self.estado} {self.codigo}"

# MODELO PARA EMPRESA
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100, null=False, blank=False)
    rfc = models.CharField(max_length=50, null=False, blank=True)
    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE, null=True, blank=True)
    tipo_moneda = [
        ('mxn', 'MXN - Moneda Nacional Mexicana'),
        ('usd', 'USD - Dolar Estadunidense')
    ]
    moneda = models.CharField(max_length=10, choices=tipo_moneda, blank=True, null=True)
    condiciones_pago = models.CharField(max_length=200, null=False, blank=True, default='15')

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
    telefono = models.CharField(max_length=120, blank=True)  # Agregando blank=True
    celular = models.CharField(max_length=20, blank=True)  # Agregando blank=True
    fax = models.CharField(max_length=20, blank=True)  # Agregando blank=True
    
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

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# MODELO PARA PROSPECTO
class Prospecto(Persona):
    pass

# MODELO PARA CLIENTE
class Cliente(Persona):
    pass

#----------------------------------------------------
# NUEVO MODELO PARA CONCEPTOS
#----------------------------------------------------

# MODELO PARA METODO
class Metodo(models.Model):
    nombre = models.CharField(max_length=100)# REPRESENNTA EL METODO
    leyenda = models.TextField(default="Leyenda predeterminada")# MUESTRA UNA DESCRIPCION DE LA NORMA
    def __str__(self):
        return self.nombre

# MODELO PARA SERVICIO
class Servicio(models.Model):
    servicio = models.CharField(max_length=50)# REPRESENTA EL NOMBRE DEL SERVICIO
    descripcion = models.TextField()#MUESTRA UNA DESCRIPCION DEL SERVICIO
    precio_sugerido = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.ForeignKey(Metodo, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_concepto
    
# MODELO PARA CONCEPTO
class Concepto(models.Model):
    nombre_concepto = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad_servicios = models.IntegerField()
    notas = models.TextField()

    def total(self):
        return self.cantidad_servicios * self.servicio.precio_sugerido

    def __str__(self):
        return f'{self.servicio.nombre_concepto} - {self.cantidad_servicios}'