from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import database # Aquí importamos tu archivo anterior

# 1. Creamos la aplicación de FastAPI
app = FastAPI(title="RestoGest Analytics API")

# 2. Al arrancar, ejecutamos la función que crea el archivo de la base de datos si no existe
database.crear_base_de_datos()

# 3. Esta función ayuda a abrir y cerrar la conexión a la base de datos automáticamente en cada pedido
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- MODELOS DE VALIDACIÓN (Pydantic) ----
# Aquí definimos las "reglas" de qué datos estamos dispuestos a recibir en formato JSON.
class DetallePedidoSchema(BaseModel):
    producto: str
    cantidad: int
    precio_unitario: float

class CrearPedidoSchema(BaseModel):
    mesa: int
    detalles: List[DetallePedidoSchema] # Un pedido contiene una lista de productos


# ---- RUTAS / ENDPOINTS ----

# Ruta de bienvenida (para probar que la API funciona)
@app.get("/")
def inicio():
    return {"mensaje": "API de RestoGest funcionando correctamente"}

# Ruta para RECIBIR y GUARDAR un pedido (POST)
@app.post("/pedidos/")
def crear_pedido(pedido_input: CrearPedidoSchema, db: Session = Depends(get_db)):
    
    # A. Calculamos el total de la cuenta multiplicando cantidad * precio de cada producto
    total_pedido = sum(item.cantidad * item.precio_unitario for item in pedido_input.detalles)
    
    # B. Creamos el registro del Pedido principal en la base de datos
    nuevo_pedido = database.PedidoDB(mesa=pedido_input.mesa, total=total_pedido)
    db.add(nuevo_pedido)
    db.commit()          # Guardamos los cambios
    db.refresh(nuevo_pedido) # Esto nos devuelve el ID (ej: Pedido #1) que generó automáticamente la base de datos
    
    # C. Recorremos los productos que venían en el pedido y los guardamos en la tabla de detalles
    for item in pedido_input.detalles:
        nuevo_detalle = database.DetallePedidoDB(
            pedido_id=nuevo_pedido.id, # Vinculamos el detalle al ID del pedido principal
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.precio_unitario
        )
        db.add(nuevo_detalle)
    
    db.commit() # Guardamos todos los detalles en la base de datos
    
    # Respondemos al cliente que todo salió bien
    return {
        "mensaje": "Pedido registrado con éxito", 
        "pedido_id": nuevo_pedido.id, 
        "total_cuenta": total_pedido
    }