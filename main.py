import network
import espnow
import time
from machine import I2C, Pin, deepsleep
from bme280 import BME280
from utime import sleep

# Pin zur Steuerung der Stromversorgung des BME280 (GPIO4)
power_pin = Pin(4, Pin.OUT)

# Initialisiere den I2C-Bus mit SDA auf GPIO21 und SCL auf GPIO22
i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# WLAN-Interface muss aktiv sein, um send()/recv() zu verwenden
sta = network.WLAN(network.STA_IF)  # Oder network.AP_IF
sta.active(True)
sta.disconnect()  # Optional, für ESP8266 relevant

# ESP-NOW initialisieren
e = espnow.ESPNow()
e.active(True)

# MAC-Adressen der Empfänger (Peers)
peer1 = b'\x08\xD1\xF9\xE0\x0E\x94'  # Setze hier die richtige MAC-Adresse für den ersten Empfänger ein
peer2 = b'\x08\xD1\xF9\xDF\xAE\x2C'  # Setze hier die richtige MAC-Adresse für den zweiten Empfänger ein

# Peers hinzufügen
e.add_peer(peer1)  # Ersten Peer hinzufügen
e.add_peer(peer2)  # Zweiten Peer hinzufügen

# Funktion zum Auslesen der Daten vom BME280-Sensor
def read_bme280_data(bme280):
    try:
        # BME280-Daten auslesen
        temp = bme280.values[0]  # Temperatur
        hum = bme280.values[2]   # Luftfeuchtigkeit
        return temp, hum
    except OSError as e:
        print("Fehler beim Auslesen des BME280-Sensors:", e)
        return None, None

# Funktion zum Senden der BME280-Daten an beide Empfänger
def send_bme280_data():
    # Stromversorgung für den BME280 aktivieren
    power_pin.on()
    sleep(1)  # Warte eine Sekunde, damit der Sensor startet

    # BME280-Sensor initialisieren
    bme280 = BME280(i2c=i2c, address=0x76)
    
    # Daten vom BME280 auslesen
    temp, hum = read_bme280_data(bme280)
    
    # Falls Daten vorhanden, Nachricht formatieren und senden
    if temp is not None and hum is not None:
        message = f"Temperatur: {temp}, Luftfeuchtigkeit: {hum}"
        e.send(peer1, message)
        print(f"Daten an Peer1 gesendet: {message}")
        
        e.send(peer2, message)
        print(f"Daten an Peer2 gesendet: {message}")

    # Stromversorgung für den BME280 deaktivieren
    power_pin.off()

# Hauptprogramm
print("Sende BME280-Daten an zwei Empfänger und gehe dann in Deep Sleep...")

# Daten senden
send_bme280_data()

# Deep Sleep für 60 Sekunden (1 Minute)
time_in_ms = 60 * 1000  # 60 Sekunden in Millisekunden
print("Gehe in Deep Sleep für 60 Sekunden...")
deepsleep(time_in_ms)
