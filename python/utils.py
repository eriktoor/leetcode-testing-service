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
    
    with f as fl: 
        f.write(data)

    f.close()


import os 

def cleanup(file_dir, filename): 
    """
    @desc delete a file and its pycache given the directory, name 
    @args
        @arg1 file_dir, a string representing the name of a directory 
        @arg2 filename, a string representing the name of a file
    @ret void, will just delete a file
    """
    from os import listdir 

    for val in listdir("{0}/__pycache__".format(file_dir)): 
        DELETE_PATH = "{0}/__pycache__/{1}".format(file_dir, val) 
        os.remove(DELETE_PATH)
        print("DELETED ", DELETE_PATH)
    FILE_PATH = "{0}/{1}.py".format(file_dir, filename) 
    os.remove(FILE_PATH)
    print("DELETED ", FILE_PATH)


