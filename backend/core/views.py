from django.http import HttpResponseRedirect

def index(request, path=''):
    # Aquí definimos los prefijos de las rutas que deben permanecer en Django (ej. DRF).
    api_prefixes = ['api', 'admin', 'media']  # Puedes agregar más prefijos según lo necesites.
    
    # Obtenemos la primera parte de la ruta solicitada.
    path_prefix = path.split('/')[0]
    
    # Si la ruta solicitada empieza con un prefijo de API, no redirige.
    if path_prefix in api_prefixes:
        return None  # Deja que Django maneje la ruta.

    # De lo contrario, redirige a la ruta en Vite.
    return HttpResponseRedirect(f'http://127.0.0.1:5173/{path}')
