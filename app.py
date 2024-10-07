from flask import Flask, render_template, request, redirect, url_for, session
from combo_conv import combination, alphaone
import ast
import sympy
import os
import psycopg2
from keygen import new_int, key_gen

app = Flask(__name__, template_folder='templates')

app.secret_key = 'your_secret_key'  # Needed to use sessions in Flask
DATABASE = "postgresql://nishant:sTOc3DUyEtDRKxAyrC9DHU8uph8DEXwq@dpg-crg2d23qf0us73dfg3v0-a/users_hcyh"
def send_cursor():   
    conn = psycopg2.connect( # Connect to your PostgreSQL database
        dbname="users_hcyh",
        user="nishant",
        password="sTOc3DUyEtDRKxAyrC9DHU8uph8DEXwq",
        host="dpg-crg2d23qf0us73dfg3v0-a",
        port="5432"
    )
    cursor = conn.cursor()
    return cursor, conn

def initialize_db():
    c, conn = send_cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id SERIAL PRIMARY KEY,
                  username VARCHAR(20) UNIQUE NOT NULL,
                  password VARCHAR(50) UNIQUE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS combinations
                 (id SERIAL PRIMARY KEY,
                  username VARCHAR(20) NOT NULL,
                  comboname VARCHAR(20) NOT NULL,
                  combo TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()  
 
def int_check(s):
    try:
        int(s)
    except ValueError:
        return False
    
    if s is float :
        return False
    
    s=int(s)
    if s<0:
        return False
    elif s % 1 == 0:
        return True
    else:
        return False   
    
def in_ascii(char):
    ascii_val = ord(char)

    if 32 <= ascii_val <= 126:
        return True
    else:
        return False
    
def refiner(raw):
    raw=list(raw)
    for count in range(len(raw)):
        raw[count] = raw[count][0]
    return raw
 
def check_combo(ciphername,password):
    errorr=err("", False)
     
    if password == "":
        errorr.raise_issue("Input password in decryption")

    elif ciphername == "csar":
        if int_check(password) == False:
            errorr.raise_issue("Password must be an integer between 1 and 27 or 66 for all possible combinations")
        else:
            password=int(password)
            if password != 66:
                if password > 27 or password < 1:
                    errorr.raise_issue("Password must be an integer between 1 and 27 or 66 for all possible combinations")
    
    elif ciphername == "sub":
        if int_check(password) == False:
            errorr.raise_issue("Password must be a positive integer")
           
    elif ciphername == "vig":
        password = password.lower()
        for x in password:
            if x not in alphaone.keys():
                errorr.raise_issue("Password must contain alphabets or spaces only")

    elif ciphername == "morse":
        pass
    
    elif ciphername == "byoc":
        already_in=[]
        if len(password) != 27:
            errorr.raise_issue("Password must be 27 digits long")
        for x in password:
            if x not in alphaone.keys():
                errorr.raise_issue("Password must be alphabets only")
            if x in already_in:
                errorr.raise_issue("Password can't be repeated")
            else:
                already_in.append(x) 

    elif ciphername == "scrambler":
        if len(password) < 5:
            errorr.raise_issue("Password must atleast be 5 characters long")

        for char in password:
            if not in_ascii(char):
                errorr.raise_issue("Password can only contain lowercase, uppercase alphabets, spacebar, numbers 0-9, underscore")

    elif ciphername == "aes":
        if len(password) != 16:
            errorr.raise_issue("Key must be 16 bytes (128 bits) long.")
    
    else:
        errorr.raise_issue("Cipher doesn't exist")
    return errorr

def read_combo(combo):
    output = ""
    lookup_dict = {"csar":"Caesar", "vig":"Vigenere", "morse":"Morse", "sub":"Substitution", "scrambler":"Scrambler", "byoc":"Build your own cipher", "aes":"AES(128)"}
    count = 0  
    if combo == []:
        return ""
    
    for step in combo:
        count += 1
        output += f"Step {count}; cipher: {lookup_dict[step[0]]}, password: '{step[1]}'\n"
    return output

class err:
    def __init__(self, name, true):
        self.name = name
        self.true = true
    
    def raise_issue(self, name):
        self.true = True
        self.name = name

@app.route('/')
def index():
    initialize_db()
    if 'user' in session:
        curr_user = session['user']
    else:
        session['user'] = None
        curr_user = session['user']
    session['step1'] = True
    print(session['step1'])
    if curr_user != None:
        return redirect(url_for('cipherious'))
    else:
        return redirect(url_for('create_account'))

@app.route('/my_acc', methods=['GET', 'POST'])
def my_acc():
    output={}
    c, conn = send_cursor()
    curr_user=session['user']

    c.execute('SELECT comboname, combo FROM combinations WHERE username = %s', (curr_user,))
    all_combos = c.fetchall()

    for comboname, combo_str in all_combos:
        combo = ast.literal_eval(combo_str) #Converts string from db to list
        out_str = read_combo(combo) 
        out_str = out_str.replace('\n', '<br>')
        output[comboname] = out_str

    conn.close()
    return render_template('my_acc.html', combos=output)

@app.route('/del_combo', methods=['GET', 'POST'])
def del_combo():
    output=""
    c, conn = send_cursor()
    curr_user=session['user']

    if request.method == 'POST':
        req_combo = request.form['combo']
        c.execute('SELECT comboname FROM combinations WHERE username = %s',(curr_user,))
        all_combos=c.fetchall()
        all_combos= refiner(all_combos)

        if req_combo in all_combos:
            c.execute('DELETE FROM combinations WHERE comboname = %s AND username = %s', (req_combo, curr_user))
            conn.commit()
            conn.close()
            output="Deleted the combo: " + req_combo
        else:
            output="Combination not found. Please check your spelling"

    return render_template('del_combo.html', output=output)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    output=""
    if request.method == 'POST':
        c, conn = send_cursor()

        curr_user=session['user']
        old_password= request.form['old_password']
        new_password = request.form['new_password']

        c.execute('SELECT password FROM users WHERE username=%s', (curr_user,))
        corr_password=c.fetchone()[0]
        
        if corr_password == old_password:
            c.execute('UPDATE users SET password = %s WHERE username = %s', (new_password, curr_user))
            output="Your password was changed successfully"
            
        else:
            output="Wrong password"
            return render_template('change_password.html' , output = output)
        
        conn.commit()
        conn.close()
    return render_template('change_password.html', output = output)

@app.route('/del_acc', methods=['GET', 'POST'])
def del_acc():
    output=""
    if request.method=='POST':
        c, conn = send_cursor()
        password = request.form['password']
        curr_user=session['user']
        c.execute('SELECT password FROM users WHERE username = %s', (curr_user,))
        right_pword=c.fetchone()[0]

        if password != right_pword:
            output = "Wrong password"
        else:
            c.execute('DELETE FROM users WHERE username = %s', (curr_user,))
            c.execute('DELETE FROM combinations WHERE username = %s', (curr_user,))
            conn.commit()
            session.clear()
            output = "Account deleted "
            return redirect(url_for('create_account'))
        conn.close()
    return render_template('del_acc.html', output=output)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('create_account'))

