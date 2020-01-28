import pymodbus

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.server.asynchronous import StartSerialServer
from pymodbus.client.sync import ModbusSerialClient

import time

# Configure the service logging
import logging
logging.basicConfig(filename='modbusData.log',level=logging.DEBUG)
log = logging.getLogger()

# Data Register addresses
VOLTS_L1_TO_NEUTRAL = 44059
AMPS_L1 = 44056
KVA = 44013

# Initialize PowerScout as remote datastore 
# note: MIGHT REQUIRE ModbusSparseDataBlock instead!!
powerScout = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # discrete input contacts
    co = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # discrete output coils
    hr = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # analog output holding registers
    ir = ModbusSequentialDataBlock(0x0000, [16]*0x270E)) # analog input registers
context = ModbusServerContext(slaves=powerScout, single=True)

client = ModbusSerialClient(method='rtu',port='/dev/ttyTHS2',parity='N',stopbits=1,bytesize=8,baudrate=9600,timeout=3)
# Establish connection
client.connect()

# Run the server
StartSerialServer(context, port='/dev/pts/3', timeout=1)

# Send data request
value = client.read_holding_registers(VOLTS_L1_TO_NEUTRAL,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(AMPS_L1,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(KVA,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

time.sleep(20)

value = client.read_holding_registers(VOLTS_L1_TO_NEUTRAL,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(AMPS_L1,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(KVA,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

time.sleep(20)

value = client.read_holding_registers(VOLTS_L1_TO_NEUTRAL,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(AMPS_L1,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

value = client.read_holding_registers(KVA,16,unit=0)
buffer = "Requested value %d\n" % value
log.info(buffer)

time.sleep(20)

# Receive data 
# Handshake?
