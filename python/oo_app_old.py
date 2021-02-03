#Using More Routes
# from flask import request
# from flask import jsonify

"""

http://127.0.0.1:5000/test?q=add_nums&data=def%20add_nums(a,b):%20\n\tprint(%22hello%22)\n\treturn%20a%20PLUS%20b

http://127.0.0.1:5000/test?q=add_nums&data=def%20hello_world():%20\n\tprint(%22hello%20world%22)
"""
DELIMETER = ";"

from flask import Flask, request, jsonify 
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

import json
import time 
import os
import importlib 

from build_file import build_file

def check_syntax(q): 

    error = None 

    try: 
        user = importlib.import_module(q) 
        error = None 
    except SyntaxError as err:
        user = None 
        error = "Syntax error: \n{0}".format(err)

    return user, error


from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class info():
    def __init__(self, question, testcase):
        self.question = question 
        self.error = None 
        self.correct = 0 
        self.total = 0 
        self.time = None 
        self.failed_test = None 
        self.std_out = None 
        self.expected = None 
        self.actual = None 
        self.test = testcase 
        self.result = None 
        self.time_started = None
        self.time_ended = None 

    def start_timer(self):
        self.time_started = time.time()

    def set_time(self): 
        self.time_ended = time.time() 
        time_elasped = self.time_ended - self.time_started  
        self.time = round(1000*time_elasped, 2)

    def cleanup(self): 
        self.set_time() 
        self.actual, self.expected = str(self.actual), str(self.expected)

        if self.test and ";" in self.test: 
            self.test = self.test.replace(";", "\n")

        if self.correct == self.total:
            self.result = "Approved"




import re 
def create_args_array(line, DELIMETER=";"): 
    args_str = line.split(DELIMETER)

    args = [] 

    for arg in args_str: 
        arg = arg.strip() 
        if "[" in arg: 
            args.append(eval(arg))
        elif "(" in arg: 
            args.append(eval(arg))
        elif re.findall('\d', arg): 
            args.append(eval(arg))
        elif not arg: 
            continue
        else: 
            args.append(arg)

    return args, args_str





def execute_testcase(ret, testcase, user_method, sol_method): 

    if "\n" in testcase: 
        testcase = testcase.replace("\n", ";")

    args, args_str = create_args_array(testcase)

    import traceback 
    with Capturing() as ret.std_out: 
        try: 
            ret.expected = user_method( *args)
        except Exception as error: 
            print(traceback.format_exc())
            ret.error = str(error)
    
    ret.actual = sol_method(*args)
    ret.test = testcase

    if  ret.expected == ret.actual: 
        ret.correct += 1 
    else: 
        ret.failed_test = "\n".join(args_str)

    ret.total = 1


def test_file(q, file, testcase=None): 
    # https://stackoverflow.com/questions/8718885/import-module-from-string-variable
    # import importlib
    # i = importlib.import_module("matplotlib.text")
    # package = question + ".user_file"

    ret = info(q, testcase)
    user, err = check_syntax(q + "." + file)

    if err:
        ret.error = err
        ret.result = "Compile Error"
        return ret

    sol = importlib.import_module(q + ".solution") 

    user_class = getattr(user, "Solution" )
    sol_class = getattr(sol, "Solution" )

    user_method = getattr(user_class(), q)
    sol_method = getattr(sol_class(), q)

    if testcase: 
        ret.start_timer()
        execute_testcase(ret, testcase, user_method, sol_method)
        ret.cleanup()
        return ret 
    else: 
        ret.start_timer()
    
    with open("{0}/cases.txt".format(q)) as f: 
        lines = f.readlines()
        num = len(lines)
        for line in lines:

            # num_args = user_method.func_code.co_varnames
            original_line = line 
            line = line.replace("\n","").strip()

            args, args_str = create_args_array(line)

            import traceback 
            with Capturing() as ret.std_out: 
                try: 
                    ret.expected = user_method(*args)
                except Exception as error: 
                    print(traceback.format_exc())
                    ret.error = str(error)
                    ret.result = "Runtime Error"
                    break 
            
            ret.actual = sol_method( *args)
            ret.test = original_line

            if  ret.expected == ret.actual: 
                ret.correct += 1 
            else: 
                ret.failed_test = "\n".join(args_str)
                ret.result = "Wrong Answer"
                break


    print(ret.__dict__)
    print("-----------------------------------")



    ret.cleanup()
    return ret


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/run")
def run_code():
    s = time.time() 
    ###################################################################
    # STEP 1: Get Query Parameter Data
    ###################################################################
    data, question, testcase = request.args.get('data'), request.args.get('q'),request.args.get('testcase')
    print(data)

    ###################################################################
    # STEP 2: Build File from Query Parameter Data 
    ###################################################################

    import random 
    filename =  "user_file-"+ str(int(time.time())) + "-"  + str(random.randrange(1,100))
    build_file("{0}/{1}.py".format(question, filename), data)
    ###################################################################
    # STEP 3: Get API Output and Return it to User
    ###################################################################
    # try: 
    #     info = test_file(question, filename, testcase)    
    #     print("Took ", time.time() - s, "seconds ")
    # except: 
    #     print("An error has  occured, probably put line 234 out of try to see stack trace")
    print("IN RUN CODE")
    print(testcase)
    info = test_file(question, filename, testcase)    
    print("Took ", time.time() - s, "seconds ")

    ###################################################################
    # STEP 4: Delete Created Files
    ###################################################################
    cleanup(question, filename)


    return json.dumps(info.__dict__)


def cleanup(question, filename): 
    from os import listdir 

    for val in listdir("{0}/__pycache__".format(question)): 
        os.remove("{0}/__pycache__/{1}".format(question, val))
    os.remove("{0}/{1}.py".format(question, filename))

@app.route("/api/submit")
def submit():
    s = time.time() 
    ###################################################################
    # STEP 1: Get Query Parameter Data
    ###################################################################
    data, question = request.args.get('data'), request.args.get('q')

    ###################################################################
    # STEP 2: Build File from Query Parameter Data 
    ###################################################################

    import random 
    filename =  "user_file-"+ str(int(time.time())) + "-"  + str(random.randrange(1,100))
    build_file("{0}/{1}.py".format(question, filename), data)
    ###################################################################
    # STEP 3: Get API Output and Return it to User
    ###################################################################
    # try: 
    #     info = test_file(question, filename)    
    #     print("Took ", time.time() - s, "seconds ")
    # except: 
    #     print("An error has  occured, probably put line 272 out of try to see stack trace")
    info = test_file(question, filename)    
    print("Took ", time.time() - s, "seconds ")

    ###################################################################
    # STEP 4: Delete Created Files
    ###################################################################
    cleanup(question, filename)


    return json.dumps(info.__dict__)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # test_file("add_nums")