@app.route('/cc_func', methods=['GET','POST'])
def cc_func():
    output, password = standard("csar")
    return render_template('Caesar Cipher.html', output = output , password = password)

@app.route('/sub_func', methods=['GET','POST'])
def sub_func():
    output, password = standard("sub")
    return render_template('Pyscript_seed.html', output = output , password = password)

@app.route('/vig_func', methods=['GET','POST'])
def vig_func():
    output, password = standard("vig")
    return render_template('Vig_htmll.html', output = output , password = password)

@app.route('/morse_func', methods=['GET','POST'])
def morse_func():
    output, password = standard("morse")
    return render_template('morse_html.html', output = output)

@app.route('/dif_hel', methods=['GET', 'POST'])
def dif_hel():
    output = ""
    if request.method == 'POST':
        if session['step1']:  # Step 1: Generate superkey
            num = request.form["text"]
            base = request.form["password"]
            priv_key = request.form["ende"]

            if not int_check(priv_key):
                output = "Private key must be a number"
                return render_template('dif_hel1.html', output=output)
            
            priv_key = int(priv_key)

            if num != "" and int_check(num):
                num = int(num)
            if base != "" and int_check(base):
                base = int(base)

            if num == "" and base == "" and 50 < priv_key < 750:  # Generate num and base
                num = new_int(10000000000000000000, 1000000000000000000000000)
                base = sympy.randprime(50, 300)
                superkey = base ** priv_key % num
                output = f"Your superkey is {superkey}, num is {num}, base is {base}. Input your partner's superkey to generate a common final number."
                session['step1'] = False

                # Store the values in session
                session['num'] = num
                session['base'] = base
                session['priv_key'] = priv_key

            elif not int_check(num) or not int_check(base):
                output = "Num and base can be left blank or have an appropriate number, not text. Also, superkey must be between 50 and 750"
            
            elif 10000000000000000000 < num < 1000000000000000000000000 and sympy.isprime(base) and 50 < base < 300 and 50 < priv_key < 750:
                superkey = base ** priv_key % num
                output = f"Your superkey is {superkey}. Input your partner's superkey to generate a common final number."
                session['step1'] = False

                # Store the values in session
                session['num'] = num
                session['base'] = base
                session['priv_key'] = priv_key

            else:
                output = "Your num has to be a 20-24 digit number, your base has to be between 50 and 300 and a prime, your private key needs to be between 50 and 750. One of these is not proper."
            
        else:
            action = request.form['action']
            if action == "step1":
                session['step1'] = True
                return render_template('dif_hel1.html', output="")
            
            o_superkey = request.form['o_superkey']
            if int_check(o_superkey):
                o_superkey = int(o_superkey)
                num = session.get('num')
                priv_key = session.get('priv_key')
                final = o_superkey ** priv_key % num
                output = f"The common number that you and your friend share is {final}."
            else:
                output = "Error: Partner's superkey must be a positive integer."

    if session['step1']:
        return render_template('dif_hel1.html', output=output)
    else:
        return render_template('dif_hel2.html', output=output)
        
