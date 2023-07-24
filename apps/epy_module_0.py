# this module will be imported in the into your flowgraph
from gnuradio import *
import mapper
print("premable")
preamble = (mapper.preamble_generator(32,511,1033)).get_preamble()
print(type(preamble))
binary_string = ''.join(str(bit) for bit in preamble)
print(binary_string)
reversed_binary_string = binary_string[::-1]
print(reversed_binary_string)

