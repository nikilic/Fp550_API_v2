import inspect
#from serialtest_1Def import *
#import serialtest_1Def
import serial
import time

from commands_v1 import *
import config

if config.sim == False:
    port = serial.Serial("/dev/ttyUSB0", baudrate=19200, timeout=14.0)

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
    lenbyte=0x20+4+len(data)
    packet = packet + chr(lenbyte)  #<< 0x20 + 4 + data.b.length
    packet=packet+ chr(seq_num())  #'\x22' #SEQ
    packet=packet+chr(cmd)
    packet=packet +data
    packet=packet+chr(PA1)
    packet=packet+bcc(packet)
    packet=packet+chr(ETX)
    
    for character in packet:
      print character, character.encode('hex'),';',
    print '-->'
       
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
        eot=0
        bIx=0
        print" RECEIVED packet from FP550"
        while eot==0:
            for c in port.read():
                if c=='\x16':
                    print "ACK",
                    break
                line.append(c)
                bIx=bIx+1
                #print len(line), hex(ord(c)),';;',           

                if c=='\x03' : # or c=='\x16':
                    eot=1
                    print 'eot'
                    #print line
                    str1 = "".join(line)
                    #str1=[:-3]
                    print "Article:"
                
                    print (repr(str1).replace(" ",""))
                    print 'bIx=', bIx
                    line=[]
                elif c=='\x01':
                    bIx=1
                    break
                elif bIx==2:
                    print "--->"
                    pck_Len=hex(ord(c))
                    #print 'LEN', hex(ord(c))
                    break
                elif  bIx==3:
                    pck_Seq=hex(ord(c))
                    #print'SEQ', hex(ord(c))
                    break
                elif  bIx==4:
                    pck_Cmd=hex(ord(c))
                    #print'CMD', hex(ord(c))
                    break
                elif c=='\x04':
                    print 'Poz EndData-x04=',bIx
                    #print line[4:(bIx-1)]
                    bSt=bIx
                    str_data = "".join(line[4:(bIx-1)])
                    #print 'DATA Field:', #str_data
                    #print (repr(str_data).replace(" ",""))
                    pck_Data=repr(str_data).replace(" ","")
                    break
                elif c=='\x05':
                    print 'Poz EndStatus -x05=',bIx
                    #str_data1 = "".join(line[bSt:(bIx-1)])
                    pck_Sts=line[bSt:(bIx-1)]
                    print 'STATUS Field:', line[bSt:(bIx-1)]
                    break
                        
            
        #            break
        #    break
        print line, 'out' # print what is received
    else:
        pck_Data = "\x80\x80\x80\x85\x80\xba" #hex(ord("a"))
        pck_Len = hex(ord("b"))
        pck_Cmd = hex(ord("c"))
        pck_Seq = hex(ord("d"))
        pck_Sts = hex(ord("e"))

def cmd_Get_Diag():
    print "GET DIAG x47_______________________"
    data=""
    cmd1= 0x47 #GET_STATUS #\x4A
    pack=build_packet(cmd1, data)
    '''for character in pack:
      print character, character.encode('hex'),';',
    print '-->' '''
    port.write(pack)  #send packet
    print "GET DIAG-Command -Sent"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
def cmd_Get_PIB():
    output = []
    output.append("GET PIB 0x63______________________")
    data=""
    cmd1= 0x63 #GET_PIB #\x63
    pack=build_packet(cmd1, data)
    ''' for character in pack:
      print character, character.encode('hex'),#';',
    print '-->' '''
    if config.sim == False:
        port.write(pack)  #send packet
    #print "GET PIB-Command SENT"
    #print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    output.append('Recv class packet data:'+str(pck_Data))
    output.append('LEN='+str(pck_Len))
    output.append('SEQ='+str(pck_Seq))
    output.append('Cmd='+str(pck_Cmd))
    output.append('Status:'+str(pck_Sts))
    if config.sim == False:
        port.close
    return output
    
def cmd_Last_Fwrite():
    print "LAST_FWrite 0x77______________________"
    data=""
    cmd1= 0x6e #Last Fwrite#\x77
    pack=build_packet(cmd1, data)
    for character in pack:
      print character, character.encode('hex'),';',

    port.write(pack)  #send packet
    print "Last_Fwrite-Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
def cmd_Read_Article():
    global fn
#    fn="F"
    print "Read Artical0x6b______________________"
    data=fn
    cmd1= 0x6B #Read Article x6B
    pack=build_packet(cmd1, data)
    for character in pack:
      print character, character.encode('hex'),';',

    port.write(pack)  #send packet
    print "Read Artical-Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    
def cmd_Write_Article():
    print "Write Artical  0x6b______________________"
