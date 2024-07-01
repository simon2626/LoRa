import signal
import sys
import threading
import pygame
import serial
import time

# allow multiple joysticks
joy = []

# Arduino USB port address (try "COM5" on Win32)
usbport = "COM5"

# define usb serial connection to Arduino
ser = serial.Serial(usbport, 9600 )

pos_x = '00'
pos_y = '00'
pos_z = '00'
pos_v = '00'
T_pos = '00'


# handle joystick event
def handleJoyEvent(e):

    global pos_x,pos_y,pos_z,pos_v,T_pos

    while True:
        if e.type == pygame.JOYAXISMOTION:
            axis = "unknown"
            if (e.dict['axis'] == 0):
                axis = "X"
        
            if (e.dict['axis'] == 1):
                axis = "Y"
        
            if (e.dict['axis'] == 2):
                axis = "V"
        
            if (e.dict['axis'] == 3):
                axis = "Z"
        
            if (axis != "unknown"):
        
                val = e.dict['value']
        
                if(val == 0):
        
                    val = 0
        
                elif (val > 0):
        
                     val = int(round(50 + 50 * (e.dict['value'])-1,0))
        
                else:
        
                     val = int(round(50 * abs(e.dict['value'])-1,0))
        
        
                ms = "Axis: %s; Value: %f" % (axis, e.dict['value'])
        
                # uncomment to debug
        
                output(ms, e.dict['joy'])            # uncomment to debug
        		
                # X to Servo 1
                if (axis == "X"):
        
                    if(e.dict['value'] == 0):
        
                        pos_x = "00"
        
                    elif (e.dict['value'] > 0):
        
                        pos_x = int(round(50 + 50 * (e.dict['value'])-1,0))
        
                    elif(e.dict['value'] < 0):
        
                        pos_x = int(round(50 - 50 * abs(e.dict['value']),0))
        
                        if(int(pos_x) < 10 ):
        
                            pos_x = '0%s'%(pos_x)
        
        
        
                   # print ("X Servo ", pos_x)
        
                #Throttle to Servo 2
                if (axis == "Y"):
        
                    if(e.dict['value'] == 0):
        
                        pos_y = "00"
        
                    elif (e.dict['value'] > 0):
        
                        pos_y = int(round(50 + 50 * (e.dict['value'])-1,0))
        
                    elif(e.dict['value'] < 0):
        
                        pos_y = int(round(50 - 50 * abs(e.dict['value']),0))
        
                        if(int(pos_y) < 10 ):
        
                            pos_y = '0%s'%(pos_y)
        
        
                   # print ("y Servo ", pos_y)
        
        
        
                #Twsit to Servo 3
                if (axis == "V"):
        
                    if(e.dict['value'] == 0):
        
                        pos_v = "00"
        
                    elif (e.dict['value'] > 0):
        
                        pos_v = int(round(50 + 50 * (e.dict['value'])-1,0))
        
                    elif(e.dict['value'] < 0):
        
                        pos_v = int(round(50 - 50 * abs(e.dict['value']),0))
        
                        if(int(pos_v) < 10 ):
        
                            pos_v = '0%s'%(pos_v)
        
        
                   # print ("v Servo ", pos_v)
        
        
        
                #Throttle to servo 4
                if (axis == "Z"):
        
                    if(e.dict['value'] == 0):
        
                        pos_z = "00"
        
                    elif (e.dict['value'] > 0):
        
                        pos_z = int(round(50 + 50 * (e.dict['value'])-1,0))
        
                    elif(e.dict['value'] < 0):
        
                        pos_z = int(round(50 - 50 * abs(e.dict['value']),0))
        
                        if(int(pos_z) < 10 ):
        
                            pos_z = '0%s'%(pos_z)
        
        
                    #print ("z Servo ", pos_z)
            T_pos =str( pos_v )+ str(pos_x) + str(pos_y) + str(pos_z)
            
            
            # uncomment to debug
            print("T_pos valeu",T_pos)
            print("V Servo  ",pos_v)
            print("X Servo  ",pos_x)
            print("Y Servo  ",pos_y)
            print("Z Servo  ",pos_z)
            print("\r\n")

              
            
        
        
        
        elif e.type == pygame.JOYBUTTONDOWN:
            str1 = "Button: %d" % (e.dict['button'])
            # uncomment to debug
            output(str1, e.dict['joy'])
            # Button 0 (trigger) to quit
            if (e.dict['button'] == 0):
                print ("Bye!\n")
                #ser.close()
                quit()
                
        if pygame.event.peek():
            e = pygame.event.poll()
            pygame.event.clear()

        ReadWriteSerial(T_pos)

        
        
    
	




# print the joystick position
def output(line, stick):
    print ("Joystick: %d; %s" % (stick, line)  )

#read & write to/from serial port
def ReadWriteSerial(inputvar):
    if ser.isOpen() != True:
        ser.open()
        

    # keyboard input
    #//inputvar = str(inputvar)
    # send the character to the device
    # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
    print("Serial output %s\n\r" % inputvar)
    ser.write(bytes((inputvar + '\r\n'),encoding = 'ascii'))

    time.sleep(0.1)
    
    outputvar = ''
    # let's wait one second before reading output (let's give device time to answer)
    while ser.inWaiting() > 0:
           outputvar += str(ser.read(1), encoding='ascii')
           

    
    
    if outputvar != '':
        print(outputvar)
        print("\r\n")
	
	
    ser.close()

# wait for joystick input  
#def joystickControl():  
    #while True:

     #   pygame.event.clear()
      #  e = pygame.event.wait()  
       # if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN):  
        #    print(e) 


        
            

            

# main method
def main():
    # initialize pygame
    pygame.joystick.init()
    pygame.display.init()

    if not pygame.joystick.get_count():
        print ("\n Please connect a joystick and run again.\n" )
        quit()

    print ("\n%d joystick(s) detected." % pygame.joystick.get_count())

    for i in range(pygame.joystick.get_count()):
        myjoy = pygame.joystick.Joystick(i)
        myjoy.init()
        joy.append(myjoy)
        print( "Joystick %d: " % (i) + joy[i].get_name()  )

    print ("Depress trigger (button 0) to quit.\n" )

    # run joystick listener loop
    e = pygame.event.poll()
    handleJoyEvent(e) 
    #joystickControl()

# allow use as a module or standalone script
if __name__ == "__main__":
    main()
