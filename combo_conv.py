import math
import base64 as b64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from bases import base_change
alphaone={ "a":1 , "b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26, " ":27 }
alpha={ "a":".-" , "b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--..",
        "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5":".....", "6":"-...." , "7":"--...", "8": "---..", "9": "----.", "0": "-----"}

def julian (shiftno, letter):
    letter=int(letter)
    letter= (letter+shiftno)
    if letter > 27:
        letter=letter-27
    return letter

def uid(no):
        no += 1
        output = no**2 - 7*no
        return  abs(output)
   
def digitsum(n1):
    n1=str(n1)
    inp_list = list(map(str, n1))
    output=0
    for x in inp_list:
        output = output + int(x)
    return output
        
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
        for count in range(26):
            word = encrypt_caesar(inp_list, count+1)
            output_list.append(word)

        outstr = ""
        for x in output_list:
            outstr += f"{x}, "
        return "The possible combinations are:", outstr[:-2]
        
    def caesar():
        shift=int(password)

        #Takes user input and runs function on it
        if shift != 66:  
            inp=input.lower()
            inp_list = list(map(str, inp))
            return(encrypt_caesar(inp_list, shift))

        #All shifts
        elif shift==66:
            shift=0
            inp, _ = filter_list(input, "csar", 1)
            inp_list = list(map(str, inp))
            return decrypt_caesar(inp_list)
    return caesar()

def morse(input, ende):          
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
                    val += char

            val=val+ " "
        val=val[:-1]
        return val

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
            
        return output

    def vigenere(): 
        inp="" 
        key=password.lower()  #Key input
        keylist = list(map(str, key))

        inp=input.lower() #Input of inp
        inp_list = list(map(str, inp))
        return vigenere_converter(inp_list, keylist, ende)
    return vigenere()

def sub(inp, password, ende):
    def farmer (seed):
        letlist=[]
        def farmer_algorithm(ln):
            ln= ln / seed ** math.sin(seed)
            ln= (ln+seed) *2
            ln= ln*seed%1.7655747 
            ln= 2*ln+3 + 100 * math.sin(ln)
            ln= ln/2
            ln= ln-seed
            ln= ln + seed/2 - seed / ln
            ln = abs(round(ln)) 

            if ln==0:
                ln=10
            return ln % 95
        
        for x in range(95):
            seeder = uid(x+1)
            ln = farmer_algorithm(seeder)
            if ln==0:
                ln=10
            char = chr(ln+31)

            count = 0
            while char in letlist:
                count+=1
                ln += 1
                var = uid(ln)
                ln += var + count

                ln %= 95
                if ln==0:
                    ln += 7
                char = chr(ln+31)

                if count > 100000:
                    for x in range(95):
                        if chr(126-x) not in letlist:
                            char = chr(126-x)
        
            count = 0
            letlist.append(char)
        return letlist
  
    seed = int(password)
    alphatwo = farmer(seed)
    output = ""

    for char in inp:  
        if ende==1:
            ind = ord(char) - 32 #Finding Ascii value of character and making it index
            inp2 = alphatwo[ind] #Obtaining replacement character

        elif ende==66:
            ind=alphatwo.index(char) #Finding index
            inp2 = chr(ind + 32) 

        output+=inp2 
    return output

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
            char=alphatwo[x]

        else:
            char=[i for i in alphatwo if alphatwo[i] == x][0]     
        val=val+char
    return val

def scrambler(text, password, ende):
    val_list=[]
    for x in text:
        val_list.append(ord(x))

    superkey = ord(password[0]) + ord(password[1]) - 20
    while superkey < 50: #Extracting superkey from first 5 alphabets
        superkey += ord(password[0])
        
    def collatz(superkey, char, iteration):  
        val = ord(char)

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
    
def aes_decrypt(ende, inp, key): #Checks if input is in b64 for decryption and creates cipher and ciphertext on the way
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
        inp = inp.encode('utf-8')  # text --> bytes
        iv = get_random_bytes(16) # Generate a random 16-byte initialization vector (IV)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Pad the input to be a multiple of 16 bytes
        padded_inp = pad(inp, AES.block_size)

        ciphertext = cipher.encrypt(padded_inp)
        ciphertext = iv + ciphertext
        ciphertext = b64.b64encode(ciphertext).decode('utf-8') #bytes --> b64
        return ciphertext

    else:  # Decryption
        _, ciphertext, cipher = aes_decrypt(66, inp, key)

        padded_inp = cipher.decrypt(ciphertext)
        output = unpad(padded_inp, AES.block_size)
        return output.decode('utf-8') #stringify

def bases(number, base_out, sys_in, sys_out, ende):
    base_out = int(base_out)
    if ende == 1:
        number = base_change(number, 66, 95, sys_in, sys_out)
        number = base_change(number, 1, base_out, sys_out, sys_out)
    else:
        number = base_change(number, 66, base_out, sys_out, sys_out)
        number = base_change(number, 1, 95, sys_out, sys_in)
    return number

def combination(text, ende, combo):
    lookup = {"vig":vig, "morse": morse, "byoc": byoc, "sub":sub, "scrambler":scrambler}
    if ende==66:
        combo.reverse()

    for step in combo:
        p_word = step[1]
        cipher = step[0]
        text, template = filter_list(text, cipher, ende)

        if cipher=="csar":
            if ende==66:
                p_word= "-" + p_word
            text=cc(text, p_word)

        elif cipher == "aes":
            inp_check,_,_ = aes_decrypt(ende, text, p_word.encode())
            
            if inp_check:
                text = aes(text,p_word, ende)
            else:
                return None 
            
        elif cipher == "morse":
            text = morse(text, 1)
        
        elif cipher == "base":   
            lookup_ = {"u": "unicode", "a": "alpha", "n": "normal"}
            password = p_word.split()
            text = bases(text, password[0], lookup_[password[1]], lookup_[password[2]], ende)

        else:
            text = lookup[cipher](text, p_word, ende)
        text = unfilter(text, template)
    return text

def filter_list(inp, cipher, ende): #Creates a list which maps where non-allowed letters should go
    output_list= []
    capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    unicode = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
    morse_en = "abcdefghijklmnopqrstuvwxyz 1234567890"
    morse_de = "- .|"
    if ende == 1:
        lookup = {"csar":alphaone, "sub":unicode, "vig":alphaone, "morse": morse_en, "byoc": alphaone, "aes":unicode, "scrambler":unicode, "base":unicode}
    else:
        lookup = {"csar":alphaone, "sub":unicode, "vig":alphaone, "morse": morse_de, "byoc": alphaone, "aes":unicode, "scrambler":unicode, "base":unicode}
    
    filtered = ""
    def morse_len(char):
        if char == " ":
            return 2
        return len(alpha[char]) + 1

    if cipher == "morse":
        inp = inp.lower()

    for x in inp:
        if x in lookup[cipher]:
            if cipher != "morse":
                output_list.append("")
                filtered += x

            else:
                if ende == 1:
                    for _ in range(morse_len(x)):
                        output_list.append("")
                else:
                    if x == "|":
                       output_list.append("")
                filtered += x 

        elif x in capitals:
            if lookup[cipher] == alphaone or lookup[cipher] == morse_en:
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

        if count >= len(inp):
            return output
        elif x == "":
            output += inp[count]
        elif x =="U":
            output += inp[count].upper()
        else:
            count -= 1
            output += x
            
    if len(input_list) < len(inp): #Adds rest of input to the output if the text has expanded during encryption
        difference = len(inp) - len(input_list)
        output += inp[-difference:]
    return output