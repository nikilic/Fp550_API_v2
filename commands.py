import inspect
#from serialtest_1Def import *
#import serialtest_1Def
import serial
import time, datetime, os
from flask import url_for
from subprocess import call
from commands_v1 import *
import config

if config.sim == False:
    port = serial.Serial("/dev/ttyUSB0", baudrate=19200, timeout=14.0)
    #port = serial.

# print chr(SALE)
#print SUBTOTAL, TOTAL
def whoami():
    cmd_name=inspect.stack()[1][3]
    cmd_name=cmd_name[4:]
    return cmd_name

def bcc(packet):
    bcc=""
    sum=0
    for c in packet:
        sum=sum+ord(c)
    sum=sum-1
    crc1=(sum&0x000f)+0x30
    crc2=0x30+((sum&0x00f0)>>4)
    crc3=0x30+((sum&0x0f00)>>8)
    crc4=0x30+((sum&0xf000)>>12)
    bcc=chr(crc4)+chr(crc3)+chr(crc2)+chr(crc1)
    return bcc

def build_packet(cmd, data = ""):
#    global seq_num
    packet = ""
    packet = packet + chr(STX) # \x01
    lenbyte =0x20+4+len(data)
    packet = packet + chr(lenbyte)  #<< 0x20 + 4 + data.b.length
    packet=packet+ chr(seq_num())  #'\x22' #SEQ
    packet=packet+chr(cmd)
    packet=packet +data
    packet=packet+chr(PA1)
    packet=packet+bcc(packet)
    packet=packet+chr(ETX)
    
    #for character in packet:
      #print (character, character.encode('hex'),';',)
    print ('-->')
       
    return packet
#Sequence number , svaki poziv inkrementuje, ako je seq_num(false) ne inkrementuje(zadrzava prethodni)
seq=0x1F
def seq_num(incr=True):
    global seq
    if incr:
        seq += 1
    if seq==0x7f:
        seq=0x1f 
    return seq

# Waiting for FP response (ACK, NAK, packet)
def recv():
    global pck_Data
    global pck_Len
    global pck_Cmd
    global pck_Seq, pck_Sts
    if config.sim == False:
        line= []
        ack_s=[]
        eot=0
        bIx=0
        print(" RECEIVED packet from FP550")
#        port_buff = port.read()
#        print (port_buff)
#        port_buff = b"\x01abcdata1\x31\xc1\xc0\x80dddata2\x04STATUS\x05bcc\x03"  #.encode("cp1252")
        '''for c in port_buff:
            line.append(c)
            bIx=bIx+1 
        '''
        while eot == 0:
            for c in port.read():  # port_buff:
                if c == 22:
                    print( "ACK",)
                    ack_s.append(c)
                    break
                line.append(c)
                bIx=bIx+1
                #print len(line), hex(ord(c)),';;',           

                if c == 3:  # or c=='\x16':
                    eot=1
                    print ('eot')
                    #print line
#                    str1 = "".join(line)
                    #str1=[:-3]
                    print ("Article:")
                
#                    print (repr(str1).replace(" ",""))
                    print ('bIx=', bIx)
                    #line=[]
                elif c == 1:
                    bIx=1
                    #  break
                elif bIx == 2:
                    print ("--->")
                    pck_Len = c #hex(ord(c))
                    #print 'LEN', hex(ord(c))
                    #  break
                elif  bIx==3:
                    pck_Seq= c #hex(ord(c))
                    #print'SEQ', hex(ord(c))
                    #  break
                elif  bIx==4:
                    pck_Cmd=c #hex(ord(c))
                    #print'CMD', hex(ord(c))
                    #  break
                elif c == 4:
                    print( 'Poz EndData-x04=',bIx)
                    #print line[4:(bIx-1)]
                    bSt=bIx
                    #str_data = "".join(line[4:(bIx-1)])
                    #print 'DATA Field:', #str_data
                    #print (repr(str_data).replace(" ",""))
                    pck_Data = line[4:bSt]  #repr(str_data).replace(" ","")
                    print(pck_Data)
                    #  break
                elif c == 5:
                    print('Poz EndStatus -x05=',bIx)
                    #str_data1 = "".join(line[bSt:(bIx-1)])
                    pck_Sts=line[bSt:(bIx-1)]
                    print('STATUS Field:', line[bSt:(bIx-1)])
                    #  break
                        
            
        #            break
        #    break
        print ('ACKs ',ack_s)
        print (line, 'out') # print what is received
        print(''.join(chr(x) for x in line))
        print(', '.join(hex(y) for y in line))
    else:
        pck_Data = "\x80\x80\x80\x85\x80\xba" #hex(ord("a"))
        pck_Len = "\x41"
        pck_Cmd = hex(ord("c"))
        pck_Seq = hex(ord("d"))
        pck_Sts = hex(ord("e"))
    output = {
            "ACKS": ack_s,
            "recv_pck_Data": pck_Data,
            "LEN": pck_Len,
            "SEQ": pck_Seq,
            "Cmd": pck_Cmd,
            "Status": pck_Sts
        }
    return output


