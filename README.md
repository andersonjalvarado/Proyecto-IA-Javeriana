# Proyecto de Aprendizaje de Máquina

Este proyecto utiliza la librería Dash para visualizar datos procesados con pandas, numpy y scikit-learn. La visualización se ejecuta en un servidor local y se puede acceder a través de un navegador web.

## Estructura del Proyecto

```
Proyecto
│
├── code/
│   ├── Visor/
│   │   └── visor.py
│   │   └── ipc.py
│   │── NoteBook/
│       └── Proyecto.py
├── data
│
├── requeriments.txt
├── README.md
└── ...
```

## Requisitos

Asegúrate de tener Python 3.x instalado en tu sistema. Puedes descargarlo desde [python.org](https://www.python.org/).

### Instalación de Dependencias

Las dependencias del proyecto están listadas en el archivo `requeriments.txt`. Para instalar todas las dependencias, sigue estos pasos:

1. Abre una terminal (Command Prompt, PowerShell, Terminal, etc.).
2. Navega hasta el directorio raíz de tu proyecto donde se encuentra `requeriments.txt`.
3. Ejecuta el siguiente comando:

   ```bash
   pip install -r requeriments.txt
   ```

## Ejecución del Proyecto

Para ejecutar la visualización con Dash, sigue estos pasos:

1. Abre una terminal.
2. Navega hasta el directorio `code/Visor` donde se encuentra el archivo `visor.py`.

   ```bash
   cd code/Visor
   ```

3. Ejecuta el script `visor.py` con Python:

   ```bash
   python visor.py
   ```

4. Una vez que el servidor esté en funcionamiento, deberías ver un mensaje similar a este en la terminal:

   ```
   Dash is running on http://127.0.0.1:8050/
   ```

5. Abre tu navegador web preferido y navega a la dirección proporcionada, normalmente `http://127.0.0.1:8050/`.

## Archivos Clave

- `requeriments.txt`: Lista de dependencias necesarias para ejecutar el proyecto.
- `Informe_Proyecto.pdf`: Informe sobre el proyecto.
- `code/Visor/visor.py`: Script principal que contiene la configuración y ejecución del servidor Dash.
- `code/NoteBook/Proyecto.ipnb`: Notebook de la realización y prueba del Proyecto.

## Notas Adicionales

- Asegúrate de tener todas las dependencias correctamente instaladas para evitar errores durante la ejecución.
- Puedes personalizar el script `visor.py` según tus necesidades específicas de visualización y procesamiento de datos.


## Contacto

Para cualquier pregunta o sugerencia, por favor abre un issue en el repositorio o contacta al autor del proyecto.