@app.route('/BYOCone', methods=['GET', 'POST'])
def BYOCone():
    fin_dict={"a": "","b": "","c": "","d":"","e": "","f": "","g":"","h":"","i":"","j":"","k":"","l":"","m":"","n":"","o":"","p":"","q":"","r":"","s":"","t":"","u":"","v":"","w":"","x":"","y":"","z":"", " ":""}
    problem = err("", False)
    output=''

    if request.method == 'POST':
        for x in alphaone.keys():
            char = request.form[x]

            if char not in alphaone.keys():
                problem.raise_issue(f"Character replacing {x} is invalid")
                fin_dict[x] = char

            elif char in fin_dict.values():
                problem.raise_issue(f"You're trying to replace multiple letters with {char}")

            else:
                fin_dict[x] = char
                output = ''
                for x in fin_dict.values(): 
                    output = output + x
                output = f"Your cipher password is {output}. Go to use your own cipher page, input the password and use it to encrypt and decrypt text"    

    if problem.true:
        return render_template('BYOC-one.html', output = problem.name)
    else:
        return render_template('BYOC-one.html', output = output)
    
@app.route('/BYOCtwo', methods=['GET','POST'])
def BYOCtwo():
    output, password = standard("byoc")
    return render_template('BYOC-2.html', output = output , password = password)

@app.route('/scrambler_func', methods=['GET','POST'])
def scrambler_func():
    output, password = standard("scrambler")
    return render_template('scrambler_html.html', output = output, password = password)

@app.route('/aes_func', methods=['GET', 'POST'])
def aes_func():
    output, password = standard("aes")
    if output == None:
        output = "Input during decryption is always in base64. Your input is wrong"
    return render_template('aes.html', output = output, password = password)

def standard(cipher):
    output=""
    password=""
    if request.method == 'POST':
        text = request.form["text"]
        if cipher != "morse":
            password = request.form["password"]

        if cipher == "csar": #Caesar handling
            if password == "":
                password = key_gen(cipher)

            elif password[0] == "-":
                ende = '66'
                password= password[1:]
            else: 
                ende = '1'

        else:
            ende = request.form['action']

        if password == "" and ende == "1":
            password = key_gen(cipher)

        combin= [[cipher ,  password ]]
        oops = check_combo(cipher, password)
        if oops.true == False:
            ende= int(ende)
            output = combination(text , ende, combin)
        else:
            output = oops.name
            oops.true = False
    return output, password

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    issues=err('',False)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        terms = request.form.get('terms')     
        c, conn = send_cursor()
        
        if terms:
            c.execute("SELECT username FROM users")
            alluser = c.fetchall()

            if not any(username == x[0] for x in alluser) :
                c.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                session['user'] = username
                return redirect(url_for('cipherious'))
            
            else:
                issues.raise_issue("Username already taken")
            conn.close()

        else:
            c.execute("SELECT username FROM users")
            alluser = c.fetchall()

            if any(username == x[0] for x in alluser) :
                c.execute("SELECT password FROM users WHERE username = %s", (username,))
                result=c.fetchone()

                if password==result[0]:
                    session['user'] = username
                    conn.commit()
                    return redirect(url_for('cipherious'))
                else:
                    issues.raise_issue("Wrong password")
            
            else:
                issues.raise_issue("Username not found")
            conn.close()
        
    return render_template('create_account.html',error=issues.name)

