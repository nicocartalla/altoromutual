# Consiga Obligatoria #4
## ****Evaluación Automatizada de Vulnerabilidades en AltoroMutual****
> Autores: Nicolás Cartalla, Carol Glass, Antonia Mescia
> 

Esta serie de pruebas fue diseñada con el propósito de detectar y resolver vulnerabilidades de seguridad en AltoroMutual. El objetivo principal es implementar pruebas sistemáticas que se realicen de manera recurrente, para así garantizar que no se reintroduzcan problemas que ya han sido solucionados previamente. La ejecución de estas pruebas en cada liberación es esencial para mantener la integridad y seguridad de la aplicación.

### Instalación y prerrequsitos

Para realizar las pruebas es esencial contar con el entorno adecuado. Los prerrequisitos se detallan a continuación:

- **Proyecto AltoroJ**
- **Python3**
- **pip3**: Es la herramienta que se utilizará para instalar las librerías necesarias.
- **Librería** `requests`

El proyecto puede ser corrido utilizando el entorno provisto por la cátedra. En caso de optar por esta alternativa, se deberán correr lo siguientes comandos en la terminal para instalar Python3, pip3 y `requests`:

```bash
sudo apt-get update
sudo apt-get -y install python3
sudo apt-get -y install python3-pip
pip3 install requests
```

Para quienes prefieran trabajar con Docker o no cuenten con la máquina virtual de la cátedra, se ha incluido en este repositorio una imagen de Docker que replica el ambiente provisto por la cátedra. Para usarla:

1. Asegurar tener Docker instalado en el equipo.
2. Clonar el repositorio y navegar al directorio donde se encuentra el Dockerfile.
3. Construir la imagen con el siguiente comando:

```bash
docker build -t altoro .
```

1. Una vez construida, ejecutar un contenedor basado en la imagen:

```bash
docker run -dp 8081:8080 altoro
```

### Descripción de las pruebas

#### Inyección SQL en Login

El script `SqlInjection.py` está diseñado para comprobar si la funcionalidad de login de la aplicación es vulnerable a inyecciones SQL o no. Realiza varios intentos de inicio de sesión con distintos payloads que suelen ser indicativos de vulnerabilidades de inyección SQL. Si detecta un inicio de sesión válido cuando no debería serlo, retorna un código de salida 1, indicando que la aplicación es vulnerable. Si no detecta vulnerabilidades, retorna un código de salida 0. 

#### Cross-Site Scripting en barra de búsqueda

El script `Xss.py` ha sido diseñado para evaluar si la aplicación es susceptible a ataques Cross-Site Scripting (XSS), particularmente en la barra de búsqueda. Realiza varias peticiones con diferentes valores de entrada; si el HTML retornado lo contiene, se interpreta que la vulnerabilidad está presente.

#### Consolidación de las pruebas

El script `main**.**py` sirve como punto de entrada central para la ejecución de las pruebas. Una vez ejecutadas todas las pruebas, este script genera un reporte consolidado. Al estructurar el script de esta manera, se facilita la adición de nuevas pruebas en el futuro, haciendo que el proceso de evaluación de seguridad sea más eficiente y organizado. Los resultados podrán ser consultados por consola, o en el log `dast-report.txt` que se guarda en la carpeta `/tmp` .

### **Ejecución de las pruebas**

Existen dos formas principales de ejecutar las pruebas de seguridad:

#### Ejecución Manual

A continuación, se describen los pasos para correr las pruebas de forma manual:

1. Tener el proyecto levantado, sea utilizando la máquina virtual o con Docker.
2. Estar parado en el directorio **`/**dast` del proyecto.
3. Ejecutar el script `main.py` utilizando el siguiente comando:

```python
python3 main.py
```

1. Observar los resultados en la consola. Un posible resultado se ve de la siguiente forma:

```python
***** Login - SQL Injection Test *****
[*] uid={'user': 'admin', 'passw': 'test'}, Received a 302, but the AltoroAccounts cookie was not found.
[*] uid={'user': "'", 'passw': "'"}, Received a 302, but the AltoroAccounts cookie was not found.
[*] uid={'user': '+--', 'passw': 'test'}, Received a 302, but the AltoroAccounts cookie was not found.
[!] uid={'user': "admin' or 1=1 --", 'passw': 'test'}, SQL injection detected in the login.
         Set-Cookie received: JSESSIONID=528AC2966378DD4EF5E9FC8EB26E9484; Path=/; HttpOnly, AltoroAccounts=ODAwMDAwfkNvcnBvcmF0ZX41LjIzOTQ3ODM2MUU3fDgwMDAwMX5DaGVja2luZ345MzgyMC40NHw4MDAwMDJ+U2F2aW5nc34xMDA$

***** Search - Cross Site Scripting Test  *****
[!] An XSS was detected in the URL: http://localhost:8081/search.jsp?query=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E
[!] An XSS was detected in the URL: http://localhost:8081/search.jsp?query=%3Cscript%3Ealert%28%27xss%27%29%3C%2Fscript%3E
[!] An XSS was detected in the URL: http://localhost:8081/search.jsp?query=%3Cimg%20src%3Dx%20onerror%3Dalert%28%27xss%27%29%3E
[!] An XSS was detected in the URL: http://localhost:8081/search.jsp?query=javascript%3Aalert%28%27xss%27%29

Total tests passed: 3/8
```

#### Ejecución Automatizada mediante GitHub Actions

Se ha implementado el pipeline `AltoroCI` , diseñado para automatizar y garantizar la seguridad del código cada vez que se realiza una acción con pull request hacia la rama `main`. 

El primer paso consiste en hacer una copia del código del repositorio utilizando `actions/checkout@v2`. Posteriormente, el pipeline procede con la preparación del ambiente; para ello, instala Docker en la máquina virtual. Este proceso implica actualizar la lista de paquetes, instalar dependencias necesarias, añadir el repositorio oficial de Docker, y finalmente instalar Docker en si.

Una vez que Docker está instalado y listo para ser utilizado, el siguiente paso es autenticarse en Docker Hub. Para ello utiliza un token secreto previamente almacenado en las variables secretas del repositorio. Con el acceso a Docker Hub establecido, el pipeline construye una imagen Docker para el proyecto `altoromutual`. Esta imagen es etiquetada como `latest`. Además, se crea una etiqueta adicional para esta imagen usando el ID del commit actual, lo que facilita la identificación en futuras revisiones.

A continuación, se construye una imagen Docker específicamente diseñada para llevar a cabo las pruebas de seguridad, basándose en el archivo ****`Dockerfile-dast`. Una vez construida esta imagen, se ejecuta y pone en marcha las pruebas de seguridad en un contenedor aislado. Finalmente, el pipeline publica las etiquetas de imágenes, tanto `latest` como la etiquetada con el ID del commit, en Docker Hub. 

Esta metodología asegura un proceso continuo de integración y despliegue que valora y prioriza la seguridad.