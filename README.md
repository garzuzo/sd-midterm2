# Exam 2 

**Universidad ICESI**  
**Course:** Distributed systems  
**Teacher:** Juan M Álvarez Q.  
**Topic:** Microservices Architecture design  
**email:** juan.alvarez8 at correo.icesi.edu.co

### Learning goals
* Design a microservices architecture application

### Suggested technologies for the midterm development
* [Open API](https://openapi.tools/)
* github repository
* Flask and [connexion](https://connexion.readthedocs.io/en/latest/)
* Mongo db and [mlab](https://mlab.com/)
* [travis-ci](https://travis-ci.org/)

### Description

For this exam you should redesing the application developed in midterm 1 into a REST-based microservices arquitecture. your aplication must comply the following:

* Must have a github repository which is a fork of the **[sd-mdterm2](https://github.com/ICESI-Training/sd-midterm2)** repository
* It is suggested to use mlab for data storage: mlab is a database as a service provider for mongo databases.
* The system must accept Http requests from cURL (you can use other REST clients like postman, insomnia or postwoman.
* The application must have an endpoint to insert data in the database.
* The application must have an endpoint to retrieve all the registers from a database collection or table.
* The design must have continous integration unit tests for all microservices.


### Actividades (EN español para evitar ambigüedades)
1. Documento README.md en formato markdown:  
  * Formato markdown (5%).
  * Nombre y código del estudiante (5%).
  * Ortografía y redacción (5%).
2. Documentación de la API de conformidad con el estándar [OpenAPI](https://github.com/OAI/OpenAPI-Specification). (15%)
3. Pruebas unitarias de cada microservicio para el proceso de integración contínua (10%). Evidencia del código pasando dichas pruebas(5%).
4. Archivos fuentes en el repositorio de los microservicios implementados (15%).
5. Documentación de las tareas para desplegar los microservicios en una máquina local (10%). Evidencias del despliegue (peticiones cURL o similares)(10%).
6. El informe debe publicarse en un repositorio de github el cual debe ser un fork de https://github.com/ICESI-Training/sd-midterm2 y para la entrega deberá hacer un Pull Request (PR) al upstream (10%). Tenga en cuenta que el repositorio debe contener todos los archivos necesarios para el despliegue.
7. Documente algunos de los problemas encontrados y las acciones efectuadas para su solución (10%).


**Integrantes:** Camilo Diaz A00329772  
**Integrantes:** Johnatan Garzón A00333960


#### Evidencia de la API de conformidad con el estándar OpenAPI





#### Evidencia de pruebas unitarias de cada microservicio para el proceso de integración continua
Prueba para obtener todos los usuarios:
```python
def test_valid_read_clients(client):
        response = client.get('/users')
        assert response.status_code == 200
```

Prueba de endpoint inválido:
```python
def test_invalid_endpoint_read_clients(client):
        response = client.get('/users/32')
        assert response.status_code == 405
```

Prueba de crear usuarios:
```python
def test_valid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 
        response = client.post('/users', data=dict(id='abc12345', name='Marshmillow'), headers=header)
        
        assert response.status_code == 201
        response_remove=client.delete('/users/abc12345')
        assert response_remove.status_code == 204
```


Prueba para verificar la eliminación de clientes que no existen
```python
def test_delete_clients_unavailable(client):
        response_remove=client.delete('/users/juanmaid')
        assert response_remove.status_code == 404
```


Prueba para verificar la no creación de usuarios que existen previamente:
```python
def test_invalid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='1', name='Marshmillo'), headers=header)
        
        assert response.status_code == 402
    
```


Prueba para obtener todos los usuarios:
```python
def test_invalid_body_req_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='bcc21912', names='Marshmillo'), headers=header)
        
        assert response.status_code == 400
```






#### Evidencia del código pasando dichas pruebas
Para correr las pruebas de manera local se usa el comando:
```sh
$ pytest tests/test_app.py
```
Podemos observar el resultado exitoso de las seis pruebas implementadas:

![alt text](images/pytest_passed.PNG?raw=true "")

Ahora, observamos el resultado de la ejecución de las pruebas en travis CI:

![alt text](images/pytest_passed_travis.PNG?raw=true "")



#### Tareas para desplegar los microservicios en una máquina local
```sh
$ pip install -r requirements.txt
$ python3 backend/app.py
```
#### Evidencias del despliegue

Obtener todos los usuarios

![alt text](images/pytest_passed.PNG?raw=true "")

Agregamos un nuevo usuario

![alt text](images/post_postman.PNG?raw=true "")


Obtenemos de nuevo la lista con todos los usuarios para ver el nuevo usuario agregado

![alt text](images/get_postman_after_addPNG?raw=true "")

Eliminamos un usuario

![alt text](images/delete_postman.PNG?raw=true "")

#### Problemas encontrados y acciones efectuadas para su solución


- Se presentaron inconvenientes en el entendimiento de la integración de openapi con nuestra aplicación en Flask. Con el tiempo fuimos comprendiendo que lo indicado en el archivo .yaml de openapi y sus endpoints estaban ligados a cada método correspondiente, que depende del tipo de petición y la ruta.
  
- Tuvimos Problemas al importar la app.py que está en la carpeta backend en el archivo de pruebas (test_app.py), ya que al principio estabamos usando tres puntos (...) para llegar a la carpeta padre que contenía dicha carpeta. Esto resultó en errores, que primeramente solucionamos importando la libreria imp, que nos permitia importar un modulo dada una ruta, sin embargo, esta librería estaba deprecada. Por lo tanto, para solucionar esto buscamos otra librería equivalente llamada importlib, la cual, mediante el modulo machinery permite realizar la tarea requerida que se mencionó anteriormente.
Otro problema tenía que ver con la variable de entorno utilizada para guardar las credenciales de ingreso a la base de datos remota, esto debido a que no hallabamos una forma clara de cargar esta variable en travis CI, primero intentamos cargar la variable directamente en la plataforma de travis CI, pero al momento de hacer el pull request obteniamos un error, ya que la variable solo se encontraba en nuestro repositorio, por lo que pensamos en pasar la variable encriptada en el archivo .travis.yml, lo que permitiría ser usada en cualquier otro repositorio. Sin embargo, siguió fallando, y llegamos a la conclusión junto al profesor de que la configuración del travis en el repositorio original (al que se le debía hacer el pull request), no contaba con los permisos necesarios para hacer uso de variables de entorno.

![alt text](images/failed_PR_travis.PNG?raw=true "")

En una vista más detallada


![alt text](images/detailed_failed_PR_travis.PNG?raw=true "")


- Por último, un problema por el que no se realizaban las peticiones HTTP en el ui de openapi, era porque estábamos accediendo desde otro origen al servidor, por lo tanto teníamos que permitir el acceso desde otros orígenes, es decir: activamos el Cross-Origin Resource Sharing (CORS), esto mediante un decorator de la librería flask_cors (@cross_origin(origin='*'))