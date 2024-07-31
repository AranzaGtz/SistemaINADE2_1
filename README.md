# SistemaINADE2.1

Este es un proyecto Django. Siga las siguientes instrucciones para configurarlo en su máquina local.

## Requisitos

- Python 3.x
- pip
- Homebrew (opcional pero recomendado para algunas dependencias)

## Instalación

### 1. Clonar el repositorio:

   ```sh
   git clone https://github.com/AranzaGtz/SistemaINADE2.git
   cd SistemaINADE2
   ```

### 2. Crear y activar un entorno virtual (opcional pero recomendado):

   - Crear el entorno virtual:

     ```sh
     python -m venv venv
     ```

   - En macOS y Linux:

      ```sh
      source venv/bin/activate
      ```

   - En Windows:

      ```sh
      venv\Scripts\activate
      ```

### 3. Instalar las dependencias:

   - Instalar Homebrew (opcional):

      ```sh
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```

   - Añadir Homebrew a tu PATH:

      ```sh
      (echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"') >> /home/ubuntu/.bashrc
      eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
      ``
   - Instalar las dependencias necesarias para WeasyPrint:

      ```sh
      brew install pango gdk-pixbuf cairo libffi
      ```
   
   - Si estás en un sistema Ubuntu, también puedes instalar estas dependencias del sistema:
      
      ```sh
      sudo apt-get install -y libcairo2-dev libjpeg-dev libgif-dev librsvg2-dev
      ```

   - Configurar PKG_CONFIG_PATH y LD_LIBRARY_PATH:
   
      ```sh
      export PKG_CONFIG_PATH=/home/linuxbrew/.linuxbrew/lib/pkgconfig
      export LD_LIBRARY_PATH=/home/linuxbrew/.linuxbrew/lib

      echo 'export PKG_CONFIG_PATH=/home/linuxbrew/.linuxbrew/lib/pkgconfig' >> ~/.bashrc
      echo 'export LD_LIBRARY_PATH=/home/linuxbrew/.linuxbrew/lib' >> ~/.bashrc
      source ~/.bashrc
      ```

   - Instalar las dependencias del proyecto desde requirements.txt:

      ```sh
      pip install -r requirements.txt
      ```


### 4. Realizar las migraciones de la base de datos:

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

### 5. Ejecutar el servidor de desarrollo:

   ```sh
   python manage.py runserver
   ```

## Uso

Para acceder al proyecto, abra su navegador web y vaya a http://127.0.0.1:8000/.


---
¡Gracias por usar nuestro proyecto!
