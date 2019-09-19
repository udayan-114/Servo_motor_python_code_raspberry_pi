
import smbus
import time
#import tkinter
import RPi.GPIO as GPIO
from random import randint

GPIO.setmode(GPIO.BCM)

# define the servo pins. 
# Here you could change the code and add your pins for example
servoPIN12 = 12
#servoPIN18 = 18
    data = bus.read_i2c_block_data(0x76, 0xAA, 2)
    C5 = data[0] * 256 + data[1]

# Read temperature coefficient of the temperature
    data = bus.read_i2c_block_data(0x76, 0xAC, 2)
    C6 = data[0] * 256 + data[1]

# MS5803_02BA address, 0x76(118)
#		0x40(64)	Pressure conversion(OSR = 256) command
    bus.write_byte(0x76, 0x40)

    time.sleep(0.5)

# Read digital pressure value
# Read data back from 0x00(0), 3 bytes
# D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]

# MS5803_02BA address, 0x76(118)
#		0x50(64)	Temperature conversion(OSR = 256) command
    bus.write_byte(0x76, 0x50)

    time.sleep(0.5)

# Read digital temperature value
# Read data back from 0x00(0), 3 bytes
# D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]

    dT = D2 - C5 * 256
    TEMP = 2000 + dT * C6 / 8388608
    OFF = C2 * 65536 + (C4 * dT) / 128
    SENS = C1 * 32768 + (C3 * dT ) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0

    if TEMP >= 2000 :
            T2 = 0
            OFF2 = 0
            SENS2 = 0
            if TEMP > 4500:
                SENS2 = SENS2-((TEMP-4500)*(TEMP-4500))/8
    elif TEMP < 2000 :
            T2 = (dT * dT) / 2147483648
            OFF2= 3 * ((TEMP - 2000) * (TEMP - 2000))
            SENS2= 7 * ((TEMP - 2000) * (TEMP - 2000)) / 8 
            if TEMP < -1500 :
        
                    SENS2 = SENS2 + 2 * ((TEMP + 1500) * (TEMP +1500))

    TEMP = TEMP - T2
    OFF = OFF - OFF2
    SENS = SENS - SENS2
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) /10
    cTemp = TEMP / 100.0
    fTemp = cTemp * 1.8 + 32



    A= pressure
    if A<1016:
        move1 = randint(0,1)
        p12.ChangeDutyCycle(move1)
       
    elif A>1016:
	move2 = randint(90,91)
       	p12.ChangeDutyCycle(move1)
        time.sleep(1)
	   
		
	
#except KeyboardInterrupt:
        p12.stop()
  #p18.stop()
        GPIO.cleanup()
        time.sleep(1)


#top = Tk()
    

# Output data to screen
    # print ("Pressure : %.2f mbar" %pressure)
    #print ("Temperature in Celsius : %.2f C" %cTemp)
    #print ("Temperature in Fahrenheit : %.2f F" %fTemp)
    #time.sleep(2)
#button1= Button(root, command=start).grid(row=0,column=0)
#label1 = Label(root,textvariable = pressure).grid(row=1, column=0)
#root.mainloop()
#L1 = Label(top,text = "pressure")
#L1.pack(side = LEFT)
#E1 = Entry (top,bd=5)
#E1.pack(side= RIGHT)
#top.mainloop()

