# CentroTIC

Este proyecto hace referencia a las aplicaciones de:

* Diplomado IoT
* KIT PRAES
* Protocolo PAWS con SDR
* Nariz Electronica Version I
* Nariz Electronica Version II
* Sistemas GRIPV
* E3Tratos

Para lanzar el proyecto se requiere realizar los siguiente:

Usuarios Linux

* 1) Clonar el repositorio: `` git clone https://github.com/LuisDiazM/CentroTIC.git ``
* 2) Crear un entorno virtual con virtualenv `` virtualenv -p python3 env_centrotic ``
* 3) Activar el entorno virtual `` source env_centrotic/bin/activate ``
* (Para desactivar el entorno virtual ``deactivate``)
* 4) Instalar los paquetes pip del archivo requeriments.txt `` pip install -r requeriments.txt``
* 5) Instalar postgresql ``sudo apt-get install postgresql``
* 6) Ingresar al usuario postgres ``sudo su postgres``
* 7) Item Abrir postgres usando ``psql``
* 8) Crear una contraseña al usuario postgres `` \password postgres ``
* 9) Crear una base de datos vacía ``CREATE DATABASE centrotic;``
* 10) Salir ``\q``
* 11) ``exit``
* 12) Realizar las migraciones ``python manage.py makemigrations`` 
* 13) ``python manage.py migrate``
* Lanzar el servidor ``python manage.py runserver``

Ahora puede disfrutar del proyecto de manera local.

Usuarios Windows
* Instalar git bash
* Instalar vagrant
* Instalar Virtualbox
* Abrir una terminal de git bash
* Clonar el repositorio `` git clone https://github.com/LuisDiazM/CentroTIC.git ``
* ``cd CentroTIC``
* ``vagrant init``
Estos comandos se ejecutan después de tener todo instalado
* ``vagrant up``
* ``vagrant ssh`` 
* Repetir los pasos 6-13 para usuarios linux
* Lanzar el servidor ``python manage.py runserver 0.0.0.0:8080`` 

## Nota importante
Para acceder a los archivos desde linux sólo requiere ingresar a la consola de git bash ``cd /vagrant/src/`` y encontrará el proyecto django que ejecutará