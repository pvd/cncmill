#!/usr/bin/python

import serial
import time
import struct
import hal

comm = serial.Serial()
comm.port = "/dev/ttyACM0"
comm.baudrate = 115200
comm.timeout = 1
comm.dtr = True
comm.open()

h = hal.component("ctrlpanel")
h.newpin("mpgXcount", hal.HAL_S32, hal.HAL_OUT)
h.newpin("mpgYcount", hal.HAL_S32, hal.HAL_OUT)
h.newpin("mpgZcount", hal.HAL_S32, hal.HAL_OUT)

# buttons
h.newpin("power", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("home", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("zeroAll", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("zeroX", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("zeroY", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("zeroZ", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("start", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("stop", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("laser", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("feedPlus", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("feedMin", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("jogSpeed1", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("jogSpeed2", hal.HAL_BIT, hal.HAL_OUT)
h.newpin("estop", hal.HAL_BIT, hal.HAL_OUT)

# leds
h.newpin("led_power", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_home", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_zeroAll", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_zeroX", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_zeroY", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_zeroZ", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_start", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_stop", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_laser", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_feedPlus", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_feedMin", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_jogSpeed1", hal.HAL_BIT, hal.HAL_IN)
h.newpin("led_jogSpeed2", hal.HAL_BIT, hal.HAL_IN)


print "Waiting for the board..."
time.sleep(3)
h.ready()

try:
  while 1:
    # repeat this loop every 100ms
    time.sleep(0.1)

    # Prepare the led status value
    ledStatus = h['led_power'];
    ledStatus = ledStatus | h['led_home'] << 1;
    ledStatus = ledStatus | h['led_zeroAll'] << 2;
    ledStatus = ledStatus | h['led_zeroX'] << 3;
    ledStatus = ledStatus | h['led_zeroY'] << 4;
    ledStatus = ledStatus | h['led_zeroZ'] << 5;
    ledStatus = ledStatus | h['led_start'] << 6;
    ledStatus = ledStatus | h['led_stop'] << 7;
    ledStatus = ledStatus | h['led_laser'] << 8;
    ledStatus = ledStatus | h['led_feedPlus'] << 9;
    ledStatus = ledStatus | h['led_feedMin'] << 10;
    ledStatus = ledStatus | h['led_jogSpeed1'] << 11;
    ledStatus = ledStatus | h['led_jogSpeed2'] << 12;

    # create the binary structure and transmit it to the control panel
    outStatus = struct.pack("=BHB", 0x55, ledStatus, 0xAA)
    comm.write(outStatus)

    # keep on reading while there is still data and the sync is not found
    sync = comm.read(1)
    while (len(sync) == 0) and (sync != chr(0x55)):
      print "ctrlpanel: searching for sync"
      sync = comm.read(1)

    # if, at this point, the sync is still not found, start again
    if sync != chr(0x55):
      print "ctrlpanel: sync not found, sending ledstatus again"
      continue

    # read the packet from the serial port
    rawInput = comm.read(15)
    btnStatus = struct.unpack("=iiiHB",rawInput)
  
    # make sure that this is a correct packet by checking the tail byte
    if ( btnStatus[4] != 0xAA ):
      print "Out of sync, flushing rx buffer and trying to resync"
      comm.reset_input_buffer();
    else:
      h['mpgXcount'] = btnStatus[0]
      h['mpgYcount'] = btnStatus[1]
      h['mpgZcount'] = btnStatus[2]
      h["power"] = btnStatus[3] & 0x1
      h["home"] = (btnStatus[3] >> 1) & 0x1
      h["zeroAll"] = (btnStatus[3] >> 2) & 0x1
      h["zeroX"] = (btnStatus[3] >> 3) & 0x1
      h["zeroY"] = (btnStatus[3] >> 4) & 0x1
      h["zeroZ"] = (btnStatus[3] >> 5) & 0x1
      h["start"] = (btnStatus[3] >> 6) & 0x1
      h["stop"] = (btnStatus[3] >> 7) & 0x1
      h["laser"] = (btnStatus[3] >> 8) & 0x1
      h["feedPlus"] = (btnStatus[3] >> 9) & 0x1
      h["feedMin"] = (btnStatus[3] >> 10) & 0x1
      h["jogSpeed1"] = (btnStatus[3] >> 11) & 0x1
      h["jogSpeed2"] = (btnStatus[3] >> 12) & 0x1
      h["estop"] = (btnStatus[3] >> 13) & 0x1
except KeyboardInterrupt:
  raise SystemExit

