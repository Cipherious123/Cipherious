import math

unicode=""
for x in range(94):
    unicode += chr(x+33)
normal = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
for x in unicode:
    if x not in normal:
        normal += x
    if x not in b64:
        b64 += x
        


def sys_change(sys_in, sys_out, num):
    lookup = {"normal": normal, "base64": b64, "unicode":unicode}
    num = str(num)
    
def base_change(num, ende, base): #Accepts unicode system and converts to and from base 10
        if ende == 1:
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

            return output
        else:   
            length = len(num) -1
            base10 = 0
            for x in num:
                val = ord(x) - 32
                base10 += (base**length)*val
                length -= 1
            return base10