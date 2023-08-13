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
    EbN0_min = 4
    EbN0_max = 10
    EbN0_range = range(EbN0_min, EbN0_max+1)
    ber_bpsk = [berawgn(x)      for x in EbN0_range]
    xrange1=[11,14,17,20,23,26,30,33]
    yrange1=[0.05474,0.015105,0.0077571,0.0010027,0.00062133,0.00033845,6.2218e-05,4.1153e-05]
    xrange1g=[11,14,17,20,23,26,30,33]
    yrange1g=[0.043661,0.0095109,0.0065167,0.0024261,0.001783,0.00090752,0.00093805,0.00085558]# more overflows at higher gain?
    xrange1g64=[11,14,17,20,23,26,30,33]
    yrange1g64=[0.050531,0.043954,0.015,0.0038905,0.0020079,0.00034102,0.0,9.0941e-08]#
    xrange2=[5,15,25,35,45,55,65,]#75,85] # works in wider range, almost aline with short range
    yrange2=[0.24511,0.011913,0.00041699,2.7185e-07,0.0,0.0,0.0,] 
    #xrange21=[5,15,25,35,45]#,55,65,]#75,85] # doubleing tout doesnt improve so 60s is good enough
    #yrange21=[0.24492,0.011817,0.00050549,3.8225e-05,7.5919e-06]
    xrange3=[4,5,6,7,8,9,10] # old curve
    yrange3=[0.22298, 0.087213, 0.03737, 0.010088, 0.0018753, 0.00017928, 1.0067e-05]#osr2

    f = pylab.figure()
    s = f.add_subplot(1,1,1)
    #s.semilogy(EbN0_range, ber_bpsk, 'k-o', label="OTA BPSK ")
    s.semilogy(xrange1, yrange1, 'b-o', label="OTA BPSK ")
    s.semilogy(xrange1g, yrange1g, 'g-o', label="OTA BPSK GRAND-1")
    s.semilogy(xrange1g64, yrange1g64, 'm-o', label="OTA BPSK GRAND-1 64")
    s.semilogy(xrange2, yrange2, 'r-o', label="OTA BPSK wideRange")
    #s.semilogy(xrange21, yrange21, 'c-o', label="OTA BPSK 120secTout")
    #s.semilogy(xrange3, yrange3, 'y-o', label="OTA BPSK OSR2orig")

    s.set_title('BER OTA Experiment')
    s.set_xlabel('Tx gain (dB)')
    s.set_ylabel('BER')
    s.legend()
    s.grid()
    pylab.show()
