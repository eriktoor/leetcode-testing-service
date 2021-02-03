
DELIMETER = ";"



from urllib.parse import unquote

def build_file(name, data): 
    """
    @desc create file given text 
    @args
        @arg1 name, the name of a file that will be created 
        @arg2 data, text that needs to go into a file 
    @ret void, will just create a file and close it
    """
    f = open (name, "w")
    data = unquote(data)

    lines = data.split("\\n")

    with f as fl: 
        f.write(data)

    f.close()


import os 

def cleanup(question, filename): 
    """
    @desc delete a file and its pycache given the directory, name 
    @args
        @arg1 question, a string representing the name of a directory 
        @arg2 filename, a string representing the name of a file
    @ret void, will just delete a file
    """
    from os import listdir 

    for val in listdir("{0}/__pycache__".format(question)): 
        os.remove("{0}/__pycache__/{1}".format(question, val))
    os.remove("{0}/{1}.py".format(question, filename))

