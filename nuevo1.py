from pymodbus.server.sync import StartSerialServer, ModbusRtuFramer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
import random
import threading
import time

def mA_to_register(current_mA):
    # El rango de 4-20mA se mapea a 0-1000 en el registro Modbus
    return int((current_mA - 4) * 1000 / 16)

# Configuración de los registros Modbus
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)  # 100 Holding Registers iniciales
)
context = ModbusServerContext(slaves=store, single=True)

# Función para actualizar el registro con datos simulados
def update_register():
    while True:
        try:
            # Simulando valores de corriente entre 4mA y 20mA
            simulated_current = random.uniform(4, 20)  # Corriente entre 4mA y 20mA
            register_value = mA_to_register(simulated_current)  # Convertir corriente a registro

            # Accede al contexto del esclavo para actualizar los valores
            slave_context = context[0]  # Accede al único esclavo configurado
            slave_context.setValues(3, 0, [register_value])  # 3 = Holding Register
            print(f"Simulando corriente: {simulated_current:.2f} mA -> Registro: {register_value}")

            time.sleep(1)  # Actualiza cada segundo
        except Exception as e:
            print(f"Ocurrió una excepción en update_register: {e}")

# Ejecutar la actualización de registros en un hilo
threading.Thread(target=update_register, daemon=True).start()

# Configura el servidor Modbus RTU
print("Iniciando servidor Modbus esclavo en Windows (RS485)...")
StartSerialServer(
    context=context,
    framer=ModbusRtuFramer,
    port="COM6",  # Cambia por el puerto COM asignado a tu adaptador RS485
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N'
)
