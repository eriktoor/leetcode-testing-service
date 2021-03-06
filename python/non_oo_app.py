#Using More Routes
# from flask import request
# from flask import jsonify

"""

http://127.0.0.1:5000/test?q=add_nums&data=def%20add_nums(a,b):%20\n\tprint(%22hello%22)\n\treturn%20a%20PLUS%20b

http://127.0.0.1:5000/test?q=add_nums&data=def%20hello_world():%20\n\tprint(%22hello%20world%22)
"""


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
    def __init__(self):
        self.question = None 
        self.error = None 
        self.correct = None 
        self.total = None 
        self.time = None 
        self.failed_test = None 
        self.std_out = None 
        self.expected = None 
        self.actual = None 
        self.test = None 

def test_file(q, file, testcase=None): 
    # https://stackoverflow.com/questions/8718885/import-module-from-string-variable
    # import importlib

    # i = importlib.import_module("matplotlib.text")
    # package = question + ".user_file"

    ret = info()
    ret.question = q

    ts = time.time()

    user, err = check_syntax(q + "." + file)
    ret.test = testcase

    if err:
        ret.error = err
        # print(ret.__dict__)
        return ret

    sol = importlib.import_module(q + ".solution") 

    user_method = getattr(user, q)
    sol_method = getattr(sol, q)


    print(user_method)

    correct = 0

    if testcase: 
        line = testcase.replace("\n","").strip()
        args_str = line.split(" ")
        args = [int(i) for i in args_str]


        import traceback 
        with Capturing() as ret.std_out: 
            try: 
                ret.expected = user_method(*args)
            except Exception as error: 
                print(traceback.format_exc())
                ret.error = str(error)
        
        ret.actual = sol_method(*args)
        ret.test = line

        if  ret.expected == ret.actual: 
            correct += 1 
        else: 
            ret.failed_test = " ".join(args_str)

        ret.correct = correct 
        ret.total = 1
        ret.time = time.time() - ts


        return ret 


    with open("{0}/cases.txt".format(q)) as f: 
        lines = f.readlines()
        num = len(lines)
        for line in lines:

            # num_args = user_method.func_code.co_varnames

            line = line.replace("\n","").strip()
            args_str = line.split(" ")
            args = [int(i) for i in args_str]


            import traceback 
            with Capturing() as ret.std_out: 
                try: 
                    ret.expected = user_method(*args)
                except Exception as error: 
                    print(traceback.format_exc())
                    ret.error = str(error)
            
            ret.actual = sol_method(*args)
            ret.test = line

            if  ret.expected == ret.actual: 
                correct += 1 
            else: 
                ret.failed_test = " ".join(args_str)
                break
        
    
    ret.correct = correct 
    ret.total = num
    ret.time = time.time() - ts


    print(ret.__dict__)

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
    info = test_file(question, filename, testcase)    
    print("Took ", time.time() - s, "seconds ")


    from os import listdir 

    for val in listdir("{0}/__pycache__".format(question)): 
        os.remove("{0}/__pycache__/{1}".format(question, val))
    os.remove("{0}/{1}.py".format(question, filename))


    return json.dumps(info.__dict__)




@app.route("/api/submit")
def submit():
    s = time.time() 
    ###################################################################
    # STEP 1: Get Query Parameter Data
    ###################################################################
    data, question = request.args.get('data'), request.args.get('q')
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
    info = test_file(question, filename)    
    print("Took ", time.time() - s, "seconds ")


    from os import listdir 

    for val in listdir("{0}/__pycache__".format(question)): 
        os.remove("{0}/__pycache__/{1}".format(question, val))
    os.remove("{0}/{1}.py".format(question, filename))


    return json.dumps(info.__dict__)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # test_file("add_nums")
