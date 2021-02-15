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
    def __init__(self, question, testcase, filename):
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
        self.filename = filename 

    def start_timer(self):
        self.time_started = time.time()

    def set_time(self): 
        self.time_ended = time.time() 
        time_elasped = time.time() - self.time_started  
        self.time = round(1 + 1000*time_elasped, 0)

    def change_error(self):        
        if not self.std_out: 
            if self.error and self.filename in self.error:
                self.error = self.error.replace(self.filename, "Solution")
            return 

        std_out = (self.std_out).split("\n")
        include_line = False 
        error_arr  = [] 

        for line in std_out: 
            if self.filename in line or include_line and line != "":
                line = re.sub('".*.py"', 'Solution.py', line)
                if self.filename in line: 
                    line = line.replace(self.filename, 'Solution.py')

                include_line = True  
                error_arr.append(line)

        self.error = "\n".join(error_arr[::-1])

    def cleanup(self): 
        self.set_time() 
        self.actual, self.expected = str(self.actual), str(self.expected)

        if self.test and ";" in self.test: 
            self.test = self.test.replace(";", "\n")

        if self.correct == self.total:
            self.result = "Approved"

        if self.std_out: 
            self.std_out = "\n".join(self.std_out)

        self.change_error()




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




import multiprocessing

from multiprocessing import Process, Manager




def closure(func, mem, ret, args): 
    res = func(*args)
    mem[ret.filename] = res


def run_user_function(function, ret, args):
    timeout = 5
    manager = Manager()
    mem = manager.dict()
    p = multiprocessing.Process(target=closure, args=(function, mem, ret, args))
    p.start()
    p.join(timeout)
    if p.is_alive():
        # stop the downloading 'thread'
        p.terminate()
        ret.result = "Time Limit Exceeded"
        ret.error = "Time Limit Exceeded"
        ret.should_break = True         
        # and then do any post-error processing here

    return mem[ret.filename]



    

def execute_testcase(ret, testcase, user_method, sol_method): 
    ret.test = testcase

    args, args_str = create_args_array(ret.test)

    import traceback 
    with Capturing() as ret.std_out: 
        try: 
            ret.expected = user_method(*args) #works but not for TLE Exception
            # ret.expected = run_user_function(user_method, ret, args) #Will not work on a Windows mahcine but works for TLE exception

        except Exception as error: 
            print("Line 129 Traceback Error:")
            print(traceback.format_exc())
            ret.error = str(error)
            ret.result = "Runtime Error"
            ret.should_break = True  
    
    ret.actual = sol_method( *args)

    if  ret.expected == ret.actual: 
        ret.correct += 1 
    elif ret.result: 
        ret.failed_test = "\n".join(args_str)
        ret.should_break = True 
    else: 
        ret.result = "Wrong Answer"
        ret.should_break = True 

    ret.total += 1 



def test_file(q, file, testcase=None): 
    # https://stackoverflow.com/questions/8718885/import-module-from-string-variable
    # import importlib
    # i = importlib.import_module("matplotlib.text")
    # package = question + ".user_file"

    ret = info(q, testcase, file) #JSON that will be returned to the user 

    ###################################################################
    # STEP 1: Get Code for User and Solution File and Ensure that there are no errors 
    ###################################################################
    user, err = check_syntax(q + "." + file)

    if err:
        ret.time_started = time.time()
        ret.error = err
        ret.result = "Compile Error"
        ret.total += 1
        ret.testcase = testcase
        ret.cleanup()
        return ret

    sol = importlib.import_module(q + ".solution") 

    ###################################################################
    # STEP 2: Get User Methods 
    ###################################################################
    user_class = getattr(user, "Solution" )
    sol_class = getattr(sol, "Solution" )

    try: 
        user_method = getattr(user_class(), q)
    except: 
        ret.result = "Name Error"
        ret.error = "Name Error: method has no attribute ", q
        return ret

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