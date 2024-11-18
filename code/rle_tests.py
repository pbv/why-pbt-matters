#
# Test AI-generated run-length encoding functions using Hypothesis
# Pedro Vasconcelos 2024

from hypothesis import given, assume, event, settings, Verbosity
import hypothesis.strategies as st
import itertools 

from rle_chat import rle_encode, rle_decode
# from rle_chat2 import rle_encode, rle_decode
# from rle_chat3 import rle_encode, rle_decode
# from rle_chat4 import rle_encode, rle_decode
# from rle_chat5 import rle_encode, rle_decode


#
# Experiment 1: round-trip property for arbitrary strings 
#

@settings(max_examples=500)
@given(st.text())
def test_decode_encode_1(s):
    assert rle_decode(rle_encode(s)) == s

#
# Experiment 2: restrict generation to strings without digits
#
# a strategy for Unicode characters excluding digits
no_digits = st.characters(exclude_categories='N')

@settings(max_examples=500)
@given(st.text(alphabet=no_digits))
def test_decode_encode_2(s):
    assert rle_decode(rle_encode(s)) == s

#
# Experiment 3: collect statistics
#
@settings(max_examples=500)
@given(st.text(alphabet=no_digits))
def test_decode_encode_3(s):
    event(f'longest = {longest_count(s)}')
    assert rle_decode(rle_encode(s)) == s

#
# Compute the maximum length of repeated characters
#
def longest_count(s: str) -> int:
    maxlen = 0
    for _, g in itertools.groupby(s):
        maxlen = max(maxlen, len(list(g)))
    return maxlen

#
# Experiment 4: improve test data generation
#

# generator for long sequences of repeated characters
many_no_digits = st.builds(lambda count, char: count*char,
                           st.integers(min_value=0, max_value=20),
                           no_digits)

# combine the two strategies with equal probability
combined = st.one_of(many_no_digits, st.text(alphabet=no_digits))

@settings(max_examples=500)
@given(combined)
def test_decode_encode_4(s):
    event(f'longest = {longest_count(s)}')
    assert rle_decode(rle_encode(s)) == s


# generate parenthesis more frequently
no_digits2 = st.one_of(no_digits, st.sampled_from("()"))
@settings(max_examples=500)
@given(st.text(alphabet=no_digits2))
def test_decode_encode_5(s):
    assert rle_decode(rle_encode(s)) == s
