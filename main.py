from machine import I2C, Pin
from bme280 import BME280
from utime import sleep

# Initialisiere den I2C-Bus mit SDA auf GPIO21 und SCL auf GPIO22
i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# Initialisiere den BME280-Sensor an der Adresse 0x76
bme280 = BME280(i2c=i2c, address=0x76)

while True:
    temp = bme280.values[0]  # Temperatur
    hum = bme280.values[2]   # Luftfeuchtigkeit

    print("Temperatur:", temp)
    print("Luftfeuchtigkeit:", hum)
    
    sleep(1)
