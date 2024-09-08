import os
from combo_conv import alphaone, alphagreat
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
        return new_int(1,27)
    elif cipher == 'sub':
        return new_int(100,999999)
    elif cipher == 'morse':
        return '_'
    elif cipher == 'byoc':
        blacklist=[]
        output = "-"*27
        for x in alphaone.keys():
            clear = False

            while clear == False:
                ind = new_int(1,27)
                if ind in blacklist:
                    pass
                else:
                    ind.append(blacklist)
                    clear = True
                    output[ind] = x
        return output
    
    elif cipher == "vig":
        length = new_int(15,75)
        output =""
        for x in range(length):
            ind = new_int(1,27)
            char = alphaone.keys()[ind]
            output = output + char
        return output
    
    elif cipher == "scrambler":
        length = new_int(20,75)
        superkey = new_int(20,250)
        output =""
        for x in range(length):
            ind = new_int(1,27)
            char = alphagreat.keys()[ind]
            output = output + char
        return superkey, output