@app.route('/cipherious', methods=['GET', 'POST'])
def cipherious():
    curr_user=session['user']
    return render_template('HOME.html',curr_user=curr_user)

@app.route('/create_combo', methods=['GET', 'POST'])
def create_combo():
    if 'combo' not in session:
        restart()

    if request.method == 'POST':
        action = request.form['action']
        session['errorr']['true'] = False

        if action == 'Save name of combination':    
            set_name()
            if not session['errorr']['true']:
                session['errorr']['name'] = f"You have set name to {session['comboname']}"

        elif action == 'Submit this step':
            submit()

        elif action == 'Delete the previous step':
            delete()

        elif action == 'Restart':
            restart()

        elif action == 'Complete combination':
            completed()
            if not session['errorr']['true']:
                restart()
    
    toreturn = session['errorr']['name'] + read_combo(session['combo'])
    return render_template('create_combo.html', steps=toreturn, name = session['comboname'])

def delete():
    if not session['combo']:
        session['errorr']['true'] = True
        session['errorr']['name'] = "Combo is empty"
    else:
        session['combo'].pop()
        combo_text = read_combo(session['combo'])
        session['errorr']['name'] = f"Your combo is {combo_text} "

def restart():
    session['combo'] = []
    session['comboname'] = ""
    session['errorr'] = {"name":"Start a combo by setting your combo name" , "true":False, "nameset":False}

def set_name():
    comboname = request.form['comboname']
    if comboname == "":
        session['errorr']['true'] = False
        session['errorr']['name'] = "Comboname not given"
        return 

    c, conn = send_cursor()
    curr_user = session['user']

    c.execute('SELECT comboname FROM combinations WHERE username = %s', (curr_user,))
    all_names = c.fetchall()

    for name in all_names:
        if comboname == name[0]:
            session['errorr']['name'] = "You used this name already"
            session['errorr']['true'] = True
            return

    session['errorr']['nameset'] = True
    session['comboname'] = comboname

def submit():
    lookup_dict = {'0':"csar", '1':"vig", '2':"sub", '3':"scrambler", '4':"byoc", '5':"morse", '6':"aes"}
    ciphername = request.form['cipherselected']
    password = request.form['password']

    ciphername = lookup_dict[ciphername]
    if not session['errorr']['nameset']:
        session['errorr']['true'] = False
        session['errorr']['name'] = "Comboname not given"
        return 
    
    if password == "":
        password = key_gen(ciphername)
        
    prob = check_combo(ciphername, password)
    session['errorr']['true'] = prob.true
    session['errorr']['name'] = prob.name

    if session['errorr']['nameset'] and not session['errorr']['true']:
        step = [ciphername, password]
        combo = session.get('combo', [])
        combo.append(step)
        session['combo'] = combo

def completed():
    if session['combo'] == "":
        session['errorr']['true'] = True
        session['errorr']['name'] = "Combo is empty"

    for x in session['combo']:
        if x [0] == "morse" and x != session['combo'][-1]:
            session['errorr']['true'] = True
            session['errorr']['name'] = "Morse code must be the last step in the combo"
            return 
        
    c, conn = send_cursor()
    curr_user = session['user']
    combo = str(session['combo'])
    comboname = session.get('comboname', "")
    c.execute('INSERT INTO combinations (username, comboname, combo) VALUES (%s, %s, %s)', (curr_user, comboname, combo))

    conn.commit()
    conn.close()
    session['errorr']['name'] =  "Your combo was saved under the name " + comboname

@app.route('/use_combo', methods=['GET', 'POST'])
def use_combo():
    output=""
    if request.method == 'POST':
        combo_name = request.form['comboname']
        inp = request.form['inptext']
        ende = request.form["action"]
        
        c, conn = send_cursor()
        curr_user=session['user']
        c.execute('SELECT combo FROM combinations WHERE username=%s AND comboname=%s', (curr_user, combo_name))
        combo_ = c.fetchone()

        if combo_ == None:
            output="Error, combination not found"
        else:
            combo_ = combo_[0]
            combo_ = ast.literal_eval(combo_)
            ende = int(ende)
            output = combination(inp, ende, combo_)

        if output == None:
            output = "Input during decryption is always in base64. Your input is wrong"

        conn.close()
    return render_template('use_combo.html',output=output)

if __name__ == "__main__":
    initialize_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(debug = True, host='0.0.0.0', port=port)