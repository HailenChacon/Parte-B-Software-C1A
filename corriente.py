from pymodbus.server.sync import StartSerialServer, ModbusRtuFramer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
import random
import threading
import time

def mA_to_register(current_mA):
   
    return int((current_mA - 4) * 1000 / 16)


store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0, [0]*100)  
)
context = ModbusServerContext(slaves=store, single=True)


def update_register():
    while True:
        try:

            simulated_current = random.uniform(4, 20)  
            register_value = mA_to_register(simulated_current)  

           
            slave_context = context[0]  
            slave_context.setValues(3, 0, [register_value])  
            print(f"Simulando corriente: {simulated_current:.2f} mA -> Registro: {register_value}")

            time.sleep(1)  # Actualiza cada segundo
        except Exception as e:
            print(f"Ocurrió una excepción en update_register: {e}")


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
