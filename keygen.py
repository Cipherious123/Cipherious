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
        return str(new_int(1,27))
    elif cipher == 'sub':
        return str(new_int(100,999999))
    elif cipher == 'morse':
        return '_'
    elif cipher == 'byoc':
        blacklist=[]
        output = ['']*27
        
        for x in alphaone.keys():
            clear = False

            while clear == False:
                ind = new_int(1,27)
                if ind in blacklist:
                    pass
                else:
                    blacklist.append(ind)
                    clear = True
                    output[ind-1] = x

        outstr = ""
        for x in output:
            outstr += x
        return outstr
    
    elif cipher == "vig":
        length = new_int(15,75)
        output =""
        for x in range(length):
            ind = new_int(1,27)
            char = [i for i in alphaone if alphaone[i] == ind][0]
            output += char
        return output
    
    elif cipher == "scrambler":
        length = new_int(15,75)
        output =""
        for x in range(length):
            ind = new_int(1,65)
            char = [i for i in alphagreat if alphagreat[i] == ind][0]
            output += char
        return output