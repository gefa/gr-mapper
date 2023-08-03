#!/usr/bin/env python

import numpy
from gnuradio import gr
import prbs_base

class prbs_sink_f(gr.sync_block):
    def __init__(self, which_mode="PRBS31", reset_len=100000, skip=100000):
        gr.sync_block.__init__(self,
            name="prbs_sink_f",
            in_sig=[numpy.float32],
            out_sig=[])
        self.base = prbs_base.prbs_base(which_mode, reset_len)
        self.nbits = 0.0
        self.nerrs = 0.0
        self.skip  = skip

    def work(self, input_items, output_items):
        inf = input_items[0]
        # print(len(inf)) # len here varies few 100s to few 1000s
        inb = (inf > 0).astype('int8')
        # print(inb)
        gen = self.base.gen_n(len(inb))
        if(self.nitems_read(0) > self.skip):
            # only count bit errors after first skip bits
            self.nerrs += numpy.sum(numpy.bitwise_xor(inb, gen).astype('float32'))
            self.nbits += len(inb)
        if self.nbits > 0:
            print "NBits: %d \tNErrs: %d \tBER: %.4E"%(int(self.nbits), int(self.nerrs), self.nerrs/self.nbits)
            #print "NBits: %d \tNErrs: %d \tBER: %g"%(int(self.nbits), int(self.nerrs), self.nerrs/self.nbits)
        return len(inf)

