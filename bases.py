import math
unicode=""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
normal = '''0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ '''
bas64 = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/!"#$%&'()*,-.:;<=>?@[\\]^_`{|}~ '''

def sys_change(sys_in, sys_out, num):
    lookup = {"normal": normal, "alpha": bas64, "unicode":unicode}
    num = str(num)
    out = ""
    for x in num:
        ind = lookup[sys_in].index(x)
        out += lookup[sys_out][ind]
    return out
    
def base_change(num, ende, base, sys_in, sys_out): #Accepts unicode system and converts to and from base 10
        if ende == 1:
            num = sys_change(sys_in, "normal", num)
            num = int(num)
            output = ""
            complete = False
            steps = 0
            while complete == False:
                steps += 1
                if num < base**steps:
                    complete = True

            for count in range(steps):
                place_val = steps - count #Digit we are dealing with, i.e in base 10, tens digit would have place_val = 2
                digit =  math.floor(num / base**(place_val-1)) #Value of digit
                output += chr(digit + 32)
                num -= digit* base**(place_val-1)
            output = sys_change("unicode", sys_out, output)

        else:   
            num = sys_change(sys_in, "unicode", num)
            length = len(num) -1
            output = 0
            for x in num:
                val = ord(x) - 32
                output += (base**length)*val
                length -= 1
            output = sys_change("normal", sys_out, output)
        return output