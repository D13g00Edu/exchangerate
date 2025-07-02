# exchangerate
💰 Conversor de Monedas con FastAPI
Este proyecto implementa un conversor de monedas simple pero robusto, utilizando FastAPI para el backend y una interfaz de usuario independiente construida con HTML, CSS y JavaScript. El backend consume una API externa de tasas de cambio para proporcionar conversiones en tiempo real.

✨ Características
Backend con FastAPI: Una API RESTful moderna, rápida y con documentación automática.

Documentación Interactiva (Swagger UI): Accede a la documentación de la API en tiempo real y prueba los endpoints directamente desde tu navegador.

Consumo de API Externa: Obtiene las tasas de cambio más recientes de ExchangeRate-API.com.

Manejo de CORS: Configurado para permitir peticiones desde diferentes orígenes, facilitando la integración con un frontend independiente.

Frontend Independiente: Una interfaz de usuario simple y responsiva desarrollada con HTML, CSS y JavaScript, que se comunica con el backend.

Manejo de Errores: Incluye manejo de errores para problemas de conexión, errores de la API y datos inválidos.

Seguridad de Clave API: Lee la clave API de una variable de entorno, una práctica recomendada para la seguridad en producción.

🚀 Tecnologías Utilizadas
Backend
Python 3.x

FastAPI: Framework web de alto rendimiento para construir APIs.

Uvicorn: Servidor ASGI para ejecutar aplicaciones FastAPI.

Requests: Librería HTTP para realizar peticiones a la API externa.

python-dotenv (Opcional): Para cargar variables de entorno desde un archivo .env en desarrollo local.

Frontend
HTML5: Estructura de la interfaz de usuario.

CSS3: Estilos para una apariencia limpia y responsiva.

JavaScript (ES6+): Lógica interactiva para manejar la entrada del usuario, realizar peticiones al backend y mostrar los resultados.
