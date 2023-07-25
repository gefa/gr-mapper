#!/usr/bin/env python2

import math
import numpy
try:
    from scipy.special import erfc
except ImportError:
    print "Error: could not import scipy (http://www.scipy.org/)"
    sys.exit(1)

try:
    import pylab
except ImportError:
    print "Error: could not import pylab (http://matplotlib.sourceforge.net/)"
    sys.exit(1)
def berawgn(EbN0):
    """ Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0) """
    return 0.5 * erfc(math.sqrt(10**(float(EbN0)/10)))
if __name__ == "__main__":
    EbN0_min = 7
    EbN0_max = 12
    EbN0_range = range(EbN0_min, EbN0_max+1)
    ber_theory = [berawgn(x)      for x in EbN0_range]
    print "Simulating uncoded BPSK..."
    # prbs_ber 300sec 32k rate
    ber_simu_ = [0.040517, 0.0098053, 0.00063209, 6.0279e-05, 3.2626e-05, 2.4952e-06]
    # prbs_ber_crc  300sec 32k rate
    ber_simu_crc = [0.04942, 0.012197, 0.0015112, 5.6594e-05, 1.8952e-05, 1.8952e-06]
    #ber_simu_bpsk   = [simulate_ber(x, False) for x in EbN0_range]
    #print "Simulating Viterbi..."
    #ber_simu_viterbi   = [simulate_ber(x, True) for x in EbN0_range]

    f = pylab.figure()
    s = f.add_subplot(1,1,1)
    s.semilogy(EbN0_range, ber_theory, 'g-.', label="Theoretical uncoded BPSK")
    s.semilogy(EbN0_range, ber_simu_, 'r-o', label="Simulated uncoded QPSK")
    s.semilogy(EbN0_range, ber_simu_crc, 'b-o', label="Simulated CRCcoded QPSK")
    #s.semilogy(EbN0_range, ber_simu_viterbi, 'r-o', label="Simulated Viterbi")
    s.set_title('BER Simulation')
    s.set_xlabel('Eb/N0 (dB)')
    s.set_ylabel('BER')
    s.legend()
    s.grid()
    pylab.show()
