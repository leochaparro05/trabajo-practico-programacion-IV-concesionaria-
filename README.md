# Trabajo Práctico: API CRUD de Ventas de Autos

## Información del Trabajo

**Materia:** Programación IV  
**Universidad:** Universidad Tecnológica Nacional  
**Trabajo Práctico:** API REST para Gestión de Ventas de Autos  
**Fecha de Entrega:** 20 Noviembre 2025

---

## Datos del Estudiante

**Estudiante:** Leo Chaparro
**Legajo:** 17451 
**Carrera:** Tecnicatura univeritaria en programacion 

---

Este trabajo práctico implementa una API REST completa para la gestión de ventas de autos utilizando **FastAPI**, **SQLModel** y **PostgreSQL**. El sistema permite administrar un inventario de autos y registrar las ventas realizadas, implementando todas las operaciones CRUD y aplicando patrones de diseño profesionales.

El proyecto cumple con todos los requisitos especificados en el documento del trabajo práctico, incluyendo:
- Implementación completa de operaciones CRUD para ambas entidades
- Patrón Repository para acceso a datos
- Validaciones robustas de datos
- Relaciones uno-a-muchos entre entidades
- Endpoints adicionales para búsquedas y consultas relacionadas
- Documentación automática de la API

---

## Descripción del Sistema

El sistema gestiona dos entidades principales con una relación uno-a-muchos:

### Entidad: Auto
- **marca**: Marca del vehículo (ej: Toyota, Ford, Chevrolet)
- **modelo**: Modelo específico (ej: Corolla, Focus, Cruze)
- **año**: Año de fabricación (entre 1900 y año actual)
- **numero_chasis**: Número único de identificación del chasis (alfanumérico, único en el sistema)

### Entidad: Venta
- **nombre_comprador**: Nombre completo del comprador
- **precio**: Precio de venta del vehículo
- **auto_id**: Referencia al auto vendido (clave foránea)
- **fecha_venta**: Fecha y hora de la venta

---

## Tecnologías Utilizadas

- **FastAPI 0.121.2**: Framework web moderno y rápido para construir APIs REST
- **SQLModel 0.0.27**: ORM que combina SQLAlchemy y Pydantic para modelado de datos
- **PostgreSQL 17.6**: Base de datos relacional
- **Pydantic 2.12.4**: Validación de datos y serialización
- **Uvicorn 0.38.0**: Servidor ASGI de alto rendimiento
- **Python 3.14**: Lenguaje de programación
- **python-dotenv 1.2.1**: Gestión de variables de entorno

---

## Estructura del Proyecto

```
tpconcesionario/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Configuración de base de datos PostgreSQL
├── models.py            # Modelos SQLModel (Auto y Venta)
├── repository.py        # Patrón Repository para acceso a datos
├── autos.py            # Router de endpoints para autos
├── ventas.py           # Router de endpoints para ventas
├── requirements.txt     # Dependencias Python
├── .env                # Variables de entorno (no incluido en repositorio)
├── test_connection.py  # Script de prueba de conexión
└── README.md           # Este archivo
```

---

## Instalación y Configuración

### Prerrequisitos

- Python 3.9 o superior (probado con Python 3.14)
- PostgreSQL 12 o superior (probado con PostgreSQL 17.6)
- pip (gestor de paquetes de Python)
- pgAdmin (opcional, para gestión de base de datos)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual** (recomendado):
```bash
python -m venv venv
```

3. **Activar el entorno virtual**:
   - En Windows:
   ```bash
   venv\Scripts\activate
   ```
   - En Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

5. **Configurar PostgreSQL**:
   - Crear una base de datos llamada `autos_db` en pgAdmin o mediante línea de comandos:
   ```sql
   CREATE DATABASE autos_db;
   ```

6. **Configurar variables de entorno**:
   
   Crear un archivo `.env` en la raíz del proyecto:
   ```bash
   DATABASE_URL=postgresql://usuario:password@localhost:5432/autos_db
   ```
   
   **Ejemplo:**
   ```bash
   DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/autos_db
   ```

7. **Probar la conexión** (opcional):
```bash
python test_connection.py
```

---

## Ejecución del Sistema

### Modo Desarrollo

