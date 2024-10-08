#
# Run-length encoding by ChatGPT
#

def rle_encode(data):
    """
    Encode the input string using Run-Length Encoding (RLE).
    
    Parameters:
    data (str): The input string to be encoded.
    
    Returns:
    str: The run-length encoded string.
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
            encoding.append(f"{prev_char}{count}")
            prev_char = char
            count = 1
    # Add the last group
    encoding.append(f"{prev_char}{count}")
    
    return ''.join(encoding)


def rle_decode(encoded_data):
    """
    Decode the Run-Length Encoded (RLE) string back to the original string.
    
    Parameters:
    encoded_data (str): The run-length encoded string.
    
    Returns:
    str: The decoded string.
    """
    decoded = []
    char_list = list(encoded_data)

    i = 0
    while i < len(char_list):
        char = char_list[i]
        count = ""
        i += 1

        # Collect numeric digits for the count
        while i < len(char_list) and char_list[i].isdigit():
            count += char_list[i]
            i += 1
        
        decoded.append(char * int(count))
    
    return ''.join(decoded)

# -----------------------------------------------------------------
# manual tests
# ---------------------------------------------------------------
def test_string(s):
    assert rle_decode(rle_encode(s)) == s

def run_tests():
    test_string("")
    test_string("abc")
    test_string("aaabbccc")
    test_string("aaabbbcccaaa")

if __name__ == "__main__":
    run_tests()