#    data="p'"+"\xc3\x31\x2c\x31\x30\x2c\xc0\xf0\xf2\xe8\xea\xe0\xeb"
    
    usr_go=input ("Press enter to continue:")
    data="P"+"\x80"+"00034,55,ROBA-AB"
#    data="P" + chr(0xC0)+"1234,666,ROBA-AA"
    print 'from write art:',data
    cmd1= 0x6B #Write Article x6B
    pack=build_packet(cmd1, data)
    for character in pack:
      print character, character.encode('hex'),';',

    port.write(pack)  #send packet
    print "Write Artical-Command SENT"
    print 'SeqNum:',hex(seq_num(False))
    # Prijem odziva od FP
    recv()

def cmd_Get_Tax():
    print "GET TAXES _______________________"
    usr_go=input ("Press 1 to continue:")
    data=""
    cmd1= 0x61 # ???GET_STATUS #\x4A
    pack=build_packet(cmd1, data)
    for character in pack:
      print character, character.encode('hex'),';',
    print '-->'
    port.write(pack)  #send packet
    print "GET TAX-Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()



def cmd_Get_Status():
    print "GET STATUS _______________________"
    usr_go=1
    #usr_go=input ("Press enter to continue:")
    data=""
    cmd1=GET_STATUS #\x4A
    pack=build_packet(cmd1, data)
    ''' for character in pack:
      print character, character.encode('hex'),';',
    print"WRITE PACKET"
    print '-->' '''
    if config.sim == False:
        port.write(pack)  #send packet
    print "GET STATUS-Command SENT"
    print 'SeqNum:',hex(seq_num(False))
    # Prijem odziva od FP
    recv()
    print 'Recv class packet data:', pck_Data
    print 'LEN=', pck_Len
    print 'SEQ=', pck_Seq
    print 'Cmd=', pck_Cmd
    print 'Status:', pck_Sts
    if config.sim == False:
        port.close
    return pck_Data
    
def cmd_Paper_Move(lines):
    output = []
    output.append("PAPER MOVE________________________")
    cmd1=PAPER_MOVE #'\x2c'
    data=str(int(lines))
    pack=build_packet(cmd1, data)
    ''' for character in pack:
      print character, character.encode('hex'),';:',
    print '-->' '''
    if config.sim == False:
        port.write(pack)  #send packet
    #print "PAPER MOVE-Command SENT"
    #print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    output.append('Recv class packet data:'+str(pck_Data))
    output.append('LEN='+str(pck_Len))
    output.append('SEQ='+str(pck_Seq))
    output.append('Cmd='+str(pck_Cmd))
    output.append('Status:'+str(pck_Sts))
    if config.sim == False:
        port.close
    return output
    
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


def cmd_Get_Date_Time():
    #print "GET Date_TimeS _______________________"
    output = []
    #print (whoami())
    #usr_go=input ("Press enter to continue:")
    data=""
    cmd1=0x3E #GET_Date_time \x3e
    pack=build_packet(cmd1, data)

    if config.sim == False:
        port.write(pack)  #send packet
    output.append("Transmited command:")
    output.append("GET_Date_Time")
    output.append('SeqNum:'+str(hex(seq_num(False))))

    # Prijem odziva od FP
    recv()
    output.append('Recv class packet data: '+str(pck_Data))
    output.append('LEN='+str(pck_Len))
    output.append('SEQ='+str(pck_Seq))
    output.append('Cmd='+str(pck_Cmd))
    output.append('Status:'+str(pck_Sts))
    if config.sim == False:
        port.close
    return output
    
def cmd_Get_Set_Tax():
    usr_go=input ("Press enter to continue:")
    print "GET SET TAX_______________________"
    data=""
    cmd1=0x53 #GET_Set_TAX \x53
    pack=build_packet(cmd1, data)
    ''' for character in pack:
      print character, character.encode('hex'),';',
    print '-->' '''
    port.write(pack)  #send packet
    print "GET SET TAX-Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
    print 'Recv class packet data:', pck_Data
    print 'LEN=', pck_Len
    print 'SEQ=', pck_Seq
    print 'Cmd=', pck_Cmd
    print 'Status:', pck_Sts
    port.close
def cmd_report_ART_All():
    print "Print All articles from DB_ !! Warrning -Long Print !!  _________"
    usr_go=input ("Press enter to continue:")
    data="1"
    cmd1=0x6f #report art_all\x69
    pack=build_packet(cmd1, data)
    ''' for character in pack:
      print character, character.encode('hex'),';',
    print '-->' '''
    port.write(pack)  #send packet
    print "Report ARTICLE_ALL - Command SENT"
    print 'SeqNum:',hex(seq_num(False))

    # Prijem odziva od FP
    recv()
