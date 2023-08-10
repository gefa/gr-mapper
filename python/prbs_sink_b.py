#!/usr/bin/env python

import numpy
import numpy as np
from gnuradio import gr
import prbs_base
import time
def permuteUnique(nums):
    res =[]
    perm = []
    cnt = {n:0 for n in nums}
    for n in nums:
        cnt[n]+=1
    
    def dfs():
        if len(perm) == len(nums): # complete permutation
            res.append(list(perm)) # copy list in python2 and python3
            return
        
        for n in cnt:
            if cnt[n] > 0:
                perm.append(n)
                cnt[n] -= 1
                
                dfs()
                
                cnt[n] += 1
                perm.pop()
                
    dfs()
    return np.array(res)
class prbs_sink_b(gr.sync_block):
    def __init__(self, which_mode="PRBS31", reset_len=100000, skip=100000):
        gr.sync_block.__init__(self,
            name="prbs_sink_b",
            in_sig=[numpy.int8],
            out_sig=[])
        self.base = prbs_base.prbs_base(which_mode, reset_len)
        self.nbits = 0.0
        self.nerrs = 0.0
        self.skip  = skip
        self.work_time = 0
        self.n = reset_len
        self.f0 = permuteUnique( (self.n)*[0] ) # no correction
        self.f1 = permuteUnique( (self.n-1)*[0]+[1] )
        #self.f2 = permuteUnique( (self.n-2)*[0]+[1,1] )
        #self.f3 = permuteUnique( (self.n-3)*[0]+[1,1,1] )
        self.flips = np.concatenate((self.f0, self.f1)).astype('float32') # , self.f2, self.f3
    def work(self, input_items, output_items):
        t1_start = time.time()
        inb = input_items[0]
        #print(len(inb))
        gen = self.base.gen_n(len(inb))
        if(self.nitems_read(0) > self.skip):
            # only count bit errors after first skip bits
            
            step=160
            grand = [0,0,0,0]
            for i, j in zip(np.arange(0, len(inb), step), np.arange(0, len(gen), step)):
              subinb = inb[i:i+step]
              subgen = gen[i:i+step]
              nerr= numpy.sum(numpy.bitwise_xor(subinb, subgen).astype('float32'))
              bitd = int(nerr)
              if (bitd>=0 and bitd <=3):
                grand[bitd] = grand[bitd] + 1
              '''
              # grand correct bits
              isfixed=False
              for fix in self.flips:
                #print(type(fix), type(inb[i:i+step]))
                tryfix = numpy.bitwise_xor(inb[i:i+step], fix).astype('float32')
                # if fixed
                if numpy.sum(numpy.bitwise_xor(tryfix, gen[i:i+step]).astype('float32'))==0:
                 isfixed=True
                 break
              if isfixed!=True:
                self.nerrs += numpy.sum(numpy.bitwise_xor(inb[i:i+step], gen[i:i+step]).astype('float32'))  
            '''
            print("GRAND ",grand)
            
            self.nerrs += numpy.sum(numpy.bitwise_xor(inb, gen).astype('float32'))
            self.nbits += len(inb)
        if self.nbits > 0:
            print "NBits: %d \tNErrs: %d \tBER: %.4E \tTime: %.4E"%(int(self.nbits), int(self.nerrs), self.nerrs/self.nbits, self.work_time)
            #print "NBits: %d \tNErrs: %d \tBER: %g"%(int(self.nbits), int(self.nerrs), self.nerrs/self.nbits)
        t1_stop = time.time()
        self.work_time = self.work_time+ t1_stop-t1_start
        return len(inb)

