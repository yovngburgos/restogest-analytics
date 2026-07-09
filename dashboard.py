import streamlit as st
import pandas as pd
import sqlite3

# 1. Configuración de la página web del Dashboard
st.set_page_config(page_title="RestoGest Analytics", page_icon="📊", layout="wide")

# Título principal en la pantalla
st.title("📊 RestoGest - Panel de Control Analítico")
st.markdown("Bienvenido al sistema de reportería automatizada para el administrador del restaurante.")
st.markdown("---")

# 2. Conectarnos a la base de datos SQLite usando código nativo de Python para análisis
def cargar_datos():
    # Creamos una conexión directa al archivo de la base de datos
    conn = sqlite3.connect("restogest.db")
    
    # Con Pandas (pd.read_sql), extraemos la información combinando las dos tablas usando SQL Inner Join
    query = """
    SELECT p.id as pedido_id, p.fecha_hora, p.mesa, p.total,
           d.producto, d.cantidad, d.precio_unitario
    FROM pedidos p
    INNER JOIN detalles_pedidos d ON p.id = d.pedido_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Cargar los datos guardados en un DataFrame de Pandas
try:
    df_ventas = cargar_datos()
    
    # ---- SECCIÓN 1: LOS INDICADORES CLAVE (KPIs) ----
    st.header("📈 Indicadores Generales del Día")
    
    # Pandas calcula métricas clave de negocio con un solo método
    total_recaudado = df_ventas["total"].unique().sum() # Suma los totales únicos de cada pedido
    total_pedidos = df_ventas["pedido_id"].nunique()    # Cuenta cuántos pedidos únicos hay
    ticket_promedio = total_recaudado / total_pedidos if total_pedidos > 0 else 0
    
    # Creamos 3 columnas visuales bonitas en la web con Streamlit
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Ingresos Totales", value=f"${total_recaudado:,.0f} CLP")
    col2.metric(label="Cantidad de Pedidos", value=total_pedidos)
    col3.metric(label="Ticket Promedio por Mesa", value=f"${ticket_promedio:,.0f} CLP")
    
    st.markdown("---")
    
    # ---- SECCIÓN 2: GRÁFICOS ANALÍTICOS ----
    st.header("📊 Análisis de Productos y Preferencias")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("🛒 Los productos más vendidos")
        # Agrupamos por producto, sumamos las cantidades y ordenamos de mayor a menor
        df_productos = df_ventas.groupby("producto")["cantidad"].sum().reset_index()
        df_productos = df_productos.sort_values(by="cantidad", ascending=False)
        
        # Streamlit dibuja un gráfico de barras interactivo automáticamente pasándole el DataFrame
        st.bar_chart(data=df_productos, x="producto", y="cantidad")
        
    with col_der:
        st.subheader("📋 Tabla de Datos Brutos")
        # Mostramos la tabla interactiva de datos para que el usuario pueda explorarla o filtrarla
        st.dataframe(df_ventas, use_container_width=True)

# ---- SECCIÓN 3: AUTOMATIZACIÓN (CIERRE DE CAJA) ----
    st.markdown("---")
    st.header("🤖 Automatización de Procesos")
    st.markdown("Presiona el botón para ejecutar las tareas automatizadas de fin de jornada.")

    if st.button("🚀 Ejecutar Cierre de Caja Automatizado"):
        with st.spinner("Procesando datos y generando reportes..."):
            import datetime
            
            # 1. Creamos el nombre del archivo con la fecha
            fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
            nombre_archivo = f"reporte_cierre_{fecha_hoy}.xlsx"
            
            # 2. Guardamos los datos a un Excel real usando openpyxl (lo instalamos antes)
            df_ventas.to_excel(nombre_archivo, index=False)
            
            # 3. Mostramos las animaciones de éxito
            st.success("✅ ¡Tarea completada con éxito!")
            st.balloons()
            
            st.info(f"💾 Archivo '{nombre_archivo}' generado automáticamente en la raíz del proyecto.")
            st.write("📨 **Simulación de flujo:** Reporte adjuntado y enviado con éxito al correo del administrador.")

except Exception as e:
    st.warning("Aún no hay suficientes datos registrados en la base de datos o el archivo no se ha creado.")
    st.info("Asegúrate de haber ingresado pedidos desde la interfaz de FastAPI anteriormente.")

