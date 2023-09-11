#!/usr/bin/env python3
import subprocess
import re
#import matplotlib.pyplot as plt
TRIALS=5
import csv
from datetime import datetime
import sys
if len(sys.argv) < 2:
    print("Error: Please provide abandonment threshold.")
    # sys.exit(1)
    # use some defaults
    p1_arg = "0" # grand threshold
else:
    # Get the threshold parameter 
    p1_arg = sys.argv[1]
def run_script():
    snr_values = []
    mem_values = []
    cpu_values = []
    ber_values = []
    d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits = [],[],[],[],[],[]
    list_of_lists = [d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits]
    for _,snr in enumerate([4,4.5,5.0,5.5,6.0]):
      print('SNR',snr,_)
      ber_values.append([]);cpu_values.append([]);mem_values.append([])
      for sublist in list_of_lists:
        sublist.append([])
      for trial in range(TRIALS):
        print("trial",trial)
        output = subprocess.check_output(['python3', 'check.py',str(snr),p1_arg,'6'], universal_newlines=True)
        lines = output.strip().split('\n')
        print(lines[-4])
        pft = lines[-4]
        mem_line = lines[-3]
        cpu_line = lines[-2]
        ber_line = lines[-1]
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
        mem_values[_].append(float(mem_line.split(' ')[1]))
        cpu_values[_].append(float(cpu_line.split(' ')[1]))
        #if () # if total is zero then we have to run longer, if fail is zero we run longer
        ber_values[_].append( float(pft.split(' ')[2])/float(pft.split(' ')[3]) ) # d_fail/d_total
        #ber_values[_].append(float(ber_line.split(' ')[1]))
        snr_values.append(snr)
        print(ber_values[_])
        #print(snr_values)
    return snr_values, ber_values, cpu_values, mem_values,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits

# Run the script and collect SNR and PER values
# per_values = [0.0, 0.045454545454545456, 0.019801980198019802, 0.009900990099009901, 0.02247191011235955, 0.0, 0.01, 0.0, 0.0]
# snr_values = [9.099746666666666, 9.3467, 10.317246666666668, 10.386196666666669, 8.962946666666666, 8.949133333333334, 10.323726666666667, 8.919163333333334, 9.505416666666667]
# [0.0, 0.0, 0.012195121951219513, 0.0, 0.0]
# [10.161136666666666, 10.357946666666665, 10.022413333333335, 10.184676666666666, 10.155076666666666]
snr_values, ber_values, cpu_values, mem_values,d_pass,d_fail,d_total,fix1bits,fix2bits,fix3bits = run_script()
# ber_values = [0.058824, 0.12651, 0.083333, 7.2464]
# snr_values = [3, 4, 5, 6]
# Plot PER values versus SNR values
print("snr",snr_values)
print("bler",ber_values)
print("cpu",cpu_values)
print("mem",mem_values)
print("pass",d_pass)
print("fail",d_fail)
print("total",d_total)
print("fix1",fix1bits)
print("fix2",fix2bits)
print("fix3",fix3bits)
snr = snr_values
bler = ber_values
# Flatten the bler list
flat_bler = [value for sublist in bler for value in sublist]

# Create a list of (SNR, BLER) pairs
data = list(zip(snr, flat_bler))

# Generate a timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Define the CSV file name with a timestamp
csv_file = f"snr_bler_grand_{p1_arg}_{timestamp}.csv"

# Write the data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SNR", "BLER"])  # Write header
    writer.writerows(data)  # Write data

print(f"Data saved to {csv_file}")
exit()
plt.scatter(snr_values, ber_values)
plt.xlabel('SNR')
plt.ylabel('BER')
plt.title('BER vs SNR')
plt.show()

