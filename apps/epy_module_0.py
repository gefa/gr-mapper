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

def bit_stream_tuple_to_bytes(bit_stream_tuple):
    bit_stream_string = ''.join(str(bit) for bit in bit_stream_tuple)
    bytes_list = [int(bit_stream_string[i:i+8], 2) for i in range(0, len(bit_stream_string), 8)]
    return bytes_list
byte_list = bit_stream_tuple_to_bytes(binary_string)
print("preamble bytes", byte_list)
def bytes_to_bit_stream_tuple(bytes_list):
    binary_string = ''.join(format(byte, '08b') for byte in bytes_list)
    bit_stream_tuple = tuple(int(bit) for bit in binary_string)
    return bit_stream_tuple
bit_stream_tuple = bytes_to_bit_stream_tuple(byte_list)
print("preamble tuple", bit_stream_tuple)

