import pymodbus
import asyncio


from pymodbus.client.asynchronous.serial import (
    AsyncModbusSerialClient as ModbusClient)
from pymodbus.client.asynchronous import schedulers

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.server.asynchronous import StartSerialServer
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.transaction import ModbusAsciiFramer

import time

# Configure the service logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Data Register addresses
VOLTS_L1_TO_NEUTRAL = 44059
AMPS_L1 = 44056
KVA = 44013

# Initialize PowerScout as remote datastore
# note: MIGHT REQUIRE ModbusSparseDataBlock instead!!
#print('setting up the power scout')
#powerScout = ModbusSlaveContext(
#    di = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # discrete input contacts
#    co = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # discrete output coils
#    hr = ModbusSequentialDataBlock(0x0000, [16]*0x270E), # analog output holding registers
#    ir = ModbusSequentialDataBlock(0x0000, [16]*0x270E)) # analog input registers
#context = ModbusServerContext(slaves=powerScout, single=True)

# Run the server
print('starting serial server')
#StartSerialServer(context, port='/dev/ttyTHS2', framer=ModbusAsciiFramer, timeout=1)
print('done connecting to server!')

async def start_async_test(client):

# Send data request and log response
try:
print('we in')
# address, count # of registers to read, slave address
log.debug("Read register for volts")
rr = await client.read_holding_registers(4055, 1, unit = 0x01)
#rr = await client.read_holding_registers(4205, 5, unit=0x01)
log.debug("After two reads")
buffer = "Requested value %d\n" % rr
log.info(buffer)
print('first buffer down!')
print(buffer)
rr = await client.read_holding_registers(AMPS_L1,1,unit=0x01)
buffer = "Requested value %d\n" % rr
log.info(buffer)

rr = client.read_holding_registers(KVA,1,unit=0x01)
buffer = "Requested value %d\n" % rr

log.info(buffer)

#time.sleep(20)

rr = client.read_holding_registers(VOLTS_L1_TO_NEUTRAL,1,unit=0x01)
buffer = "Requested value %d\n" % rr
log.info(buffer)

rr = client.read_holding_registers(AMPS_L1,1,unit=0x01)
buffer = "Requested value %d\n" % rr
log.info(buffer)

rr = client.read_holding_registers(KVA,1,unit=0x01)
buffer = "Requested value %d\n" % rr

log.info(buffer)

#time.sleep(20)

rr = client.read_holding_registers(VOLTS_L1_TO_NEUTRAL,1,unit=0x01)
buffer = "Requested value %d\n" % rr
log.info(buffer)

rr = client.read_holding_registers(AMPS_L1,1,unit=0x01)
buffer = "Requested value %d\n" % rr
log.info(buffer)

rr = client.read_holding_registers(KVA,1,unit=0x01)
buffer = "Requested value %d\n" % rr

log.info(buffer)

#time.sleep(20)
except Exception as e:
for err in e.args:
print(err)
finally:
print(rr)
client.close()

if __name__ == '__main__':
   
    loop, client = ModbusClient(schedulers.ASYNC_IO, port='/dev/ttyTHS2',
                                baudrate=9600, method='ascii', parity='N', stopbits=1, bytesize=8)
    client.connect()
    print('finished clienting')
    loop.run_until_complete(start_async_test(client.protocol))
    loop.close()
