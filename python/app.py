#Using More Routes

"""
Go to README.md for directions 
"""

from flask import Flask, request 
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


import json
import time 
from utils import build_file, cleanup
from test_file import test_file 


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

    ###################################################################
    # STEP 2: Build File from Query Parameter Data 
    ###################################################################
    import random 
    filename =  "user_file-"+ str(int(time.time())) + "-"  + str(random.randrange(1,100))
    file_dir = "problem/{0}".format(question)
    file_location = "problem/{0}/{1}.py".format(question, filename)

    build_file(file_location, data)

    ###################################################################
    # STEP 3: Get API Output and Return it to User
    ###################################################################
    info = test_file(file_dir, filename, testcase)    
    print("Took ", time.time() - s, "seconds to run do run_code test for question ", question, " and testcase ", testcase.replace("\n", " ") )
    print(info.__dict__)

    ###################################################################
    # STEP 4: Delete Created Files
    ###################################################################
    cleanup(file_dir, filename)


    return json.dumps(info.__dict__)




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
    file_dir = "problem/{0}".format(question)
    file_location = "problem/{0}/{1}.py".format(question, filename)

    build_file(file_location, data)

    ###################################################################
    # STEP 3: Get API Output and Return it to User
    ###################################################################
    info = test_file(file_dir, filename)    
    print("Took ", time.time() - s, "seconds to run do submit_code test for question ", question )
    print(info.__dict__)

    ###################################################################
    # STEP 4: Delete Created Files
    ###################################################################
    cleanup(file_dir, filename)


    return json.dumps(info.__dict__)

if __name__ == "__main__":
    ip4 = "68.173.145.29"
    local = "0.0.0.0"
    app.run(debug=True, host=local)
    # test_file("add_nums")
