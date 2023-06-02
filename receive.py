import serial

ser = serial.Serial(
        # Serial Port to read the data from
        port='COM7',
 
        #Rate at which the information is shared to the communication channel
        baudrate = 19200,
   
        #Applying Parity Checking (none in this case)
        parity=serial.PARITY_NONE,
 
       # Pattern of Bits to be read
        stopbits=serial.STOPBITS_ONE,
     
        # Total number of bits to be read
        bytesize=serial.EIGHTBITS,
 
        # Number of serial commands to accept before timing out
        timeout=1
)
# b'\x06'



data = []
filename = ""
print("Waiting for data")
while 1:
        if ser.read(1) == b'\x02': break
space_count = 0
while 1:
        x = ser.read(1)
        if x==b'\x03' : break
        if x==b'\x20' : space_count+=1
        if space_count == 4 : 
                filename+="."
                space_count+=1
        else: 
                if x!=b'\x20':
                        filename+=str(x.decode('ascii'))
        ser.write(b'\x06')

print("Receiving file: "+filename)
is_ending = False
b_count = 0
while 1:
        x = ser.read(1)
        if x==b'\x18' and is_ending:
                break
        if x==b'\x04':
                is_ending = True
        else:
                is_ending = False
        if b_count == 128:
                b_count = 0
                print(f" {len(data)} - {x}")
                if x!=b'\x17' and not is_ending:
                     print(f"An error occured while reading the file + {len(data)}")
                     exit()
                continue
        data.append(x)
        b_count+=1
        # ser.write(b'\x06')
print(len(data))
# data.pop()
# data.pop()
# import time
with open(filename,'wb') as file:
        for i in data:
                file.write(i)
        # time.sleep(0.01)
# input("watiting")

# for i in data:
#         ser.write(i)
#         print(ser.read(1))


