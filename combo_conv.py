import math
import base64 as b64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from bases import base_change, unicode
bas64 = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, 'a': 27, 'b': 28, 'c': 29, 'd': 30, 'e': 31, 'f': 32, 'g': 33, 'h': 34, 'i': 35, 'j': 36, 'k': 37, 'l': 38, 'm': 39, 'n': 40, 'o': 41, 'p': 42, 'q': 43, 'r': 44, 's': 45, 't': 46, 'u': 47, 'v': 48, 'w': 49, 'x': 50, 'y': 51, 'z': 52, '0': 53, '1': 54, '2': 55, '3': 56, '4': 57, '5': 58, '6': 59, '7': 60, '8': 61, '9': 62, '+': 63, '/': 64, '!': 65, '"': 66, '#': 67, '$': 68, '%': 69, '&': 70, "'": 71, '(': 72, ')': 73, '*': 74, ',': 75, '-': 76, '.': 77, ':': 78, ';': 79, '<': 80, '=': 81, '>': 82, '?': 83, '@': 84, '[': 85, '\\': 86, ']': 87, '^': 88, '_': 89, '`': 90, '{': 91, '|': 92, '}': 93, '~': 94, ' ': 95}
alphaone={ "a":1 , "b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26, " ":27 }
alpha={ "a":".-" , "b":"-...","c":"-.-.","d":"-..","e":".","f":"..-.","g":"--.","h":"....","i":"..","j":".---","k":"-.-","l":".-..","m":"--","n":"-.","o":"---","p":".--.","q":"--.-","r":".-.","s":"...","t":"-","u":"..-","v":"...-","w":".--","x":"-..-","y":"-.--","z":"--..",
        "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5":".....", "6":"-...." , "7":"--...", "8": "---..", "9": "----.", "0": "-----"}
capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def julian (shiftno, letter):
    letter=int(letter)
    letter= letter+shiftno
    if letter > 95:
        letter=letter-95
    return letter

def unicheck(inp):
    for x in inp:
        if x not in unicode:
            return False
    return True    
        
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
    def encrypt_caesar(inp, shift):
        if shift<0:
            shift *= -1
            shift = 95 - shift

        output=""   
        for x in inp:
            letter = bas64[x] + shift
            if letter > 95:
                letter=letter-95
            out_char = [i for i in bas64 if bas64[i] == letter][0]

            output += out_char
        return output 

    def decrypt_caesar(inp):
        output = "The possible combinations are:\n"
        for count in range(95):
            word = encrypt_caesar(inp, count+1)
            output += f"{word}\n"
        return output
        
    shift=int(password)
    #Takes user input and runs function on it
    if shift != 666:  
        return encrypt_caesar(input, shift) 

    #All shifts
    else:
        return decrypt_caesar(input)

def morse(inp, ende): 
    def morse_len(char):
        if char == " ":
            return 2
        return len(alpha[char]) + 1
    
    lookup2 = {".": "·", "-": "–", '|': "¦"}
    def filter_morse(inp, ende):
        output_list= []
        morse_en = "abcdefghijklmnopqrstuvwxyz 1234567890"
        morse_de = "- .|"
        filtered = ""
        inp = inp.lower()
        lookup={1:morse_en, 66:morse_de}

        for x in inp:
            if x in lookup[ende]:
                if ende == 1:
                    for _ in range(morse_len(x)):
                        output_list.append("")
                else:
                    if x == "|":
                        output_list.append("")
                filtered += x 

            elif x in lookup2.values() and ende == 66:
                output_list.append(x)

            elif x not in unicode:
                pass

            elif x in morse_de and ende == 1:
                output_list.append(lookup2[x])
        
            else:
                output_list.append(x)
        return filtered, output_list

    def unfilter(inp, input_list, ende):
        output = ""
        count = -1
        for x in input_list:
            count += 1

            if count >= len(inp):
                return output
            elif x == "":
                output += inp[count]
            elif x in lookup2.values():
                if ende == 66:
                    output += [i for i in lookup2 if lookup2[i] == x][0]
                else:
                    output += x
            else:
                count -= 1
                output += x

        if len(input_list) < len(inp): #Adds rest of input to the output if the text has expanded during encryption
            difference = len(inp) - len(input_list)
            output += inp[-difference:]   
        return inp
    
    inp, template = filter_morse(inp, ende)      
    val=""
    if ende == 1 or ende == "1":
        for x in inp:
            if x in alpha.keys():
                char=alpha[x]
            else:
                char=" "
            val = val + char + "|"
    
    else:
        inp = inp.split()
        for x in inp:
            cur_word=x.split("|")

            for y in cur_word:
                if y == "":
                    pass
                else:
                    try:
                        char=[i for i in alpha if alpha[i] == y][0]
                        val += char
                    except (KeyError, ValueError, TypeError, NameError, IndexError):
                        pass

            val=val+ " "
        val=val[:-1]   
    return unfilter(val, template, ende)

def vig(inp, key, ende):
    
    def julian_ulta (shiftno, letter): #Subtracts shift no. instead of adding
        letter -= shiftno
        if letter==0:
            letter= 95
        elif letter<0:
            letter=letter*-1
            letter=95-letter
        return letter

    index=-1
    output=""
    for char in inp:
        index += 1
        if index==len(key):
            index=0

        key_now = key[index]
        key_val = bas64[key_now]

        if ende == 1:
            inp_val = julian(key_val, bas64[char])
        elif ende == 66:
            inp_val = julian_ulta(key_val , bas64[char])

        val=[i for i in bas64 if bas64[i]==inp_val][0]
        output += val      
    return output

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

def byoc(inp, password, ende):
    val=""
    alphatwo = {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': '', 'I': '', 'J': '', 'K': '', 'L': '', 'M': '', 'N': '', 'O': '', 'P': '', 'Q': '', 'R': '', 'S': '', 'T': '', 'U': '', 'V': '', 'W': '', 'X': '', 'Y': '', 'Z': '', 'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': '', 'i': '', 'j': '', 'k': '', 'l': '', 'm': '', 'n': '', 'o': '', 'p': '', 'q': '', 'r': '', 's': '', 't': '', 'u': '', 'v': '', 'w': '', 'x': '', 'y': '', 'z': '', '0': '', '1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': '', '9': '', '+': '', '/': '', '!': '', '"': '', '#': '', '$': '', '%': '', '&': '', "'": '', '(': '', ')': '', '*': '', ',': '', '-': '', '.': '', ':': '', ';': '', '<': '', '=': '', '>': '', '?': '', '@': '', '[': '', '\\': '', ']': '', '^': '', '_': '', '`': '', '{': '', '|': '', '}': '', '~': '', ' ': ''}     
    for count in range(95):
        curr_lett=[i for i in bas64 if bas64[i] == count+1][0]
        curr_code=password[count]
        alphatwo[curr_lett]=curr_code

    for x in inp:
        if ende == 1 or ende == "1":  
            char=alphatwo[x]
        else:
            char=[i for i in alphatwo if alphatwo[i] == x][0]     
        val += char
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
    
    text = filter_list(text)
    for step in combo:
        p_word = step[1]
        cipher = step[0]

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
        
        elif cipher == "base":   
            lookup_ = {"u": "unicode", "a": "alpha", "n": "normal"}
            password = p_word.split()
            text = bases(text, password[0], lookup_[password[1]], lookup_[password[2]], ende)

        else:
            text = lookup[cipher](text, p_word, ende)
    return text

def filter_list(text):
    output = ""
    for x in text:
        if x in unicode:
            output += x
    return output
textoy = "As of Unicode version 16.0, there are 155,063 characters with code points, covering 168 modern and historical scripts, as well as multiple symbol sets. This article includes the 1,062 characters in the Multilingual European Character Set 2 (MES-2) subset| and some additional related characters."
print(morse(".-|...| |---|..-.| |..-|-.|..|-.-.|---|-..|.| |...-|.|.-.|...|..|---|-.| |.----|-....|·-----|, |-|....|.|.-.|.| |.-|.-.|.| |.----|.....|.....|,-----|-....|...--| |-.-.|....|.-|.-.|.-|-.-.|-|.|.-.|...| |.--|..|-|....| |-.-.|---|-..|.| |.--.|---|..|-.|-|...|, |-.-.|---|...-|.|.-.|..|-.|--.| |.----|-....|---..| |--|---|-..|.|.-.|-.| |.-|-.|-..| |....|..|...|-|---|.-.|..|-.-.|.-|.-..| |...|-.-.|.-.|..|.--.|-|...|, |.-|...| |.--|.|.-..|.-..| |.-|...| |--|..-|.-..|-|..|.--.|.-..|.| |...|-.--|--|-...|---|.-..| |...|.|-|...|· |-|....|..|...| |.-|.-.|-|..|-.-.|.-..|.| |..|-.|-.-.|.-..|..-|-..|.|...| |-|....|.| |.----|,-----|-....|..---| |-.-.|....|.-|.-.|.-|-.-.|-|.|.-.|...| |..|-.| |-|....|.| |--|..-|.-..|-|..|.-..|..|-.|--.|..-|.-|.-..| |.|..-|.-.|---|.--.|.|.-|-.| |-.-.|....|.-|.-.|.-|-.-.|-|.|.-.| |...|.|-| |..---| |(--|.|...|–..---|) |...|..-|-...|...|.|-|¦ |.-|-.|-..| |...|---|--|.| |.-|-..|-..|..|-|..|---|-.|.-|.-..| |.-.|.|.-..|.-|-|.|-..| |-.-.|....|.-|.-.|.-|-.-.|-|.|.-.|...|", 66))