#!/usr/bin/env python3
import subprocess
import re
import time
#import matplotlib.pyplot as plt
TRIALS=1
def run_script():
    snr_values = []
    thr_values = []
    mem_values = []
    cpu_values = []
    ber_values = []
    d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits = [],[],[],[],[],[]
    list_of_lists = [d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits]
    for _,snr in enumerate([40,40.5,41.0,41.5,42.0]): #OTA 41,44,47,50,53 rxgain 25
      print('SNR',snr,_)
      ber_values.append([]);cpu_values.append([]);mem_values.append([]);thr_values.append([])
      for sublist in list_of_lists:
        sublist.append([])
      for trial in range(TRIALS):
        print("trial",trial)
        output = subprocess.check_output(['python3', 'check_usrp.py',str(snr),'0','12'], universal_newlines=True)
        lines = output.strip().split('\n')
        thr_line = lines[-5]
        print(lines[-4])
        pft = lines[-4]
        mem_line = lines[-3]
        cpu_line = lines[-2]
        ber_line = lines[-1]
        print(thr_line)
        print(pft)
        print(mem_line)
        print(cpu_line)
        print(ber_line)
        '''
        #snr_match = re.search(r'SNR: (\d+\.\d+)', snr_line) # r'^\d+\.\d+E[-+]?\d+$'
        ber_match = re.search(r'BER: (\d+\.\d+)', ber_line)
        #print(ber_line)
        if ber_match:
            #snr_value = float(snr_match.group(1))
            ber_value = float(ber_match.group(1))
            #snr_values.append(snr_value)
            ber_values[_].append(ber_value)
            snr_values.append(snr)
        
        for i,sublist in enumerate(list_of_lists):
            print(pft.split(' ')[1+i])
            num = float(pft.split(' ')[1+i]) # skip label
            #print(_,i,sublist, num)
            sublist[_].append(num)
        '''
        d_pass[_].append(float(pft.split(' ')[1]))
        d_fail[_].append(float(pft.split(' ')[2]))
        d_total[_].append(float(pft.split(' ')[3]))
        fix1bits[_].append(float(pft.split(' ')[4]))
        fix2bits[_].append(float(pft.split(' ')[5]))
        fix3bits[_].append(float(pft.split(' ')[6]))
        thr_values[_].append(float(thr_line.split(' ')[1]))
        mem_values[_].append(float(mem_line.split(' ')[1]))
        cpu_values[_].append(float(cpu_line.split(' ')[1]))
        #if () # if total is zero then we have to run longer, if fail is zero we run longer
        ber_values[_].append( float(pft.split(' ')[2])/float(pft.split(' ')[3]) ) # d_fail/d_total
        #ber_values[_].append(float(ber_line.split(' ')[1]))
        snr_values.append(snr)
        print(ber_values[_])
        print(cpu_values[_])
        print(mem_values[_])
        print(thr_values[_])
        #print(snr_values)
      print("seeping ...")
      time.sleep(10)
    return snr_values, ber_values, cpu_values, mem_values,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits, thr_values

# Run the script and collect SNR and PER values
# per_values = [0.0, 0.045454545454545456, 0.019801980198019802, 0.009900990099009901, 0.02247191011235955, 0.0, 0.01, 0.0, 0.0]
# snr_values = [9.099746666666666, 9.3467, 10.317246666666668, 10.386196666666669, 8.962946666666666, 8.949133333333334, 10.323726666666667, 8.919163333333334, 9.505416666666667]
# [0.0, 0.0, 0.012195121951219513, 0.0, 0.0]
# [10.161136666666666, 10.357946666666665, 10.022413333333335, 10.184676666666666, 10.155076666666666]
snr_values, ber_values, cpu_values, mem_values,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits, thr_values = run_script()
# ber_values = [0.058824, 0.12651, 0.083333, 7.2464]
# snr_values = [3, 4, 5, 6]
# Plot PER values versus SNR values
print("snr",snr_values)
print("bler",ber_values)
print("cpu",cpu_values)
print("mem",mem_values)
print("THR",thr_values)
print("pass",d_pass)
print("fail",d_fail)
print("total",d_total)
print("fix1",fix1bits)
print("fix2",fix2bits)
print("fix3",fix3bits)
exit()
plt.scatter(snr_values, ber_values)
plt.xlabel('SNR')
plt.ylabel('BER')
plt.title('BER vs SNR')
plt.show()

