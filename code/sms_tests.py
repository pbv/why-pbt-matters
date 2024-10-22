#
# Test SMS packing/unpacking functions using Hypothesis
# Pedro Vasconcelos, 2024

from hypothesis import given, assume, event, settings, Verbosity
import hypothesis.strategies as st

# code under test
from sms_example import pack, unpack

# Attempt 1
#
# Packing followed by unpacking should be the identity,
# i.e. for all bytestrings s, unpack(pack(s)) == s

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
# NB: this may generate few bytes of edge values (0 and 127)
int7 = st.integers(min_value=0, max_value=127)
bytes_of_int7 = st.lists(int7).map(bytes)

@settings(max_examples=500)
@given(bytes_of_int7)
def test_round_trip_2(seq):
    assert unpack(pack(seq)) == seq

#
# Attempt 3
# Generate 7-bit integers with a higher probability of edge cases
# 33% int7, 33% 0s, 33% 127s
#
int7e = st.one_of(st.just(0), int7, st.just(127))
bytes_of_int7e = st.lists(int7e).map(bytes)

@settings(max_examples=500)
@given(bytes_of_int7e)
def test_round_trip_3(seq):
    assert unpack(pack(seq)) == seq


# ------------------------------------------------------------------
# The following attempts intend to investigate what examples fail.
# The property is:
# for all, s in <some strategy>, unpack(pack(s)) != s
# -------------------------------------------------------------------

#
# Attempt 4
# Generate only sequences of given length 
def bytes_of_len(size):
    return st.lists(int7, min_size=size, max_size=size).map(bytes)

# Check if all sequences of length 8 fail:
@settings(max_examples=500)
@given(bytes_of_len(8))
def test_fail_trip_1(seq):
      assert unpack(pack(seq)) != seq


#
# Attempt 5
#
# Generate sequences of a given length that end in 0
def bytes_of_len_end0(size):
    return bytes_of_len(size-1).map(lambda seq: seq+b'\000')

# Check if all sequences of length 8 that end in 0 fail
@settings(max_examples=500)
@given(bytes_of_len_end0(8))
def test_fail_trip_2(seq):
    assert unpack(pack(seq)) != seq



#
# Attempt 6
# Generalized conjecture:
# Enconding fails for sequences of lengths 8, 16, 24, ... ending in 0
#
bytes_len8n_end0 = st.one_of((bytes_of_len_end0(8*n) for n in (1,2,3)))

@settings(max_examples=500)
@given(bytes_len8n_end0)
def test_fail_trip_3(seq):
    event(f'len(seq) = {len(seq)}')
    assert unpack(pack(seq)) != seq
