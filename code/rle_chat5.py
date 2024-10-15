#
# Run length encoding by ChatGPT, version 5
#

def rle_encode(data):
    """
    Encode the input string using Run-Length Encoding (RLE),
    returning a list of tuples where each tuple is (character, count).
    
    Parameters:
    data (str): The input string to be encoded.
    
    Returns:
    list of tuples: The run-length encoded data, where each tuple contains (character, count).
    """
    if not data:
        return []
    
    encoding = []
    prev_char = data[0]
    count = 1

    for char in data[1:]:
        if char == prev_char:
            count += 1
        else:
            encoding.append((prev_char, count))
            prev_char = char
            count = 1
    # Add the last group
    encoding.append((prev_char, count))
    
    return encoding


def rle_decode(encoded_data):
    """
    Decode the Run-Length Encoded (RLE) data from a list of tuples
    back to the original string.
    
    Parameters:
    encoded_data (list of tuples): The run-length encoded data, where each tuple is (character, count).
    
    Returns:
    str: The decoded string.
    """
    decoded = []

    for char, count in encoded_data:
        decoded.append(char * count)
    
    return ''.join(decoded)

