import os
from combo_conv import alphaone
def new_int(min_val, max_val):
    range_size = max_val - min_val + 1
    num_bytes = (range_size.bit_length() + 7) // 8

    while True:
        # Generate random bytes
        random_bytes = os.urandom(num_bytes)
        random_int = int.from_bytes(random_bytes, 'big')
        
        if random_int < range_size:    # Ensure the random integer falls within the desired range
            return min_val + random_int
        
def key_gen(cipher):
    if cipher == 'csar':
        output = str(new_int(1,27))
    elif cipher == 'sub':
        output = str(new_int(100,999999))
    elif cipher == 'morse':
        output = '_'
    elif cipher == 'byoc':
        blacklist=[]
        output_ = ['']*27
        
        for x in alphaone.keys():
            clear = False

            while clear == False:
                ind = new_int(1,27)
                if ind in blacklist:
                    pass
                else:
                    blacklist.append(ind)
                    clear = True
                    output_[ind-1] = x

        output = ""
        for x in output_:
            output += x
    
    elif cipher == "vig":
        length = new_int(15,75)
        output =""
        for x in range(length):
            ind = new_int(1,27)
            char = [i for i in alphaone if alphaone[i] == ind][0]
            output += char
    
    elif cipher == "scrambler" or cipher == "aes":

        if cipher == "scrambler":
            length = new_int(15,75)
        else:
            length = 16

        output =""
        for x in range(length):
            ind = new_int(32,126)
            char = chr(ind)
            output += char        
    
    elif cipher == "base":
        systems = "anu"
        base_out = new_int(2,94)
        sys_in = new_int(0,2)
        sys_out = new_int(0,2)
        output = f"{base_out} {systems[sys_in]} {systems[sys_out]}"
    return output