def cmd_Last_Fwrite():
    # print ("LAST_FWrite 0x77____Date_time__________________")
    data=""
    cmd1= 0x6e #Last Fwrite#\x77
    pack=build_packet(cmd1, data)
    for character in pack:
      print (character, character.encode('hex'),';',)

    port.write(pack)  #send packet
    print ("Last_Fwrite-Command SENT")
    print ('SeqNum:',hex(seq_num(False)))

    # Prijem odziva od FP
    recv()
def cmd_Read_Article():
    global fn
#    fn="F"
    print ("Read Artical0x6b______________________")
    data=fn
    cmd1= 0x6B #Read Article x6B
    pack=build_packet(cmd1, data)
    for character in pack:
      print (character, character.encode('hex'),';',)

    port.write(pack)  #send packet
    print ("Read Artical-Command SENT")
    print ('SeqNum:',hex(seq_num(False)))

    # Prijem odziva od FP
    recv()
    
def cmd_Write_Article():
    print ("Write Artical  0x6b______________________")
#    data="p'"+"\xc3\x31\x2c\x31\x30\x2c\xc0\xf0\xf2\xe8\xea\xe0\xeb"
    
    usr_go=input ("Press enter to continue:")
    data="P"+"\x80"+"00034,55,ROBA-AB"
#    data="P" + chr(0xC0)+"1234,666,ROBA-AA"
    print ('from write art:',data)
    cmd1= 0x6B #Write Article x6B
    pack=build_packet(cmd1, data)
    for character in pack:
      print (character, character.encode('hex'),';',)

    port.write(pack)  #send packet
    print ("Write Artical-Command SENT")
    print ('SeqNum:',hex(seq_num(False)))
    # Prijem odziva od FP
    recv()

    
"""    
def cmd_Non_Fiscal():
    print "MACRO NON FISCAL___________________________"
    cmd1=START_NON_FISCAL_DOC #0x26
    data=''
    pack=build_packet(cmd1, data)

    port.write(pack)  #send packet
    print "start non fiscal Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    
    # ___________________
    cmd1=PRINT_NON_FISCAL_TEXT
    data='POPRAVLJENO********DUSAN'
    print data
    pack=build_packet(cmd1, data)

    port.write(pack)  #send packet
    print "starting received buffer-TEXT non fiscal"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    
    #-_____________________

    
    cmd1=end_NON_FISCAL_DOC    # 0x27 
    data=''
    pack=build_packet(cmd1, data)

    port.write(pack)  #send packet
    print "Command SENT-end non fiscal"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
"""


def cmd_generic(cmd_code,data=""):
    ''' function to be called by the specific FP operationId function '''
    pack=build_packet(hex(int(cmd_code, 16)), data)

    if config.sim == False:
        pack_bytes=pack.encode()
        port.write(pack_bytes)  #send packet

    rec_out = recv()
    return rec_out


def cmd_take_photo():
    """ Make photo by usb camera and save timestamped.jpg into /satic/images/ """
    pass
    lnk = 'http://0.0.0.0:8090/'
    st= datetime.datetime.now().strftime("%Y-%m-%d--%H-%M") # exmp: 2018-07-01--16-57
    ts= str(st) #.split('.')[0] #eliminise miliseconds
    # ts11="/home/pi/Public/WWWpy/static/images/"+ts+".jpg"
    ts1="static/images/"+ts+".jpg"
    wdir= os.getcwd()
    print(ts1)
    print(os.getcwd())
    print(url_for('static', filename='img1.jpg'))
    call(["fswebcam", "-d", "/dev/video0", "-r", "1280x720", "--top-banner", ts1], cwd=wdir)

    return ts1

