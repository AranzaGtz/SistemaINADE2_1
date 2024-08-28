import base64

# Rutas de los archivos .cer y .key
certificate_path = 'CSD_Sucursal_1_EKU9003173C9_20230517_223850.cer'
private_key_path = 'CSD_Sucursal_1_EKU9003173C9_20230517_223850.key'

# Leer y codificar el archivo .cer
with open(certificate_path, 'rb') as cert_file:
    certificate_content = cert_file.read()
certificate_base64 = base64.b64encode(certificate_content).decode()

# Leer y codificar el archivo .key
with open(private_key_path, 'rb') as key_file:
    private_key_content = key_file.read()
private_key_base64 = base64.b64encode(private_key_content).decode()

# Imprimir los valores codificados
print("Certificado en Base64:")
print(certificate_base64)
print("Clave Privada en Base64:")
print(private_key_base64)