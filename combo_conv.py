import math
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
            out_str += f"{x}, "
        return ("The possible combinations are:", outputstr[:-2])
        
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
        #Defining variables
        inp=""

        #Key input
        key=password
        key=key.lower()
        keylist = list(map(str, key))

        type=ende

        #Input of plaintext
        inp=input
        inp=inp.lower()
        inp_list = list(map(str, inp))
        return vigenere_converter(inp_list, keylist, type)

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
            letterno= letterno*(seed )
            letterno= letterno- 4
            letterno= 2*letterno+3
            letterno= letterno/2
            letterno= letterno-seed
            letterno= letterno*2

            if letterno<0:
                letterno=letterno*-1
            if letterno%1!=0:
                letterno=letterno+0.5
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
            pword = step[1].split(',')
            text=scrambler(text,ende,pword[1], pword[0])
    return text

def inp_check(text,ende,combo):
    text=text.lower()
    pure="true"
    length=len(combo)-1
    for x in text:
        if ende == '1': 
            if x not in alphaone.keys() and combo[0][0] != "morse":
                pure="Invalid text"
        
        elif ende == '66':
            if x not in alphaone.keys() and combo[length][0] != "morse":
                pure="Invalid text"
            if x not in ('-', '.', '|', ' ') and combo[length][0] =="morse":
                pure="Invalid text"
    
    if ende not in ('1','66'):
        pure="Invalid type(only 1 or 66)"
    
    if isinstance(combo, list) == False:
        pure="Combo type error"
    count=-1
    for x in combo:
        count=count+1
        if x[0] == "morse":
            if count != length:
                pure="Combo invalid, morse code can only be the last step in the combo"

    return pure

def scrambler(text, ende, password, superkey):
    text = text.lower()
    superkey = int(superkey)
    holystr =  "vl40MKPqez_Xuv6HhqazNNR5D1smS2Kownx TSXUHgZx7fXupWmM2667T1aBJqyNhK_MUfJUoT1H35LVBx6_4EldeJccpv4ytTaDx2qCvNN9hxn0TlcopnpXj2vO4l5VO.w5OF .Zn4VVGvQSO JaX mptrs1PNyuEX8aUErAdiVPK.fZ3BNPuNG9P9jE 1e1r3Hnx28w5Nc1tr6bjzW65Oqh3KvLEpJSBWzoyRstBim6Gl4tyZtQIcGl3jCZ9_eMwjRBd75GOxpDRvNyE.O77tufE5rWsysj.VyMxPbMgmfnyj3ReF ACpJ7luHvHWQLSi2M 1bIPYi6YVN1KL6nm X4.FzFLcbVs_jSkNDnVRdMzX6CsnZ3ODsTKxs7xBPvWC8UjYLqhNGP  Gi2bdZmOruYSO.e_Y.p6n3bc7csSrNJYurPc3xefdmfbsH BUmrOIR4r4O5sumy7ZVYq5SELOsCVT4eeQvdIX0zEVkC 14Vd6b  Y2NNhY6NDFS0_Ex JpCCXgH_Zfhn4LLAfCb_3E7dfLtnERNM2vl_D4EoOeRkxvEVccXeQH2rYMXJAuFhsQPC24Weu4ls56Crczu CFfdI3.p12nVf51JxDHq_kJ_8xz0SWNPSXE8twaKUXyw69RAwcYga4Q43_sC OOr._1fxo_39tZUOO7mzaQyWqPg7MJKOa_vYbdXEjvH19p_lxuKzuMjsNBcoIjMDGTKFkBT4vu1BeGsCsc4GactrYfMJQ47abTTk88RcXVzNPlJ9kE5unrONOEsBvk5Lm_pIf2Yv9z9JN95DfIFQZPHEk5v0 shM9AYIHfTv8uJa8kEU3oHCYAJxphWle" 
    val_list=[]
    for x in text:
        val_list.append(alphagreat[x])

    def digitsum(n1):
        n1=str(n1)
        inp_list = list(map(str, n1))
        output=0
        for x in inp_list:
            output = output + int(x)
        return output
        
    def collatz(superkey, char, iteration):  
        val = alphagreat[char]
        if iteration != 0:
            iteration = alphagreat[iteration]

        if superkey > 50: #Defining starting number and which number in collatz graph to take
            start=val* superkey + 2*iteration
        else:
            start = val * superkey * 3/4 + round(2.5 * iteration)
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
    multi_holy = len(text) / len(holystr)
    if multiplier > 1:
        multiplier = math.ceil(multiplier) 
        password = multiplier * password

    if multi_holy > 1:
        multi_holy = math.ceil(multi_holy) 
        password = multi_holy * password
        
    text_list=[]    
    blacklist = {}
    for counter in range(len(text)): #Calls collatz function for each character
        var = collatz (superkey , password[counter], 0)

        while var in text_list: # Enseures there are no duplicates
            if var in blacklist:
                blacklist[var] = blacklist[var] + 1
            else:
                blacklist.update({var : 1})

            var = collatz(superkey , password[counter], holystr[blacklist[var]])
        text_list.append(var)

    if ende == 66: #makes list of list indexes for decryption
        text_num = [] 
        for x in range(len(text)):
            text_num.append(str(x))

        real_text = " " + text
        real_text = real_text[1:]
        text = text_num

    #making a dictionary to assign value to each character
    col_order={}
    for i in range(len(text_list)):
        col_order.update({text_list[i]: i})

    text_list.sort()

    if ende == 66:
        new_order={} #making a dictionary to say which character has which index in the output text
        for count in range(len(text_list)):
            curr_character = count
            curr_val = [i for i in col_order if col_order[i] == curr_character][0]
            ind = text_list.index(curr_val)
            new_order.update({ind: curr_character})

        output= [''] * len(real_text)
        count = -1
        for x in new_order: #Assigns correct values
            output [int(new_order[x])] = real_text[x]

        outstr=""
        for x in output:
            outstr = outstr + x
        return outstr
    
    else:    
        output=""
        for x in text_list:
            output = output + text[col_order[x]]
        return output       
