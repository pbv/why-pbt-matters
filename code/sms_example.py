#
#  SMS character packing & unpacking
#  2024, Pedro Vasconcelos, based on Haskell code by John Hughes
#
# -- An implementation of character packing and unpacking,
# -- following very closely the specification in
# -- GSM TS 03.38 v5.2.0 subclause 6.1.2.1.1.
# https://www.etsi.org/deliver/etsi_gts/03/0338/05.03.00_60/gsmts_0338v050300p.pdf
#
def pack(seq: bytes) -> bytes:
    '''Pack blocks of 8 7-bit characters into 7 8-bit bytes.'''
    result = []    
    n = len(seq)
    i = 0
    # handle complete blocks of 8 characters
    while n-i>=8:
        a, b, c, d, e, f, g, h = seq[i:i+8]
        result.extend([ a    | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2 | (d<<5)&255,
                        d>>3 | (e<<4)&255,
                        e>>4 | (f<<3)&255,
                        f>>5 | (g<<2)&255,
                        g>>6 | (h<<1)&255])
        i += 8
    #
    # handle fewer than 8 leftover characters
    #
    leftover = n-i
    if leftover == 1:
        a = seq[i]
        result.append(a)
    elif leftover == 2:
        a, b = seq[i:i+2]
        result.extend([ a | (b<<7)&255,
                        b>>1 ])
    elif leftover == 3:
        a, b, c = seq[i:i+3]
        result.extend([ a | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2])
    elif leftover == 4:
        a, b, c, d = seq[i:i+4]
        result.extend([ a | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2 | (d<<5)&255,
                        d>>3])
    elif leftover == 5:
        a, b, c, d, e = seq[i:i+5]
        result.extend([ a | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2 | (d<<5)&255,
                        d>>3 | (e<<4)&255,
                        e>>4])
        
    elif leftover == 6:
        a, b, c, d, e, f = seq[i:i+6]
        result.extend([ a | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2 | (d<<5)&255,
                        d>>3 | (e<<4)&255,
                        e>>4 | (f<<3)&255,
                        f>>5])
    elif leftover == 7:
        a, b, c, d, e, f, g = seq[i:i+7]
        result.extend([ a | (b<<7)&255,
                        b>>1 | (c<<6)&255,
                        c>>2 | (d<<5)&255,
                        d>>3 | (e<<4)&255,
                        e>>4 | (f<<3)&255,
                        f>>5 | (g<<2)&255,
                        g>>6 ])
        
    return bytes(result)


def unpack(seq: bytes) -> bytes:
    '''Unpack blocks of 7 bytes into 8 7-bit characters.'''
    result = []    
    n = len(seq)
    i = 0
    # handle complete blocks 
    while (n-i > 7):
        a, b, c, d, e, f, g = seq[i:i+7]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127,
                        c>>5 | (d<<3)&127,
                        d>>4 | (e<<4)&127,
                        e>>3 | (f<<5)&127,
                        f>>2 | (g<<6)&127,
                        g>>1  
                       ])
        i += 7
    # handle leftover bytes
    leftover = n-i
    if leftover == 1:
        a = seq[i]
        result.append(a&127)
    elif leftover == 2:
        a, b = seq[i:i+2]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127])
    elif leftover == 3:
        a, b, c = seq[i:i+3]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127 ])
    elif leftover == 4:
        a, b, c, d = seq[i:i+4]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127,
                        c>>5 | (d<<3)&127 ])
    elif leftover == 5:
        a, b, c, d, e = seq[i:i+5]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127,
                        c>>5 | (d<<3)&127,
                        d>>4 | (e<<4)&127 ])
    elif leftover == 6:
        a, b, c, d, e, f = seq[i:i+6]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127,
                        c>>5 | (d<<3)&127,
                        d>>4 | (e<<4)&127,
                        e>>3 | (f<<5)&127 ])
    elif leftover == 7:
        a, b, c, d, e, f, g = seq[i:i+7]
        result.extend([ a&127,
                        a>>7 | (b<<1)&127,
                        b>>6 | (c<<2)&127,
                        c>>5 | (d<<3)&127,
                        d>>4 | (e<<4)&127,
                        e>>3 | (f<<5)&127,
                        f>>2 | (g<<6)&127
                       ])
        # check the left-over 7 bits are not zero
        # (which could in principle be another char)
        if g>>1 != 0:
            result.append(g>>1)
                        
    return bytes(result)

# ------------------------------------------------------------
# Manual tests
# ------------------------------------------------------------

def test_bytes(seq):
    assert unpack(pack(seq)) == seq

def run_tests():
    test_bytes(b'')
    test_bytes(b'1')
    test_bytes(b'12')    
    test_bytes(b'123')
    test_bytes(b'1234')
    test_bytes(b'12345')
    test_bytes(b'123456')
    test_bytes(b'1234567')
    test_bytes(b'12345678')
    test_bytes(b'123456789')
    test_bytes(b'1234567890')

if __name__ == "__main__":
    run_tests()
    
    
