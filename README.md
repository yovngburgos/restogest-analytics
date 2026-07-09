# 📊 RestoGest Analytics - API & Dashboard de Control

¡Bienvenido a **RestoGest Analytics**! Este es un proyecto de extremo a extremo (End-to-End) diseñado para resolver un problema crítico en la gestión gastronómica: la centralización de pedidos en tiempo real y la automatización del análisis financiero y operativo para la toma de decisiones.

El sistema combina una arquitectura de microservicio (API) capaz de recibir transacciones continuamente, con una plataforma analítica visual e interactiva orientada al administrador del negocio.

---

## 🚀 Características Principales

* **API Transaccional en Tiempo Real:** Desarrollada con FastAPI para la ingesta rápida y segura de pedidos desde mesas o canales digitales.
* **Base de Datos Relacional Eficiente:** Persistencia estructurada mediante SQLite y controlada a través del ORM SQLAlchemy.
* **Métricas de Negocio Automatizadas:** Cálculo inmediato de KPIs clave como Ingresos Totales, Ticket Promedio por Mesa y conteo de órdenes activas mediante Pandas.
* **Visualización Interactiva:** Dashboard gráfico dinámico construido con Streamlit para identificar preferencias de consumo (productos más vendidos) al instante.
* **Automatización de Procesos (RPA):** Módulo de "Cierre de Caja" que genera reportes automáticos en formato Excel (`.xlsx`) simulando un flujo de envío directo al correo de la gerencia.

---

## 🛠️ Tecnologías y Herramientas Utilizadas

* **Lenguaje principal:** Python 3.12
* **Desarrollo del Backend / API:** FastAPI & Uvicorn
* **Base de Datos:** SQLite & SQLAlchemy (ORM)
* **Análisis y Manipulación de Datos:** Pandas
* **Visualización de Datos / Dashboard:** Streamlit
* **Motor de Reportes:** OpenPyXL
* **Control de Versiones:** Git & GitHub

---

## 📐 Arquitectura del Proyecto

El flujo de los datos dentro del ecosistema sigue la siguiente estructura:

1. **Ingesta:** Los pedidos entran en formato JSON a través del endpoint `POST /pedidos/` de nuestra API.
2. **Persistencia:** SQLAlchemy valida los tipos de datos y los almacena de forma relacional en dos tablas conectadas (`pedidos` y `detalles_pedidos`).
3. **Análisis:** El script del dashboard realiza un `INNER JOIN` nativo vía SQL para extraer la información y Pandas procesa las tablas analíticas.
4. **Visualización:** Streamlit renderiza los componentes gráficos interactivos en el navegador web del usuario final.

---

## 💻 Instalación y Configuración Local

Si deseas clonar este proyecto y ejecutarlo en tu entorno local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/yovngburgos/restogest-analytics.git](https://github.com/yovngburgos/restogest-analytics.git)
cd restogest-analytics
