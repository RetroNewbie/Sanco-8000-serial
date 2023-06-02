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

def wait_for_confirm():
    # return
#     print("wait")
    while 1:
            x = ser.read(1)
            # print(x)
            if x == b'\x06' : return
# Pause the program for 1 second to avoid overworking the serial port
# b'\x06'

data = []
filename = "DATASTARCOM"
# filename = "KANABAS COM"
print("Reading file")


data.append(b'\x02')
# wait_for_confirm()
for char in filename:
        data.append(char.encode('ascii'))
data.append(b'\x03')

with open("DATASTAR.COM",'rb') as file:
        b_count = 0
        while True:
            if b_count==128:
                    b_count = 0
                    data.append(b'\x17')
            x = file.read(1)
            if x == b"":
                break # end of file
            data.append(x)
            b_count +=1
            

# data.insert(24320,b'\x04')
if data[-1] == b'\x17' : data.pop() 
else:
        while b_count<128:
                b_count+=1
                data.append(b'\x00')
data.append(b'\x04')
data.append(b'\x18')
data.append(b'\x04')
data.append(b'\x18')


# #TEST
# with open("myout.txt",'wb') as file:
#         for i in data:
#                 file.write(i)
# quit()

from tqdm import tqdm
print(f"Sending file (size={len(data)} byte)")
# print(data)
# BLock at ~16k/17k
first_three = True
p_count = -13
for i in tqdm(range(len(data))):
        ser.write(data[i])
    
#     time.sleep(0.001)
        if first_three and data[i] == b'\x03':
                first_three = False
                wait_for_confirm()

        # if i!=0 and i%(16384 + 13 + int((i-13)/128))==0:
        if p_count==16384+128:
                p_count=0
                wait_for_confirm()
        if (ser.inWaiting() > 0):
                x = ser.read(1)
                print(f" {i} - {data[i]} - {x}")
        #     if x != b'\x06':
        #         wait_for_confirm()
        p_count+=1
#       time.sleep(0.01)
#       if i>header_length:
#            wait_for_confirm()   

# ser.write(0x18)


