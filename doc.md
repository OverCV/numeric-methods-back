# Instalación de la aplicación

## Requisitos
Como el proyecto está ya generado, solo se necesita instalar las dependencias de la aplicación, para esto requerimos un entorno virtual de python, para esto se puede usar el siguiente comando:

```powershell
py -m venv .env
```
Tener muy en cuenta que debe de activarse el entorno virtual antes de instalar las dependencias, para esto se usa el siguiente comando:

```bash
source .env\Scripts\activate
```

Una vez activado el entorno virtual, se procede a instalar las dependencias, para esto se usa el siguiente comando:

```powershell
py -m pip install -r  .\requirements\base.txt
```

## Inicialización
Para inicializar el proyecto, se debe de ejecutar el siguiente comando:

```bash
py api/exec.py
```

## FastAPI
### Base de datos
Todo está configurado para que se use una base de datos SQLite, por lo que no se necesita configurar nada, todo lo refetente a la base de datos se encuentra en el archivo `api/database.py` y esta será usada posteriormente para inicializar la aplicación (en el `main.py` y en los api/services, la parte lógica de la aplicación).

```bash


### Documentación de endpoints
Para acceder a la documentación de la API, se debe de acceder a la siguiente ruta:

```bash
http://localhost:8300/docs
```