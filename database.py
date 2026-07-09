from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# 1. Creamos la conexión. Le decimos que cree un archivo llamado "restogest.db" 
# que funcionará como nuestra base de datos SQLite.
DATABASE_URL = "sqlite:///./restogest.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 2. Creamos una "Sesión". Esto es como abrir un canal de comunicación abierto 
# para poder guardar, borrar o consultar datos en el futuro.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Esta es la base que usaremos para heredar y crear nuestras tablas.
Base = declarative_base()


# 4. DEFINIMOS LA TABLA DE PEDIDOS (La información general)
class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True) # Un número único que se genera solo (1, 2, 3...)
    fecha_hora = Column(DateTime, default=datetime.datetime.utcnow) # La fecha y hora exacta del pedido
    mesa = Column(Integer) # El número de la mesa que hizo el pedido
    total = Column(Float, default=0.0) # El monto total de dinero de la cuenta
    
    # Esto le dice a Python que este pedido tiene una relación con la tabla de detalles
    detalles = relationship("DetallePedidoDB", back_populates="pedido")


# 5. DEFINIMOS LA TABLA DE DETALLES (Qué platos componen el pedido)
class DetallePedidoDB(Base):
    __tablename__ = "detalles_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    # Esta línea es CLAVE: conecta este detalle con el ID del pedido principal (Llave Foránea)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto = Column(String) # Ejemplo: "Hamburguesa"
    cantidad = Column(Integer) # Ejemplo: 2
    precio_unitario = Column(Float) # Ejemplo: 4500.0

    # Esto nos permite hacer cosas como "detalle.pedido" para saber a qué mesa pertenece
    pedido = relationship("PedidoDB", back_populates="detalles")


# 6. FUNCIÓN DE INICIALIZACIÓN
# Esta función la llamaremos desde el código principal para que revise si el archivo 
# ".db" existe. Si no existe, creará las tablas automáticamente basándose en los modelos de arriba.
def crear_base_de_datos():
    Base.metadata.create_all(bind=engine)