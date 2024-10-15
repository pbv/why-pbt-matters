#
# Run length encoding by ChatGPT, version 3
#

import re

def rle_encode(data):
    """
    Encode the input string using Run-Length Encoding (RLE), wrapping counts in parentheses
    to avoid confusion when input contains digits.
    
    Parameters:
    data (str): The input string to be encoded.
    
    Returns:
    str: The run-length encoded string, where counts are wrapped in parentheses.
    """
    if not data:
        return ""
    
    encoding = []
    prev_char = data[0]
    count = 1

    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            encoding.append(f"{prev_char}({count})")
            prev_char = char
            count = 1
    # Add the last group
    encoding.append(f"{prev_char}({count})")
    
    return ''.join(encoding)


def rle_decode(encoded_data):
    """
    Decode the Run-Length Encoded (RLE) string back to the original string,
    assuming counts are wrapped in parentheses.
    
    Parameters:
    encoded_data (str): The run-length encoded string, where counts are wrapped in parentheses.
    
    Returns:
    str: The decoded string.
    """
    decoded = []
    # Use a regular expression to match a character followed by a count in parentheses
    pattern = re.compile(r'(\D)\((\d+)\)')

    for match in pattern.finditer(encoded_data):
        char, count = match.groups()
        decoded.append(char * int(count))
    
    return ''.join(decoded)



