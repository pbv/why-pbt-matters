#
# Basic properties based tests using Hypothesis
# 

from hypothesis import given, assume, event, settings, Phase
import hypothesis.strategies as st
import math

# 1) Expressing properties
#
# An integer square root function
def isqrt(n):
    return int(math.sqrt(n))

# A property for testing integer square roots
@given(st.integers(min_value=0))
def test_isqrt(n):
    r = isqrt(n)
    assert r>=0 and r**2<=n and (r+1)**2>n

# 2) Generating data
#
# a strategy for generating odd integers
odds = st.integers().map(lambda x:x*2+1)

# Alternative we could use filter instead of map:
# odds = st.integers().filter(lambda x:x%2==1)
# This is slighly worse because (on average)
# it discards half of the generated values 

# 
# Test an arithmetic property:
# summing two odd integers yield an even integer
#
@given(odds, odds)
def test_add_odds(x,y):
    assert (x+y)%2 == 0


# We can use Hypothesisto search for solutions of an equation:
# find odd numbers x, y such that x+y is greater than 4 and a multiple of 4
@given(odds, odds)
def test_solve_ineq(x, y):
    assert not (x+y>4 and (x+y)%4 == 0)
    

# A list reversal function;
# this is just a wrapper over the built-in reversed() function
# (as of Python 3.12.x, reversed returns an interator)
def reverse(lst):
    return list(reversed(lst))
    
#
# 3) Let us write some properties about reverse
#

# First, a strategy for generating random lists of integers
intlist = st.lists(st.integers())

# 1) Reverse is its own inverse function:
@given(intlist)
def test_reverse_twice(x):
    assert reverse(reverse(x)) == x

    
# 2) Reverse distributes over append
# note that the order of the lists changes!
@given(intlist, intlist)
def test_reverse_append(x, y):
    assert reverse(x + y) == reverse(x) + reverse(y)

    
