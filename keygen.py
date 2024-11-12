import os
def new_int(min_val, max_val):
    range_size = max_val - min_val + 1
    num_bytes = (range_size.bit_length() + 7) // 8

    while True:
        # Generate random bytes
        random_bytes = os.urandom(num_bytes)
        random_int = int.from_bytes(random_bytes, 'big')
        
        if random_int < range_size:    # Ensure the random integer falls within the desired range
            return min_val + random_int
        
def rand_text(length):
    output =""
    for x in range(length):
        ind = new_int(32,126)
        char = chr(ind)
        output += char
    return output

def key_gen(cipher):
    if cipher == 'csar':
        output = str(new_int(1,95))

    elif cipher == 'sub':
        output = str(new_int(100,999999))

    elif cipher == 'morse':
        output = '_'

    elif cipher == 'byoc':
        blacklist=[]
        output = ""
        
        for x in range(95):
            clear = False

            while clear == False:
                char = rand_text(1)
                if char in blacklist:
                    pass
                else:
                    blacklist.append(char)
                    clear = True
                    output += char
    
    elif cipher == "vig" or cipher == "scrambler":
        length = new_int(15,75)
        output = rand_text(length)
    
    elif cipher == "aes":
        output = rand_text(16)
    
    elif cipher == "base":
        systems = "anu"
        base_out = new_int(2,94)
        sys_in = new_int(0,2)
        sys_out = new_int(0,2)
        output = f"{base_out} {systems[sys_in]} {systems[sys_out]}"
    return output