```bash
python -m uvicorn main:app --reload
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Una vez iniciada la aplicación, puedes acceder a:
- **API Raíz**: http://localhost:8000
- **Documentación interactiva (Swagger UI)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Documentación de Endpoints

### Endpoints de Autos (`/autos`)

| Método | Endpoint | Descripción | Estado |
|--------|----------|-------------|--------|
| POST | `/autos` | Crear nuevo auto | ✅ Implementado |
| GET | `/autos` | Listar autos (con paginación y filtros) | ✅ Implementado |
| GET | `/autos/{auto_id}` | Obtener auto por ID | ✅ Implementado |
| PUT | `/autos/{auto_id}` | Actualizar auto | ✅ Implementado |
| DELETE | `/autos/{auto_id}` | Eliminar auto | ✅ Implementado |
| GET | `/autos/chasis/{numero_chasis}` | Buscar por número de chasis | ✅ Implementado |
| GET | `/autos/{auto_id}/with-ventas` | Auto con sus ventas relacionadas | ✅ Implementado |

**Parámetros de búsqueda adicionales:**
- `marca`: Filtro por marca (búsqueda parcial)
- `modelo`: Filtro por modelo (búsqueda parcial)
- `skip`: Número de registros a saltar (paginación)
- `limit`: Número máximo de registros (paginación)

### Endpoints de Ventas (`/ventas`)

| Método | Endpoint | Descripción | Estado |
|--------|----------|-------------|--------|
| POST | `/ventas` | Crear nueva venta | ✅ Implementado |
| GET | `/ventas` | Listar ventas (con paginación y filtros) | ✅ Implementado |
| GET | `/ventas/{venta_id}` | Obtener venta por ID | ✅ Implementado |
| PUT | `/ventas/{venta_id}` | Actualizar venta | ✅ Implementado |
| DELETE | `/ventas/{venta_id}` | Eliminar venta | ✅ Implementado |
| GET | `/ventas/auto/{auto_id}` | Ventas de un auto específico | ✅ Implementado |
| GET | `/ventas/comprador/{nombre}` | Ventas por nombre de comprador | ✅ Implementado |
| GET | `/ventas/{venta_id}/with-auto` | Venta con información del auto | ✅ Implementado |

**Parámetros de filtro adicionales:**
- `fecha_inicio`: Filtro por fecha de inicio (ISO format)
- `fecha_fin`: Filtro por fecha de fin (ISO format)
- `precio_min`: Filtro por precio mínimo
- `precio_max`: Filtro por precio máximo
- `skip`: Número de registros a saltar (paginación)
- `limit`: Número máximo de registros (paginación)

---

## Ejemplos de Uso

### Crear un Auto

**Request:**
```http
POST /autos
Content-Type: application/json

{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456"
}
```

### Crear una Venta

**Request:**
```http
POST /ventas
Content-Type: application/json

{
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "auto_id": 1,
    "fecha_venta": "2024-03-15T10:30:00"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "auto_id": 1,
    "fecha_venta": "2024-03-15T10:30:00"
}
```

### Obtener Auto con Ventas

**Request:**
```http
GET /autos/1/with-ventas
```

**Response (200 OK):**
```json
{
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "TOY2023COR123456",
    "ventas": [
        {
            "id": 1,
            "nombre_comprador": "Juan Pérez",
            "precio": 25000.00,
            "fecha_venta": "2024-03-15T10:30:00"
        }
    ]
}
```

### Búsquedas con Filtros

**Buscar autos por marca y modelo:**
```http
GET /autos?marca=Toyota&modelo=Corolla&skip=0&limit=10
```

**Filtrar ventas por rango de fechas:**
```http
GET /ventas?fecha_inicio=2024-01-01T00:00:00&fecha_fin=2024-12-31T23:59:59
```

**Filtrar ventas por rango de precios:**
```http
GET /ventas?precio_min=20000&precio_max=30000
```

---

## Validaciones Implementadas

### Validaciones de Auto

- ✅ **Año**: Debe estar entre 1900 y el año actual
- ✅ **Número de chasis**: Debe ser único en el sistema y alfanumérico
- ✅ **Marca**: Campo obligatorio, no puede estar vacío
- ✅ **Modelo**: Campo obligatorio, no puede estar vacío
- ✅ **Unicidad de chasis**: Validación a nivel de base de datos y aplicación

### Validaciones de Venta

- ✅ **Precio**: Debe ser mayor a 0
- ✅ **Nombre del comprador**: Campo obligatorio, no puede estar vacío
- ✅ **Fecha de venta**: No puede ser una fecha futura
- ✅ **Auto_id**: Debe existir en el sistema (validación de integridad referencial)
- ✅ **Integridad referencial**: Validación antes de crear/actualizar venta

---

## Arquitectura y Patrones de Diseño

### Patrón Repository

Se implementó el patrón Repository para abstraer el acceso a datos:

- **`AutoRepository`**: Gestiona todas las operaciones CRUD de la entidad Auto
- **`VentaRepository`**: Gestiona todas las operaciones CRUD de la entidad Venta

**Ventajas:**
- Separación de la lógica de negocio del acceso a datos
- Facilita el testing y mantenimiento
- Permite cambiar la implementación de persistencia sin afectar el resto del código

### Dependency Injection

FastAPI utiliza dependency injection para inyectar las dependencias (sesiones de base de datos, repositories) en los endpoints, facilitando el testing y la mantenibilidad.

### Separación de Responsabilidades

El proyecto está organizado en módulos con responsabilidades claras:
- **models.py**: Definición de modelos de datos
- **database.py**: Configuración de base de datos
- **repository.py**: Lógica de acceso a datos
- **autos.py / ventas.py**: Lógica de endpoints y validaciones
- **main.py**: Configuración de la aplicación

### Principios SOLID

- **Single Responsibility**: Cada clase tiene una única responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Liskov Substitution**: Interfaces bien definidas
- **Interface Segregation**: Interfaces específicas y cohesivas
- **Dependency Inversion**: Dependencias inyectadas, no hardcodeadas

---

## Características Adicionales Implementadas

### Paginación
Todos los endpoints de listado soportan paginación mediante parámetros `skip` y `limit`:
- Valores por defecto: `skip=0`, `limit=100`
- Validación de parámetros (limit máximo: 1000)

### Búsquedas Parciales
- Búsqueda de autos por marca y modelo (case-insensitive, búsqueda parcial)
- Búsqueda de ventas por nombre de comprador (case-insensitive, búsqueda parcial)

### Filtros Avanzados
- Filtros por rango de fechas en ventas
- Filtros por rango de precios en ventas

### Manejo de Errores
- **400 Bad Request**: Errores de validación o datos inválidos
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Errores de validación de Pydantic

### Documentación Automática
- Swagger UI integrado en `/docs`
- ReDoc integrado en `/redoc`
- Documentación generada automáticamente desde el código

---

## Pruebas y Validación

### Métodos de Prueba

El sistema puede ser probado mediante:

1. **Documentación Interactiva (Swagger UI)**: http://localhost:8000/docs
   - Permite probar todos los endpoints directamente desde el navegador
   - Incluye ejemplos de requests y responses

2. **Herramientas Externas**:
   - Postman
   - Insomnia
   - curl

3. **Script de Prueba de Conexión**:
   ```bash
   python test_connection.py
   ```

### Ejemplo con curl

```bash
# Crear un auto
curl -X POST "http://localhost:8000/autos" \
  -H "Content-Type: application/json" \
  -d '{"marca": "Toyota", "modelo": "Corolla", "año": 2023, "numero_chasis": "TOY2023COR123456"}'

