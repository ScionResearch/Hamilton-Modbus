import minimalmodbus
import serial
import serial.tools.list_ports
import struct

# Initialize instrument as None 
# Set debug to True to print debug messages, False to run code in mycodo
instrument = None
debug = True

# Get a list of all available COM ports
com_ports = [comport.device for comport in serial.tools.list_ports.comports()]
if debug:
    print(f"Available COM ports: {com_ports}")

# Iterate over all available COM ports
for com_port in com_ports:
    # Iterate over a range of possible slave addresses
    for slave_address in range(1, 256):  # Adjust the range as needed
        try:
            # Try to create an instrument object
            temp_instrument = minimalmodbus.Instrument(com_port, slaveaddress=slave_address, debug=False)
            temp_instrument.serial.baudrate = 19200
            temp_instrument.serial.bytesize = 8
            temp_instrument.serial.parity = serial.PARITY_NONE
            temp_instrument.serial.stopbits = 2
            temp_instrument.serial.timeout = 1
            temp_instrument.mode = minimalmodbus.MODE_RTU
            temp_instrument.clear_buffers_before_each_transaction = True

            # Try to read a register to check if the slave address is correct
            temp_instrument.read_register(0)

            # If the read is successful, print a success message
            if debug:
                print(f"Success: COM port {com_port} with slave address {slave_address}")


            # If the read is successful, assign the instrument to the temp_instrument
            instrument = temp_instrument
            break
        except:
            if debug:
                print(f"Failed: COM port {com_port} with slave address {slave_address}")
            continue

    # If an instrument was found, break the outer loop as well
    if instrument is not None:
        break

# If no instrument was found, raise an error
if instrument is None:
    if debug:
        print("Error: No slave device found")
    raise Exception("No slave device found")


# # Create an instrument object
# instrument = minimalmodbus.Instrument('/dev/ttyUSB1', slaveaddress=2, debug=False)
# instrument.serial.baudrate = 19200
# instrument.serial.bytesize = 8
# instrument.serial.parity = serial.PARITY_NONE
# instrument.serial.stopbits = 2
# instrument.serial.timeout = 1
# instrument.mode = minimalmodbus.MODE_RTU
# instrument.clear_buffers_before_each_transaction = True

# Read 10 registers starting from 2090
ph_values = instrument.read_registers(2089, 10, functioncode=3)

# Read 10 registers starting from 2410
temp_values = instrument.read_registers(2409, 10, functioncode=3)

# Combine the register values to form 32-bit integers
ph_int = (ph_values[3] << 16) | ph_values[2]
temp_int = (temp_values[3] << 16) | temp_values[2]

# Convert the 32-bit integers to bytes
ph_bytes = ph_int.to_bytes(4, 'little')
temp_bytes = temp_int.to_bytes(4, 'little')

# Interpret the bytes as 32-bit floats
pH = struct.unpack('f', ph_bytes)[0]
temperature = struct.unpack('f', temp_bytes)[0]

if not debug:
    # Store measurements
    self.store_measurement(channel=0, measurement=round(pH, 2))
    self.store_measurement(channel=1, measurement=round(temperature, 2))

# Print the measurements
if debug:
    print(f"pH: {pH:.2f}")
    print(f"Temperature: {temperature:.2f}")
