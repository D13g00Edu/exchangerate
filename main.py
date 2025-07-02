from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware # Importa CORSMiddleware
import requests
import os

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="API de Conversión de Monedas",
    description="Una API para obtener tasas de cambio y realizar conversiones.",
    version="1.0.0",
)

# --- Configuración de CORS ---
# Permite que el frontend (abierto desde el sistema de archivos o cualquier origen)
# pueda hacer peticiones a este backend.
# En un entorno de producción, es recomendable restringir origins a dominios específicos.
#origins = [
#    "http://localhost",
#    "http://localhost:8000",
#    "http://127.0.0.1",
#    "http://127.0.0.1:8000",
#    "null" # Permite solicitudes cuando el HTML se abre directamente desde el sistema de archivos
#]

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins, # Lista de orígenes permitidos
#    allow_credentials=True, # Permite cookies, encabezados de autorización, etc.
#    allow_methods=["*"], # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
#    allow_headers=["*"], # Permite todos los encabezados
#)

# --- Configuración de la API de Tasas de Cambio ---
# Lee la clave API de una variable de entorno llamada "EXCHANGE_RATE_API_KEY".
# Si la variable de entorno no está definida (por ejemplo, en desarrollo local sin configurarla),
# se usará "TU_CLAVE_API_AQUI" como valor por defecto.
# Para GitHub Actions/Secrets, configura una variable de entorno/secreto con este nombre.
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY", "TU_CLAVE_API_AQUI")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

@app.post("/convert", summary="Realiza la conversión de moneda")
async def convert_currency(
    amount: float = Form(...),  # Cantidad a convertir, recibida de un formulario
    from_currency: str = Form(...), # Moneda de origen, recibida de un formulario
    to_currency: str = Form(...)    # Moneda de destino, recibida de un formulario
):
    """
    Convierte una cantidad de una moneda a otra utilizando la API de tasas de cambio.

    - **amount**: La cantidad numérica a convertir.
    - **from_currency**: El código de la moneda de origen (ej. USD, EUR).
    - **to_currency**: El código de la moneda de destino (ej. USD, EUR).
    """
    try:
        # Construye la URL para obtener las tasas de cambio de la moneda de origen
        conversion_url = f"{BASE_URL}/latest/{from_currency.upper()}"
        
        # Realiza la petición HTTP a la API externa
        response = requests.get(conversion_url)
        response.raise_for_status() # Lanza una excepción si la respuesta HTTP es un error (4xx o 5xx)
        
        # Parsea la respuesta JSON
        data = response.json()

        # Verifica si la API devolvió un error
        if data["result"] == "error":
            error_type = data.get("error-type", "Error desconocido de la API")
            return JSONResponse(status_code=400, content={"error": f"Error de la API: {error_type}. Verifica tu clave API o la moneda base."})

        # Obtiene las tasas de conversión
        exchange_rates = data["conversion_rates"]
        
        # Verifica si la moneda de destino existe en las tasas obtenidas
        if to_currency.upper() not in exchange_rates:
            return JSONResponse(status_code=400, content={"error": f"Moneda de destino '{to_currency.upper()}' no encontrada en las tasas disponibles."})

        # Realiza el cálculo de la conversión
        rate = exchange_rates[to_currency.upper()]
        converted_amount = amount * rate

        # Retorna el resultado en formato JSON
        return {
            "amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "rate": rate,
            "converted_amount": round(converted_amount, 2) # Redondea a 2 decimales
        }
    except requests.exceptions.RequestException as e:
        # Captura errores de conexión o HTTP
        return JSONResponse(status_code=500, content={"error": f"Error al conectar con la API de tasas de cambio: {e}. Verifica tu conexión a internet o la URL de la API."})
    except KeyError:
        # Captura errores si la estructura JSON de la respuesta es inesperada
        return JSONResponse(status_code=500, content={"error": "Respuesta inesperada de la API. Podría ser un problema con la clave API o el formato de la respuesta."})
    except Exception as e:
        # Captura cualquier otro error inesperado
        return JSONResponse(status_code=500, content={"error": f"Ocurrió un error interno: {e}"})

# La documentación de Swagger UI está disponible en /docs
# La documentación de ReDoc está disponible en /redoc
