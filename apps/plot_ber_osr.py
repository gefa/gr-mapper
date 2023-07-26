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
def berawgn_qpsk(EbN0):
    """ Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0) """
    return 0.5 * erfc(math.sqrt(10**(float(EbN0)/10)))
if __name__ == "__main__":
    EbN0_min = 0
    EbN0_max = 12
    EbN0_range = range(EbN0_min, EbN0_max+1)
    ber_bpsk = [berawgn(x)      for x in EbN0_range]
    # prbs_ber 300sec 32k rate 192frame_width 10^-2 offsets OSR=2
    #ber_simu_ = [0.5, 0.5, 0.5, 0.42434, 0.27182, 0.15956, 0.099878, 0.030814, 0.0094221, 0.0014812, 0.00023757, 0.00013504, 2.7085e-05]
    # prbs_ber 300sec 32k rate 192frame_width 0 offsets OSR=2
    #ber_simu_0offset = [0.5, 0.5, 0.5, 0.39183, 0.23055, 0.087862, 0.036105, 0.010274, 0.0019474, 0.00017307, 1.0738e-05, 4.2107e-07, 0] --> this is 5min
    # 2min
    ber_simu_0offset = [0.5, 0.5, 0.5, 0.39245, 0.21601, 0.089189, 0.037173, 0.010862, 0.0018578, 0.00016278, 9.4915e-06, 0, 0]
    # prbs_ber 3600sec 32k rate, SNR=5-12
    #ber_simu_3k6s = [0.45761, 0.41122, 0.2094, 0.044405, 0.0045761, 0.0009639, 0.00016751, 3.4753e-07]
    # prbs_ber_crc  ibid
    #ber_simu_crc = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, ]
    # prbs_ber 300sec 32k rate 192frame_width 0 offsets OSR=4
    ber_simu_ = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.40898, 0.3128, 0.11032, 0.039758, 0.011004, 0.0021708, 0.00020053]
    f = pylab.figure()
    s = f.add_subplot(1,1,1)
    #s.rcParams.update({'font.size': 14})
    s.semilogy(EbN0_range, ber_bpsk, 'g-.', label="Theoretical uncoded QPSK")
    #s.semilogy(EbN0_range, ber_qpsk, 's-.', label="Theoretical uncoded BPSK")
    s.semilogy(EbN0_range, ber_simu_, 'r-o', label="Simulated uncoded QPSK OSR=4")
    s.semilogy(EbN0_range, ber_simu_0offset, 'b-o', label="Simulated uncoded QPSK OSR=2")
    #s.semilogy(EbN0_range, ber_simu_3k6s[2:], 'g-o', label="Simulated uncoded QPSK long")
    #s.semilogy(EbN0_range, ber_simu_crc, 'b-o', label="Simulated CRCcoded QPSK")
    #s.semilogy(EbN0_range, ber_simu_viterbi, 'r-o', label="Simulated Viterbi")
    s.set_title('BER Simulation')
    s.set_xlabel('Eb/N0 (dB)')
    s.set_ylabel('BER')
    s.legend()
    s.grid()
    pylab.show()
