import math
import base64 as b64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
alphaone={ "a":1 , "b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26, " ":27 }
alphagreat = {'a': 40, 'b': 24, 'c': 45, 'd': 49, 'e': 7, 'f': 47, 'g': 35, 'h': 5, 'i': 46, 'j': 37, 'k': 22, 'l': 27, 'm': 13, 'n': 10, 'o': 38, 'p': 61, 'q': 39, 
    'r': 6, 's': 65, 't': 48, 'u': 28, 'v': 18, 'w': 16, 'x': 4, 'y': 2, 'z': 8, 'A': 62, 'B': 20, 'C': 19, 'D': 25, 'E': 55, 'F': 36, 'G': 44, 'H': 32, 'I': 11, 'J': 52, 
    'K': 17, 'L': 63, 'M': 41, 'N': 21, 'O': 26, 'P': 60, 'Q': 30, 'R': 12, 'S': 42, 'T': 43, 'U': 23, 'V': 51, 'W': 64, 'X': 31, 'Y': 53, 'Z': 50, '0': 54, '1': 3, '2': 14, 
    '3': 1, '4': 59, '5': 58, '6': 56, '7': 34, '8': 15, '9': 29, '.': 57, '_': 9, ' ': 33}
 
def julian (shiftno, letter):
    letter=int(letter)
    letter= (letter+shiftno)
    if letter > 27:
        letter=letter-27
    return letter

def cc(input, password):
    def encrypt_caesar(inp_list, shift):
        if shift<0:
            shift=shift*-1
            shift=27-shift
        output=""   
        for x in inp_list:
            shifted_val=julian(shift, alphaone[x]) 
            out_char = [i for i in alphaone if alphaone[i] == shifted_val][0]
            output += out_char
        return(output)

    def decrypt_caesar(inp_list):
        output_list = []
        for count in range(25):
            word = encrypt_caesar(inp_list, count+1)
            output_list.append(word)

        outstr = ""
        for x in output_list:
            outstr += f"{x}, "
        return ("The possible combinations are:", outstr[:-2])
        
    def caesar():
        shift=int(password)
        inp=""

        #Takes user input and runs function on it
        if shift != 66:  
            inp=input
            inp=inp.lower()
            inp_list = list(map(str, inp))
            return(encrypt_caesar(inp_list, shift))

        #All shifts
        elif shift==66:
            shift=0
            inp=input
            inp=inp.lower()
            inp_list = list(map(str, inp))
            return(decrypt_caesar(inp_list))
    return caesar()

def morse(input, ende):          
    alpha={ "a":".-" , "b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--..",
        "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5":".....", "6":"-...." , "7":"--...", "8": "---..", "9": "----.", "0": "-----"}
    inp=input
    inp=inp.lower()
    typ=ende
    val=""
    if typ==1:
        inp=list(map(str,inp))
        for x in inp:
            if x in alpha.keys():
                char=alpha[x]
            else:
                char=" "
            val=val+char
            val=val+"|"
        return(val)
    
    else:
        inp=inp.split()
        for x in inp:
            cur_word=x.split("|")

            for y in cur_word:
                if y == "":
                    pass
                else:
                    char=[i for i in alpha if alpha[i] == y][0]
                    val=val+char

            val=val+ " "
        val=val[:-1]
        return(val)

def vig(input, password, ende):
    
    def decoder (shiftno, letter):
        letter= (letter-shiftno)
        if letter==0:
            letter=27
        elif letter<0:
            letter=letter*-1
            letter=27-letter
        return letter

    def vigenere_converter(inp_list, keylist, type):
        index=-1
        output=""
        for x in range(len(inp_list)):
            index=index+1

            if index==len(keylist):
                index=0

            key_now=keylist[index]
            key_val=int(alphaone[key_now])-1
            char=inp_list[x]

            if char in alphaone:
                if type==1:
                    inp_val=julian(key_val, alphaone[char])
                elif type==66:
                    inp_val=decoder(key_val,alphaone[char])
                val=[i for i in alphaone if alphaone[i]==inp_val][0]
                output=output+val
            else:
                return("Error: Only english alphabets and spaces are allowed.")
        return(output)

    def vigenere(): 
        inp="" 
        key=password.lower()  #Key input
        keylist = list(map(str, key))

        inp=input.lower() #Input of inp
        inp_list = list(map(str, inp))
        return vigenere_converter(inp_list, keylist, ende)

    return vigenere()

def sub(input, password, ende):
    def farmer (seed):
        letterno=1
        letlist=[]
        count=0
        for x in range(27):
            count=count+1
            letterno=count
            letterno= (letterno-2)
            letterno= letterno * seed - (letterno + 2) 
            letterno= (letterno+seed) *2
            letterno= letterno*seed 
            letterno= letterno- 4
            letterno= 2*letterno+3
            letterno= letterno/2
            letterno= letterno-seed
            letterno= letterno + seed/2 - seed / letterno

            if letterno<0:
                letterno=letterno*-1
            letterno = round(letterno)
            if letterno > 27:
                letterno=letterno%27
            if letterno==0:
                letterno=letterno+1

            while letterno in letlist:
                letterno=letterno+1
                if letterno > 27:
                    letterno=letterno-27

            letlist.append(letterno)
        return letlist

    def seed_encrypt(alphaone,inp_list,alphatwo, type):
        output=""
        for x in range(len(inp_list)):  
            char=inp_list[x]

            if char in alphaone:
                if type==1:
                    ind_=alphaone[char]-1
                    inp2=alphatwo[ind_]

                elif type==66:
                    inp2=alphatwo.index(alphaone[char])+1
    
                value = [i for i in alphaone if alphaone[i] == inp2][0]
                output=output+ str(value)  

            else:
                return("error")
            
        return(output)

    def seed_main():   
        seed=int(password)
        type=ende
        inp=""

        alphatwo=farmer(seed)
        inp=input
        inp=inp.lower()
        inp_list = list(map(str, inp))
        return seed_encrypt(alphaone,inp_list,alphatwo,type) 

    return seed_main()

def byoc(input, password, ende):
    inp=input.lower()
    cody=password
    typ=int(ende)
    val=""
 
    alphatwo={"a":"","b":"","c":"","d":"","e":"","f": "","g":"","h":"","i":"","j":"","k":"","l":"","m":"","n":"","o":"","p":"","q":"","r":"","s":"","t":"","u":"","v":"","w":"","x":"","y":"","z":""," ": ""}
     
    for count in range(27):
        curr_lett=[i for i in alphaone if alphaone[i] == count+1][0]
        curr_code=cody[count]
        alphatwo[curr_lett]=curr_code

    inp=list(map(str,inp))
    for x in inp:
        if typ==1:  
            if x in alphatwo.keys():
                char=alphatwo[x]
            else:
                return "Error"   

        else:
            if x in alphatwo.values():
                char=[i for i in alphatwo if alphatwo[i] == x][0]
            else:
                return "Error"       
        val=val+char
    return val

def combination(text, ende, combo):
    if ende==66:
        combo.reverse()

    text, template = filter_list(text)
    for step in combo:
        if step[0]=="csar":
            if ende==66:
                step[1]= "-" + step[1]
            text=cc(text, step[1])

        elif step[0]=="sub":
            text=sub(text,step[1], ende)

        elif step [0]=="vig":
            text=vig(text,step[1], ende)

        elif step [0]=="morse":
            text=morse(text, ende)

        elif step[0]=="byoc":
            text=byoc(text,step[1],ende)

        elif step[0]=="scrambler":
            text=scrambler(text,ende,step[1])

        elif step[0] == "aes":
            text = unfilter(text, template)
            inp_check,_,_ = aes_inp(ende, text)
            
            if inp_check:
                text = aes(text,step[1], ende)
                text, template = filter_list(text) 
            else:
                return None
        
        text = unfilter(text, template)
    return text

def scrambler(text, ende, password):
    text = text.lower()
    holystr =  "vl40MKPqez_Xuv6HhqazNNR5D1smS2Kownx TSXUHgZx7fXupWmM2667T1aBJqyNhK_MUfJUoT1H35LVBx6_4EldeJccpv4ytTaDx2qCvNN9hxn0TlcopnpXj2vO4l5VO.w5OF .Zn4VVGvQSO JaX mptrs1PNyuEX8aUErAdiVPK.fZ3BNPuNG9P9jE 1e1r3Hnx28w5Nc1tr6bjzW65Oqh3KvLEpJSBWzoyRstBim6Gl4tyZtQIcGl3jCZ9_eMwjRBd75GOxpDRvNyE.O77tufE5rWsysj.VyMxPbMgmfnyj3ReF ACpJ7luHvHWQLSi2M 1bIPYi6YVN1KL6nm X4.FzFLcbVs_jSkNDnVRdMzX6CsnZ3ODsTKxs7xBPvWC8UjYLqhNGP  Gi2bdZmOruYSO.e_Y.p6n3bc7csSrNJYurPc3xefdmfbsH BUmrOIR4r4O5sumy7ZVYq5SELOsCVT4eeQvdIX0zEVkC 14Vd6b  Y2NNhY6NDFS0_Ex JpCCXgH_Zfhn4LLAfCb_3E7dfLtnERNM2vl_D4EoOeRkxvEVccXeQH2rYMXJAuFhsQPC24Weu4ls56Crczu CFfdI3.p12nVf51JxDHq_kJ_8xz0SWNPSXE8twaKUXyw69RAwcYga4Q43_sC OOr._1fxo_39tZUOO7mzaQyWqPg7MJKOa_vYbdXEjvH19p_lxuKzuMjsNBcoIjMDGTKFkBT4vu1BeGsCsc4GactrYfMJQ47abTTk88RcXVzNPlJ9kE5unrONOEsBvk5Lm_pIf2Yv9z9JN95DfIFQZPHEk5v0 shM9AYIHfTv8uJa8kEU3oHCYAJxphWle" 
    val_list=[]
    for x in text:
        val_list.append(alphagreat[x])

    superkey = alphagreat[password[0]] + alphagreat[password[1]] + alphagreat[password[2]] + alphagreat[password[3]] + alphagreat[password[4]]
    while superkey < 50: #Extracting superkey from first 5 alphabets
        superkey += 2 * alphagreat[password[0]]
    while superkey > 250:
        superkey -= alphagreat[password[2]]
        
    def digitsum(n1):
        n1=str(n1)
        inp_list = list(map(str, n1))
        output=0
        for x in inp_list:
            output = output + int(x)
        return output
        
    def collatz(superkey, char, iteration):  
        val = alphagreat[char]

        if superkey > 50: #Defining starting number and which number in collatz graph to take
            start=val* superkey + 2*iteration
        else:
            start = val * superkey * 3/4 + round(2 * iteration)
            start = round(start)

        number= digitsum(val) + digitsum(superkey) - digitsum(iteration)
        listy=[]
        keep_going = True
        count=0

        while keep_going == True: #collatz
            count=count+1
            if start%2 == 0:
                start = start/2
            else:
                start = 3*start +1
            listy.append(start)

            if start == 1 or count == number:
                keep_going = False

        length=len(listy) #Deals with when the collatz graph falls too sharply and we don't have enough values
        if length == number:
            output = listy[length-1]
        elif length >= round(number/2):        
            output = listy[round(number/2)]
        elif length >= round(number/4):
            output = listy [(number/4)]
        else:
            output = 1000 - val + length
 
        return output

    multiplier = len(text) / len(password) #Defining variables, multiplying password as required
    if multiplier > 1:
        multiplier = math.ceil(multiplier) 
        password *= multiplier 
        
    text_list=[]    
    def uid(no):
        no += 1
        output = no^2 - 7*no
        return  abs(output)
    
    for counter in range(len(text)): #Calls collatz function for each character
        var = collatz (superkey , password[counter], uid(counter))
        new_iter = 3 *uid(counter) +1

        while var in text_list: # Ensures there are no duplicates
            var = collatz (superkey , password[counter], new_iter)
            new_iter = 3*new_iter + 1

        text_list.append(var)

    #making a dictionary to assign value to each character
    col_order={}
    for i in range(len(text_list)):
        col_order.update({text_list[i]: i})

    text_list.sort()

    if ende == 66:
        new_order={} #making a dictionary to say which character has which index in the output text
        for count in range(len(text_list)):
            curr_val = [i for i in col_order if col_order[i] == count][0]
            ind = text_list.index(curr_val)
            new_order.update({ind: count})

        output= [''] * len(text)
        count = -1
        for x in new_order: #Assigns correct values
            output [int(new_order[x])] = text[x]

        outstr=""
        outstr
        for x in output:
            outstr += x
        return outstr
    
    else:    #Substituting values from the sorted text_list using col_order
        output=""
        for x in text_list:
            output = output + text[col_order[x]]
        return output
    
def aes_inp(ende, inp): #Checks if input is in b64 for decryption and creates cipher and ciphertext on the way
    if ende == 66:
        try:
            inp = b64.b64decode(inp) #b64 --> bytes
            iv = inp[:16]
            ciphertext = inp[16:]
            cipher = AES.new(key, AES.MODE_CBC, iv) # Create AES cipher in CBC mode with the key and IV
            return True, ciphertext, cipher

        except (ValueError,KeyError,TypeError):
            return False, None, None
    else:
        return True, None, None
    
def aes(inp, key, ende):
    key = key.encode()  # Ensure key is in bytes

    if ende == 1:  # Encryption
        inp = inp.encode()  # text --> bytes
        iv = get_random_bytes(16) # Generate a random 16-byte initialization vector (IV)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Pad the input to be a multiple of 16 bytes
        padded_inp = pad(inp, AES.block_size)

        ciphertext = cipher.encrypt(padded_inp)
        ciphertext = iv + ciphertext
        ciphertext = b64.b64encode(ciphertext).decode('utf-8') #bytes --> b64
        return ciphertext

    else:  # Decryption
        _, ciphertext, cipher = aes_inp(1, inp)

        padded_inp = cipher.decrypt(ciphertext)
        output = unpad(padded_inp, AES.block_size)
        return output.decode('utf-8') #stringify
        
def encrypt_num(num):
    return num

def filter_list(inp): #Creates a list which maps where non-allowed letters should go
    output_list= []
    capitals = []
    for x in alphaone:
        if x != " ":
            capitals.append(x.upper())

    filtered = ""
    for x in inp:
        if x in alphaone:
            output_list.append("")
            filtered += x
        elif x in capitals:
            output_list.append("U")
            filtered += x.lower()
        else:
            output_list.append(x)   
    return filtered, output_list

def unfilter(inp, input_list):
    output = ""
    count = -1
    for x in input_list:
        count += 1
        if x == "":
            output += inp[count]
        elif x =="U":
            output += inp[count].upper()
        else:
            count -= 1
            output += x
    return output