# Listar autos
curl "http://localhost:8000/autos?skip=0&limit=10"

# Crear una venta
curl -X POST "http://localhost:8000/ventas" \
  -H "Content-Type: application/json" \
  -d '{"nombre_comprador": "Juan Pérez", "precio": 25000.00, "auto_id": 1, "fecha_venta": "2024-03-15T10:30:00"}'
```

---

## Solución de Problemas Comunes

### Error de conexión a PostgreSQL

**Síntomas:**
- Error al iniciar la aplicación
- Mensaje: "could not connect to server"

**Soluciones:**
1. Verificar que PostgreSQL esté ejecutándose
2. Verificar que la base de datos `autos_db` exista
3. Verificar las credenciales en el archivo `.env`
4. Verificar que el puerto 5432 esté disponible
5. Ejecutar `python test_connection.py` para diagnosticar

### Error al crear tablas

**Síntomas:**
- Error al iniciar la aplicación
- Mensaje relacionado con creación de tablas

**Soluciones:**
1. Verificar que la base de datos esté creada
2. Verificar que el usuario tenga permisos para crear tablas
3. Verificar que no haya conflictos con tablas existentes
4. Las tablas se crean automáticamente al iniciar la aplicación

### Error de validación

**Síntomas:**
- Error 422 al crear/actualizar recursos
- Mensajes de validación de Pydantic

**Soluciones:**
1. Verificar que todos los campos requeridos estén presentes
2. Verificar que los tipos de datos sean correctos
3. Verificar que las validaciones personalizadas se cumplan (año, precio, etc.)
4. Revisar la documentación en `/docs` para ver los esquemas esperados

---

## Consideraciones Técnicas

### Seguridad
- Las variables de entorno se cargan desde archivo `.env` (no incluido en repositorio)
- Validaciones robustas en todos los endpoints
- Manejo apropiado de errores sin exponer información sensible

### Performance
- Paginación implementada para evitar cargar grandes volúmenes de datos
- Índices en campos de búsqueda frecuente (numero_chasis)
- Pool de conexiones configurado para optimizar el uso de recursos

### Mantenibilidad
- Código bien documentado con docstrings
- Separación clara de responsabilidades
- Uso de tipos para facilitar el mantenimiento
- Estructura de proyecto organizada

### Escalabilidad
- Arquitectura preparada para agregar nuevas entidades
- Patrón Repository facilita cambios en la capa de persistencia
- Endpoints diseñados para soportar crecimiento de datos

---

## Referencias

- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentación oficial de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de Pydantic](https://docs.pydantic.dev/)

