import importlib 
import time 
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
        self.should_break = False 

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

    ret.test = testcase

    args, args_str = create_args_array(ret.test)

    import traceback 
    with Capturing() as ret.std_out: 
        try: 
            ret.expected = user_method(*args)
        except Exception as error: 
            print("Line 129 Traceback Error:")
            print(traceback.format_exc())
            ret.error = str(error)
            ret.result = "Runtime Error"
            ret.should_break = True  
    
    ret.actual = sol_method( *args)

    if  ret.expected == ret.actual: 
        ret.correct += 1 
    else: 
        ret.failed_test = "\n".join(args_str)
        ret.result = "Wrong Answer"
        ret.should_break = True 

    ret.total += 1 


def test_file(q, file, testcase=None): 
    # https://stackoverflow.com/questions/8718885/import-module-from-string-variable
    # import importlib
    # i = importlib.import_module("matplotlib.text")
    # package = question + ".user_file"

    ret = info(q, testcase) #JSON that will be returned to the user 

    ###################################################################
    # STEP 1: Get Code for User and Solution File and Ensure that there are no errors 
    ###################################################################
    user, err = check_syntax(q + "." + file)

    if err:
        ret.error = err
        ret.result = "Compile Error"
        return ret

    sol = importlib.import_module(q + ".solution") 

    ###################################################################
    # STEP 2: Get User Methods 
    ###################################################################
    user_class = getattr(user, "Solution" )
    sol_class = getattr(sol, "Solution" )

    user_method = getattr(user_class(), q)
    sol_method = getattr(sol_class(), q)
    # num_args = user_method.func_code.co_varnames


    ###################################################################
    # STEP 3: Run the testcase(s) 
    ###################################################################
    if testcase: # Run just 1 testcase if the user clicked `Run Code` 
        if "\n" in testcase: 
            testcase = testcase.replace("\n", ";")
        ret.start_timer()
        execute_testcase(ret, testcase, user_method, sol_method)
        ret.cleanup()
        return ret 

    
    # Run all of the testcases if the user clicked `Submit Code`
    ret.start_timer()
    with open("{0}/cases.txt".format(q)) as f: 
        lines = f.readlines()

        for line in lines:
            testcase = line.replace("\n","").strip()

            execute_testcase(ret, testcase, user_method, sol_method)
            
            if ret.should_break: # If there has been an error stop executing any subsequent testcases 
                break 


    ###################################################################
    # STEP 4: Do post processing of data and return to user 
    ###################################################################
    ret.cleanup() # Do post processing of user data 

    return ret