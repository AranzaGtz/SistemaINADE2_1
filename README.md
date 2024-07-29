# SistemaINADE3

Este es un proyecto Django. Siga las siguientes instrucciones para configurarlo en su máquina local.

## Requisitos

- Python 3.x
- pip

## Instalación

1. **Clonar el repositorio**:

   ```sh
   git clone https://github.com/AranzaGtz/SistemaINADE2.git
   cd SistemaINADE2
   ```

2. **Crear y activar un entorno virtual** (opcional pero recomendado):

   - Crear el entorno virtual:

     ```sh
     python -m venv venv
     ```

   - Activar el entorno virtual:

     - En macOS y Linux:

       ```sh
       source venv/bin/activate
       ```

     - En Windows:

       ```sh
       venv\Scripts\activate
       ```

3. **Instalar las dependencias**:

   - Instalar [Homebrew](https://brew.sh/)::

      ```sh
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
   - Instalar las dependencias necesarias para WeasyPrint:

      ```sh
      brew install pango gdk-pixbuf cairo libffi
      ```
   - Agregar Dependencias al `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```

4. **Realizar las migraciones de la base de datos**:

   ```sh
   python manage.py migrate
   ```

5. **Ejecutar el servidor de desarrollo**:

   ```sh
   python manage.py runserver
   ```

## Uso

Para acceder al proyecto, abra su navegador web y vaya a `http://127.0.0.1:8000/`.

---
¡Gracias por usar nuestro proyecto!
