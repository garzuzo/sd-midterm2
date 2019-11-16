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


**Integrantes:** Johan Camilo Diaz A00329772  
**Integrantes:** Johnatan Garzón A00333960


### Evidencia de la API de conformidad con el estándar OpenAPI


##### GET
![alt text](images/get_openapi?raw=true "")

>El método post en OpenAPI posee el campo de ingreso de parametros (los parametros id y name) además del significado de las posibles status code que se pueden obtener al realizar una petición, entre estos códigos se encuentran el 201 que representa una creación exitosa de un usuario en la base de datos, el código 400 que representa una bad request es decir que los parámetros enviados en la petición no son pertinentes para la operación a realizar, y el código 402 que se presenta cuando el id del usuario que se desea agregar a la base de datos ya existe.

```yaml
    get:
      summary: Extraer la información
      description: Se extrae información todos los usuarios de la base de datos.
      operationId: app.read_user
      responses:
        200:
          description: Datos obtenidos con éxito
          content:
            text/plain:
              schema:
                type: string
                example: '[{"_id": {"$oid": "5dcb7fc020f273c7abeb0a7b"}, "id": "1", "name": "Johnatan"}]'


```
En el código YAML para la definición del método GET se cuenta con la descripción correspondiente donde se deja en claro qué función cumple este método, además se define el operationId que es un componente muy importante en la descripción del método ya que en este campo se especifica la dirección de la operación que se va a invocar cada vez que se realice una petición bajo la modalidad GET al path escrito (/users). En este caso la operación invocada se encuentra en la *app.py* y se llama *read_user*.




##### POST
![alt text](images/post_openapi?raw=true "")

>El método get por su parte posee solamente el significado de su status code 200 que se presenta cuando los datos se han obtenido de manera correcta, en adición a eso, también posee un ejemplo de cómo se vería el mensaje de respuesta de la petición.


```yaml
    post:
      summary: Crear un usuario
      description: Crea un usuario en base a los datos de id y nombre ingresados por parametro.
      operationId: app.create_user
      requestBody:
        description: Usuario a crear en la base de datos
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              $ref: '#/components/schemas/NewUser'
      responses:
        201:
          description: Usuario creado con exito
        400:
          description: Bad request
        402:
          description: El usuario ya existe


components:
  schemas:
    NewUser:
      type: object
      properties:
        id: 
          type: string
        name: 
          type: string
```
Para las peticiones de tipo POST se define que cada vez que se reciba una solicitud se invoque la operación create_user que pertenece al módulo *app.py* que se encuentra en la carpeta *backend*. En este método se especifica un requestBody donde se plantea que el parámetro que será transmitido es de tipo **x-www-form-urlencoded** y que seguirá un esquema llamado *NewUser* definido en el apartado de *components*, el cual especifíca los parametros, el tipo y el nombre de los mismos, que se encuentran en el requestBody.



##### DELETE
![alt text](images/delete_openapi?raw=true "")

>El método delete presenta dos status code, el código 204 simboliza que un usuario ha sido eliminado de la base de datos de forma correcta y el código 404 simboliza que el id del usuario que se pretendía borrar no existe. En adición a esto se puede apreciar que el método delete posee una ruta especial definida como /user/{id del usuario que se desea borrar} y que el id es reconocido como parámetro para la posterior eliminación del usuario que posea ese identificador.

```yaml
  /users/{id}:
    delete:
      summary: Eliminar usuario
      description: Se elimina el usuario de la base de datos.
      operationId: app.delete_user
      parameters:
        - name: id
          in: path
          description: Identificador del usuario a eliminar
          required: true
          schema:
            type: string
      responses:
        204:
          description: Usuario removido con éxito
        404:
          description: El usuario no existe
```
En este método se hace uso de un path diferente que cuenta con el id del usuario a eliminar, es decir, el path tiene la siguiente estructura “/users/id” donde id corresponde al usuario del que se desea prescindir. Dentro del código YAML se especifica de qué tipo debe ser este dato, para nuestro caso se decidió que el dato debe ser tipo String.

### Evidencia de pruebas unitarias de cada microservicio para el proceso de integración continua

Prueba para obtener todos los usuarios

```python
def test_valid_read_clients(client):
        response = client.get('/users')
        assert response.status_code == 200
```

Prueba de un endpoint inválido, en este caso obtener un usuario en específico no está implementado por lo que debería retornar un status code igual a 405:
```python
def test_invalid_endpoint_read_clients(client):
        response = client.get('/users/32')
        assert response.status_code == 405
```

Prueba válida de creación de un nuevo usuario. Se crea un nuevo usuario, el cúal al crear retorna un status code igual a 201, y luego es eliminado para no interferir con futuras pruebas y retorna un status code igual a 204:
```python
def test_valid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 
        response = client.post('/users', data=dict(id='abc12345', name='Marshmillow'), headers=header)
        
        assert response.status_code == 201
        response_remove=client.delete('/users/abc12345')
        assert response_remove.status_code == 204
```


