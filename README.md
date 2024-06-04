# Hamilton-Modbus

This Python script is used to communicate with a Hamilton ARC pH probe over a serial connection. It uses the `minimalmodbus` and `serial` libraries to establish the connection and communicate with the device.
it is designed to run in Mycodo (https://github.com/kizniche/Mycodo)

## Features

- Lists all available COM ports and attempts to connect to each one.
- Iterates over a range of possible slave addresses to find the correct one.
- Reads from specific registers on the Modbus device.
- Interprets the read data as 32-bit floats.
- Stores (in mycodo databse) OR prints the measurements (if debugging is turned on).

## Requirements

- Python 3.6 or higher
- `minimalmodbus` library
- `pyserial` library

## Usage

1. Install the required libraries with pip:

```bash
pip install minimalmodbus pyserial
```

2. Run the script:

```bash
python hamilton-modbus.py
```

## Debugging

Set the `debug` variable to `True` to print debug messages (True by default). This will print the available COM ports and the success or failure of each connection attempt.

## Note

The script is currently configured to read from registers 2089-2098 and 2409-2418. These register addresses may need to be adjusted depending on the specific Modbus device being used.

