#
# Test AI-generated run-length encoding functions using Hypothesis
# Pedro Vasconcelos 2024

from hypothesis import given, assume, event, settings, Verbosity
import hypothesis.strategies as st

from rle_chat import rle_encode, rle_decode
# from rle_chat2 import rle_encode, rle_decode
# from rle_chat3 import rle_encode, rle_decode
# from rle_chat4 import rle_encode, rle_decode
# from rle_chat5 import rle_encode, rle_decode


#
# Experiment 1: round-trip property for arbitrary strings 
#

@given(st.text())
def test_decode_encode_1(s):
    assert rle_decode(rle_encode(s)) == s

#
# Experiment 2: restrict generation to strings without digits
#
# a strategy for non-digits Unicode characters
nodigits = st.characters(exclude_categories=('Nd','Nl','No'))

@settings(max_examples=500)
@given(st.text(alphabet=nodigits))
def test_decode_encode_2(s):
    assert rle_decode(rle_encode(s)) == s
    
#
# Experiment 3: collect statistics
#

@settings(max_examples=500)
@given(st.text(alphabet=nodigits))
def test_decode_encode_3(s):
    event(f'longest = {longest_count(s)}')
    assert rle_decode(rle_encode(s)) == s


#
# Compute the maximum size of repeat groups
# NB: this duplicates part of the RLE implementation;
# refactoring the code could improve this
#
def longest_count(s):
    if s == '':
        return 0
    count = 1
    maxcount = 0
    i = 1
    prev = s[0]
    while i < len(s):
        if s[i] == prev:
            count = count+1
        else:
            maxcount = max(count, maxcount)
            count = 1
            prev = s[i]    
        i = i+1    
    return max(count,maxcount)


#
# Experiment 4
# Improve test case distribution
#
# generator for sequences with longer repeated identical characters
counter = st.integers(min_value=0, max_value=20)
longrepeat = st.builds(lambda count,char: ''.join(count*[char]),
                       counter, nodigits)

# combine the two strategies with equal probability
combined = st.one_of(st.text(nodigits), longrepeat)

@settings(max_examples=500)
@given(combined)
def test_decode_encode_4(s):
    event(f'longest = {longest_count(s)}')
    assert rle_decode(rle_encode(s)) == s


# generate parenthesis more frequently
nodigits2 = st.one_of(nodigits, st.sampled_from("()"))
@settings(max_examples=500)
@given(st.text(alphabet=nodigits2))
def test_decode_encode_5(s):
    assert rle_decode(rle_encode(s)) == s
