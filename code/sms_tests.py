
#
# Test SMS packing/unpacking functions using Hypothesis
#

from hypothesis import given, assume, event, note, settings, Verbosity, Phase
import hypothesis.strategies as st

# code under test
from sms_example import pack, unpack

# Attempt 1
#
# Packing followed by unpacking should be the identity,
# i.e. for all s, unpack(pack(s)) == s

# `binary' is a library strategy for generating bytestrings
# tested with 500 random examples
#

@settings(max_examples=500)
@given(st.binary())
def test_round_trip_1(seq):
    assert unpack(pack(seq)) == seq

















# ---------------------------------------------------------------------    
#
# Attempt 2
# Generate only 7-bit byte sequences
#
int7 = st.integers(min_value=0, max_value=127)
bytes_of_int7 = st.builds(bytes, st.lists(int7))

@settings(max_examples=500)
@given(bytes_of_int7)
def test_round_trip_2(seq):
    assert unpack(pack(seq)) == seq














#
# Attempt 3
#
# Generate only sequences of a given length
# check if the post condition *always* fails

def bytes_of_len(size):
    return st.builds(bytes,
                     st.lists(int7, min_size=size, max_size=size))


@settings(max_examples=500)
@given(bytes_of_len(8))
def test_fail_trip_1(seq):
      assert unpack(pack(seq)) != seq

#
# Attempt 4
# Generate only sequence that terminate in 0
#
bytes_ending_in_0 = st.builds(lambda seq: seq+b'\000', bytes_of_int7)

@settings(max_examples=500)
@given(bytes_ending_in_0)
def test_fail_trip_2(seq):
    assert unpack(pack(seq)) != seq

    
#
# Attempt 5
#

# Generate sequences of a given length that terminate in 0
def bytes_of_len_end0(size):
    return st.builds(lambda seq: seq+b'\000', bytes_of_len(size-1))

@settings(max_examples=500)
@given(bytes_of_len_end0(8))
def test_fail_trip_3(seq):
    assert unpack(pack(seq)) != seq



#
# Attempt 6
# Test generalized conjecture:
# round trip fails for sequences of length 8, 16, 24, ... ending in 0
#
bytes_len8n_end0 = st.one_of((bytes_of_len_end0(8*n) for n in (1,2,3)))

@settings(max_examples=500)
@given(bytes_len8n_end0)
def test_fail_trip_4(seq):
    assert unpack(pack(seq)) != seq
