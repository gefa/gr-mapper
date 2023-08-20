#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys
import re
# Check if the script has at least two arguments
if len(sys.argv) < 4:
    print("Error: Please provide two arguments for param1, param2, param3.")
    # sys.exit(1)
    # use some defaults
    p1_arg = "41" # tx,, rx gain =0
    p2_arg = 0 # grand
    p3_arg = "12" # timeout
else:
    # Get the first two arguments
    p1_arg = sys.argv[1]
    p2_arg = sys.argv[2]
    p3_arg = sys.argv[3]
# Convert the arguments to float numbers and store as strings
try:
    param1 = str(float(p1_arg))
    param2 = str(int(p2_arg))
    param3 = str(int(p3_arg))
except ValueError:
    print("Error: Invalid arguments. Please provide valid float numbers.")
    sys.exit(1)

# Print the values (for demonstration purposes)
print("param1:", param1)
print("param2:", param2) 
print("param3:", param3) 
def execute_commands(commands, timeout):
    #process1 = subprocess.Popen(command1, shell=True, stdin=subprocess.PIPE)
    process2 = subprocess.Popen(commands.split(' '), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    #print("process2",process2)
    last_nbits_line = ''
    last_pft_line = ''
    cput = ''
    memo = ''
    ber = ''
    start_time = time.time()
    label,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits=[0],[0],[0],[0],[0],[0],[0]
    for line in process2.stdout:
        #print(line.strip())  # Print the subprocess output
        if "CPU" in str(line):
            cput = str(line).split(" ")[1]
        if "Mem" in str(line):
            memo = str(line).split(" ")[1]
        if "pft" in str(line): #str(line).strip().split()[0]: # if line starts with "pft"
            last_pft_line = str(line)
            goodLine = str(line).split(" ")
            #print(goodLine)
            index=0
            subl = [d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits]
            for i,item in enumerate(goodLine):
              if "pft" in item:
                index = i
                #print("index",i)
                for c,su in enumerate(subl): 
              #if index!=0:
                  #print(goodLine[i+c+1])
                  su[0]=(int(goodLine[i+c+1].replace("\\n'","")))
                break
            #print(d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits)
        ''' try:
              index = goodLine.index("pft")
              print(index)
              for i,subl in enumerate([label,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits]):
                subl.append( goodLine[index+i])
            except ValueError:
              pass
        
        if "NBits" in str(line):
            #print(f"\rProcessing item {i}", end='', flush=True)
            #print(f"\r"+str(line), end='', flush=True)
            last_nbits_line=str(line)
            #print(last_nbits_line, last_pft_line, end='', flush=True)
            #print(str(line).strip().split())
            str_list=str(line).strip().split()
            #if ber value > 0:
#            ber_idx = str_list.index("BER:")
            ber_idx =0
            for _,element in enumerate(str_list):
                if "BER" in element:
                    ber_idx=_
            if ber_idx==0:
                error("BER not in NBits line, garbled stdout?")
            ber_str = (str_list[ber_idx+1]).replace("\\n'",'')
            ber=float(re.findall(r'\d+\.\d+E[-+]?\d+', ber_str)[0])
            
            try:
              ber=float(ber_str)
            except ValueError:
              ber_match = re.search(r'BER: (\d+\.\d+)', ber_str)
              if ber_match:
                ber = float(ber_match.group(1))
            finally:
              ber = -1
              return -1
            
            if ber > 0.0:
                print(str(line))
                #label1, nbits, label2, nerror, label3, ber = str(line).strip().split()
                print(f'pft: {d_pass} {d_fail} {d_total} {fix1bits} {fix2bits} {fix3bits}')
                print(f'Mem: {memo}')
                print(f'CPU: {cput}')
                print(f'BER: {ber}')
                break
        '''
        if (start_time+18<time.time()):
          if "O" in str(line):
            print("Overflow")
            process2.terminate()
            process2.wait()
            return -1
        
          if "U" == str(line)[0]:
            print("Underflow")
            process2.terminate()
            process2.wait()
            return -1
        
        #elif "message buffer overflowing" in str(line):
        #    print(f"\r"+last_nbits_line+last_pft_line+"message buffer overflowing", end='\n', flush=True)
        if (start_time+timeout<time.time()):
            total_time =  time.time()-start_time-4# 4sec starup time
            print('')
            print('THR: {}'.format(d_pass[0]*32/total_time))# 32bits is pkt len
            print(f'pft: {d_pass[0]} {d_fail[0]} {d_total[0]} {fix1bits[0]} {fix2bits[0]} {fix3bits[0]}')
            print(f'Mem: {memo}')
            print(f'CPU: {cput}')
            print(f'BER: {ber}')
            break
            #process2.terminate()
            #process2.wait()
            #return -1
        print(f"\r"+last_pft_line, end='', flush=True)
        #print(last_nbits_line, last_pft_line, end='', flush=True)
    process2.terminate()
    #time.sleep(timeout)
    #process1.communicate('\n'.encode())  # Sends an Enter character to stdin
    #process2.communicate('\n'.encode())
    #os.killpg(os.getpgid(process2.pid), signal.SIGINT)
    process2.wait()
    return 0
import datetime
current_datetime = datetime.datetime.now()
current_month = current_datetime.strftime("%B")  # Full month name
current_date = current_datetime.strftime("%d")  # Day of the month (zero-padded)
current_hour = current_datetime.strftime("%H")  # Hour in 24-hour format (zero-padded)
current_minute = current_datetime.strftime("%M")  # Minute (zero-padded)
current_second = current_datetime.strftime("%S")  # Second (zero-padded)
# Combine the individual components into a single string
formatted_datetime = f"{current_month} {current_date}, {current_hour}:{current_minute}:{current_second}"
#print(formatted_datetime)
file = 'bersim_snr_'+str(param1)+'_'+formatted_datetime.replace(' ','_')+'.txt' #+'_grand_'+str(param2)+'_tout_'+str(param3)+formatted_datetime.replace(' ','_')+'.txt'
#file = f"sim_noise_{formatted_datetime}_{param1}_{param2}_{param3}_auto.txt"
print(file)
command2 = './prbs_test_crc_usrp.py -t '+param1+' -g '+param2#+' -g '+param3 #+" > "+str(file)
timeout = float(param3)
ret = -1
while (ret != 0):
    ret = execute_commands(command2, timeout)
exit()
'''
    process1 = subprocess.Popen(command1, shell=True, stdin=subprocess.PIPE)
    process2 = subprocess.Popen(command2, shell=True, stdin=subprocess.PIPE)
    time.sleep(timeout)
    process1.communicate('\n'.encode())  # Sends an Enter character to stdin
    process2.communicate('\n'.encode())
    #os.killpg(os.getpgid(process2.pid), signal.SIGINT)
    process2.wait()
    #os.killpg(os.getpgid(process1.pid), signal.SIGINT)
    process1.wait()
'''

# first run receive flowgraph, then, second run usrp one
command1 = ' '#"/home/gefa/workspace/grand7_grc3.11/pkt_rcv.py > "+per_file
command2 = param1+'.py -t 69' #+' -g '+param2+' > '+file
commands = command1+" & "+command2
timeout = int(param3)  # Time in seconds
execute_commands(commands, timeout)

def parse_file(file_path):
    nbit = 0
    nerror = 0
    ber = -1.0
    with open(file_path, 'r') as file:
        for line in file: # we only need last line of pft
            if line.startswith('NBits'):
                label1, _nbit, label2, _nerror, label3, _ber = line.strip().split()
                nbit = int(_nbit)
                nerror = int(_nerror)
                ber = float(_ber)
    return nbit, nerror, ber

# Packet error rate
file_path = file #per_file  # file path with recorded PER measurements
nbit, nerror, ber = parse_file(file_path)
print(f'BER: {ber}', 'NBits', nbit, 'NErrors', nerror)

