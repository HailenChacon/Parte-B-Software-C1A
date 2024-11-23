from pymodbus.server.sync import StartSerialServer, ModbusRtuFramer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
import random
import threading
import time

store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

def update_register():
    while True:
        try:
            # Simular radiación solar en W/m²
            simulated_radiation = random.uniform(0, 1200)  
            register_value = int(simulated_radiation)

            
            slave_context = context[0]  
            slave_context.setValues(3, 5, [register_value])  

            print(f"Simulando radiación solar: {simulated_radiation:.2f} W/m² -> Registro: {register_value}")

            time.sleep(1)  # Actualiza cada segundo
        except Exception as e:
            print(f"Ocurrió una excepción en update_register: {e}")


threading.Thread(target=update_register, daemon=True).start()

# Configura el servidor Modbus RTU
print("Iniciando servidor Modbus esclavo para el Sensor Pyr20 en Windows (RS485)...")
StartSerialServer(
    context=context,
    framer=ModbusRtuFramer,
    port="COM6",  # Cambia por el puerto COM asignado a tu adaptador RS485
    baudrate=9600,
    stopbits=1,
    bytesize=8,
    parity='N'
)