Prueba para verificar que la eliminación de usuarios que no existen retornen un 404:
```python
def test_delete_clients_unavailable(client):
        response_remove=client.delete('/users/juanmaid')
        assert response_remove.status_code == 404
```


Prueba para verificar que no se cree un usuario que existía previamente, es decir, que retorne un status code igual a 402:
```python
def test_invalid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='1', name='Marshmillo'), headers=header)
        
        assert response.status_code == 402
    
```


Prueba para verificar que retorne un status code igual a 400 cuando se envíe un body incorrecto en la creación de un nuevo usuario:
```python
def test_invalid_body_req_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='bcc21912', names='Marshmillo'), headers=header)
        
        assert response.status_code == 400
```






### Evidencia del código pasando dichas pruebas
Para correr las pruebas de manera **local** se usa el comando:
```sh
$ pytest tests/test_app.py
```
Podemos observar el resultado exitoso de las seis pruebas implementadas:

![alt text](images/pytest_passed?raw=true "")

Ahora, observamos el resultado de la ejecución de las pruebas en **travis CI**:


![alt text](images/travis_passed?raw=true "")

Observamos como se carga primero la variable de entorno **MONGO_FLASK**, y luego se encarga de instalar los requerimientos indicados en **requirements.txt**, y por último ejecuta las pruebas, dando como resultado seis pruebas exitosas:

![alt text](images/pytest_passed_travis?raw=true "")




### Tareas para desplegar los microservicios en una máquina local

Las tareas que se deben llevar a cabo son:

1. Se deben instalar los requerimientos necesarios que se encuentran en *requirements.txt*
2. Se exporta la variable de entorno *MONGO_FLASK* que contiene las credenciales para conectarse con la base de datos remota
3. Ejecutar la aplicación *app.py* que se encuentra en la carpeta *backend*
```sh
$ pip install -r requirements.txt
$ export MONGO_FLASK=d_user:distribuidos20192
$ python3 backend/app.py
```


### Evidencias del despliegue

Ahora, se puede observar las respuestas correctas por parte de cada uno de los endpoints implementados.

Obtener todos los usuarios:

![alt text](images/get_postman?raw=true "")

Agregamos un nuevo usuario:

![alt text](images/post_postman?raw=true "")


Obtenemos de nuevo la lista con todos los usuarios para ver el nuevo usuario agregado:

![alt text](images/get_postman_after_add.png?raw=true "")

Eliminamos un usuario

![alt text](images/delete_postman?raw=true "")

### Problemas encontrados y acciones efectuadas para su solución


- Se presentaron inconvenientes en el entendimiento de la integración de openapi con nuestra aplicación en Flask. Con el tiempo fuimos comprendiendo que lo indicado en el archivo .yaml de openapi y sus endpoints estaban ligados a cada método correspondiente, que depende del tipo de petición y la ruta.
  
- Tuvimos problemas al importar la app.py que está en la carpeta backend en el archivo de pruebas (test_app.py), ya que al principio estabamos usando tres puntos (...) para llegar a la carpeta padre que contenía dicha carpeta. Esto resultó en errores, que primeramente solucionamos importando la libreria imp, que nos permitía importar un módulo dada una ruta, sin embargo, esta librería estaba deprecada. Por lo tanto, para solucionar esto buscamos otra librería equivalente llamada importlib, la cual, mediante el modulo machinery permite realizar la tarea requerida que se mencionó anteriormente.
  
- Otro problema tenía que ver con la variable de entorno utilizada para guardar las credenciales de ingreso a la base de datos remota, esto debido a que no hallabamos una forma clara de cargar esta variable en travis CI, primero intentamos cargar la variable directamente en la plataforma de travis CI, pero al momento de hacer el pull request obteniamos un error, ya que la variable solo se encontraba en nuestro repositorio, por lo que pensamos en pasar la variable encriptada en el archivo .travis.yml, lo que permitiría ser usada en cualquier otro repositorio. Sin embargo, siguió fallando, y llegamos a la conclusión junto al profesor de que la configuración del travis en el repositorio original (al que se le debía hacer el pull request), no contaba con los permisos necesarios para hacer uso de variables de entorno.

![alt text](images/failed_PR_travis?raw=true "")

>En una vista más detallada, se puede observar el error de pymongo al no poder obtener las credenciales de autenticación para la conexión con mlab:


![alt text](images/detailed_failed_PR_travis?raw=true "")


- Por último, un problema por el que no se realizaban las peticiones HTTP en el ui de openapi, era porque estábamos accediendo desde otro origen al servidor, por lo tanto teníamos que permitir el acceso desde otros orígenes, es decir: activamos el Cross-Origin Resource Sharing (CORS), esto mediante un decorator de la librería flask_cors (@cross_origin(origin='*'))