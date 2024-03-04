# Proyecto: Topicos de Telemática ST0263

## Estudiante
- **Nombre:** Juan Pablo Ramirez
- **Correo Electrónico:** jurami35@eafit.edu.co

## Profesor
- **Nombre:** Alvaro Enrique Ospina Sanjuan
- **Correo Electrónico:** aeospinas@eafit.edu.co

## Descripción
Este proyecto aborda el desafío 1-2, que consiste en establecer una comunicación entre procesos utilizando API REST y RPC. El objetivo principal es crear una estructura de red Peer-to-Peer (P2P) no estructurada y gestionarla de manera centralizada, con el fin de comprender su funcionamiento y arquitectura. Este enfoque permite explorar cómo se establecen las conexiones entre los middleware y los demás componentes del sistema, así como facilitar la comunicación entre cliente y servidor. Ejemplos de estructuras similares incluyen Utorrent, Ares, Skype, entre otros.

## Aspectos que no se Cumplieron
Aunque el proyecto presenta avances significativos, hay algunos aspectos que no se cumplieron totalmente:
- No se realizó el despliegue en AWS Academy.
- Se utilizan diccionarios y listas para simular la base de datos, en lugar de implementar un sistema de gestión de bases de datos.
- Aunque algunos servicios indican ingresar contraseñas e IPs, no se implementó un nivel de seguridad adecuado en el proyecto.

# Arquitectura
![image](https://github.com/juanxv/jurami-ST0263/assets/44956232/a9ec66c0-3aa0-4849-81a9-cf5b2096c4cf)
# Proyecto: Comunicación entre Procesos - Arquitectura Peer-to-Peer

## Descripción
Este proyecto implementa una arquitectura Peer-to-Peer (P2P) no estructurada centralizada, en la cual los peers se conectan a un servidor central para compartir y buscar archivos. El servidor actúa como un catálogo que almacena información sobre la ubicación de los archivos, pero no los contiene físicamente. Cuando un peer desea descargar un archivo, el servidor le proporciona la información necesaria para conectarse a otro peer que posea el archivo deseado.

### Funcionamiento
1. **Login de Peers:** Los peers se registran en el servidor al hacer login y luego indexan sus archivos para que el servidor conozca qué archivos poseen.
2. **Búsqueda de Archivos:** Un peer puede buscar archivos en el servidor, el cual le proporcionará la información de cómo obtenerlos de otros peers.
3. **Descarga de Archivos:** El servidor indica al peer la dirección IP y el puerto de otro peer que posee el archivo deseado, permitiendo así la descarga directa del archivo.

### Patrones de Diseño Utilizados
- **Factory:** Se utiliza en la creación del servidor mediante una función que crea una instancia única de este.
- **Singleton:** La variable `users` representa la información de los usuarios conectados, y solo tiene un valor durante la conexión, lo que la convierte en una instancia única.

## Entorno de Desarrollo y Configuraciones

### IDE
Visual Studio Code

### Lenguaje de Programación
Python v3.11.6

### Librerías Utilizadas
- **grpcio** v1.62.0
- **grpcio-tools** v1.62.0
- **Flask** v3.0.0
- **requests** v2.31.0

## Instalación de Librerías
Para instalar las librerías necesarias, ejecuta el siguiente comando en una terminal de Visual Studio Code:

pip install grpcio grpcio-tools Flask requests

Ejecución
------------
El archivo Pservidor.proto requiere correr el siguiente comando para crear los archivos necesarios para funcionar.
Se sugiere utilizar el nombre de Pservidor.proto pues las importaciones tienen el nombre de este archivo mas el agregado automatico
de correr el comando.

Nota: Asegurarse de estar en la carpeta peer
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. Pservidor.proto

Al tener los archivos pb2 de grpc ya es posible ejecutar individualmente los servidores localmente.
Primero inicializamos el servidor con

- python Server.py

Luego inicializamos el servidor del peer y el cliente
Nota: asegurarse de estar en la carpeta servidor

- python Pservidor.py
- python Pcliente.py

Registramos el cliente en el Server y ya estaria la configuración inicial.
Se pueden crear mas peers siguiendo el paso de inicializar peer server y cliente.

Configuraciones adicionales
---------------------------
Los puertos manejan un rango donde se van a crear y enlazar con el cliente del peer, si se desea expandir este rango se puede modificar las variables rango-Min y rango-Max

Finalmente deberia tener una vista de Pservidor Consola izquierda, Pcliente consola central y Servidor consola derecha.
![image](https://github.com/juanxv/jurami-ST0263/assets/44956232/315ce2bb-9148-4f57-9693-c288951b4ad1)

# Referencias

https://www.toolify.ai/es/ai-news-es/tutorial-de-python-grpc-crea-un-cliente-y-servidor-grpc-en-python-con-diferentes-tipos-de-llamadas-1098372
https://pythonbasics.org/flask-rest-api/
