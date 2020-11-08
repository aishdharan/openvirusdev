
import os
import glob
    
def get_section_globs():
    section_globs = {}

    section_globs["abstract"]  = ("abstract",   '**/sections/**/*abstract*.xml')
    section_globs["abstract1"] = ("abstract1"), '**/sections/**/*abstract*/*.xml'
    section_globs["method"]    = ("method",     '**/sections/**/*method*/*.xml')
    section_globs["all"]       = ("all",        '**/sections/**/*.xml')
    section_globs["figure"]    = ("figure",     '**/sections/**/*figure*.xml')
    section_globs["table"]     = ("table",      '**/sections/**/*table*.xml')
    section_globs["reflist"]   = ("ref-list",    '**/sections/**/*ref-list*/*.xml')

    return section_globs

def extract_files(directory, section_type):
    glob = get_section_globs()[section_type][1]
    return get_globbed_files(directory, glob)
	
def get_globbed_files(directory, file_glob, recurse=True):
    """
    returns a list of files satisfying the file_glob expression
    in the context of dir
    temporarily changes directory and then resets to current dir
    recurses through the directory if recursive = True (default)    
    """
    current_dir = os.getcwd()
    os.chdir(directory)
    files = glob.glob(file_glob, recursive=recurse)
#    print("number of " + file_glob + " files in " + directory + ": " + str(len(files)))
    os.chdir(current_dir)
    return files
	
def get_or_create_section_dirs():
    section_dirs = get_globbed_files(project, '**/sections')
    if (len(section_dirs) == 0):
        cmd = "ami -v -p " + project + " section"
        print("running: "+cmd)
#        ! $cmd
        section_dirs = get_globbed_files(project, '**/sections')
        print("found: " + section_dirs)
        
def get_glob_dict_all():
    return get_glob_dict(get_section_globs())

def get_glob_dict(section_globs):
    
    glob_dict = {}
    for key in section_globs:
        glob = section_globs[key]
        glob_dict[key] = glob
        
    return glob_dict
    
