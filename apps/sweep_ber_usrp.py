#!/usr/bin/env python3
import subprocess
import re
#import matplotlib.pyplot as plt
TRIALS=6
def run_script():
    snr_values = []
    ber_values = []

    for _,snr in enumerate(range(41,50,2)):
      print('SNR',snr,_)
      ber_values.append([])
      for trial in range(TRIALS):
        print("trial",trial)
        output = subprocess.check_output(['python3', 'check_usrp.py',str(snr),'0','0'], universal_newlines=True)
        lines = output.strip().split('\n')
        #snr_line = lines[-2]
        ber_line = lines[-1]

        #snr_match = re.search(r'SNR: (\d+\.\d+)', snr_line)
        ber_match = re.search(r'BER: (\d+\.\d+)', ber_line)

        if ber_match:
            #snr_value = float(snr_match.group(1))
            ber_value = float(ber_match.group(1))
            #snr_values.append(snr_value)
            ber_values[_].append(ber_value)
            snr_values.append(snr)
        print(ber_values[_])
        #print(snr_values)
    return snr_values, ber_values

# Run the script and collect SNR and PER values
# per_values = [0.0, 0.045454545454545456, 0.019801980198019802, 0.009900990099009901, 0.02247191011235955, 0.0, 0.01, 0.0, 0.0]
# snr_values = [9.099746666666666, 9.3467, 10.317246666666668, 10.386196666666669, 8.962946666666666, 8.949133333333334, 10.323726666666667, 8.919163333333334, 9.505416666666667]
# [0.0, 0.0, 0.012195121951219513, 0.0, 0.0]
# [10.161136666666666, 10.357946666666665, 10.022413333333335, 10.184676666666666, 10.155076666666666]
snr_values, ber_values = run_script()
# ber_values = [0.058824, 0.12651, 0.083333, 7.2464]
# snr_values = [3, 4, 5, 6]
# Plot PER values versus SNR values
print("snr",snr_values)
print("ber",ber_values)
exit()
plt.scatter(snr_values, ber_values)
plt.xlabel('SNR')
plt.ylabel('BER')
plt.title('BER vs SNR')
plt.show()

