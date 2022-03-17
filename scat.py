import re
import sys #for removing comments
import os
import random

#=====system_settings============================
types=["wchar_t", "vector<vector<int>>", "vector<int>","unsigned char","signed char","unsigned int","char", "signed int", "short int","unsigned short","signed short","unsigned long long","long long",
       "float","long double","double","bool","void","int32_t","int64_t","long","int","short"]
loop_names=["for","while", "else", "elif", "if", "case"]
open_brackets = "([{"
open_brackets_for_clearing_spaces="(["
closed_brackets = ")]}"
closed_brackets_for_clearing_spaces=")]"
space = " "
other_syntax_symbs=";\n\t,<>+=-:"
syntax_symbs=space+closed_brackets+open_brackets_for_clearing_spaces+other_syntax_symbs
#================================================

#=====settings===================================
#==100% working, cant cause errors:
delete_cout_tie_on=1 #delete cout.tie(0);
remove_comments_on=1 #remove all the comms
delete_empty_lines_on=1 #remove empty lines.                                              || some functions leaves empty lines so it'll be better not to turn off this
random_endl_on=1




#==90% working:
clear_defines_on=1 #clear #DEFINES from the code
replace_libs_to_bitsstd_on=1 #replace all libraries with BITS/STDC++.H
return0_check_on=1 #add return 0; if there aren't "return 0;" in code                     || dont add return 0 if there are strings or functions with "return 0;"
add_fast_input_on=1 #add fast input if there aren't
const_to_define_on=0 #replace const by define                                             || can theoretically cause errors
const_to_code_on=1 #const into code                                                       || can theoretically cause errors
remove_not_used_funcs_on=1 #remove useless vars and funcs from code                       || can theoretically cause errors    
remove_not_used_defines_on=1 # remove_not_used_defines
semicolon_endl_on=1 # ; -> ;\n
comma_to_full_on=1 # long long i,c -> long long i long long c



#==CAN CAUSE ERRORS:
ANTI_1e6_to_1000000_on=1 #replace 1e6 1e7 etc                                             || RECOMMENDED TO AVOID ERRORS with const_to_define and const_to_code functions / can theoretically cause errors
bad_codestyle_on=1 #" {"->" \n{"  , "..; ...;" to "...;\n ...;"                || can theoretically cause errors. recommended if using remove_not_used_funcs. not recommended if there are strings with "...;..." in program.
change_var_names_on=1 #TODO



#==TROLLING:
one_line_program_on=0 # 2-liner from program.                                             || replace all libs to bitsstd
#================================================





#TODO:
#change var names!
#SKAT-UVAGA!
#typedef to define 

#==========COMMENT REMOVER FUNCTIONS
def removeComments(text):
    """ remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
    """
    pattern = r"""
                            ##  --------- COMMENT ---------
           //.*?$           ##  Start of // .... comment
         |                  ##
           /\*              ##  Start of /* ... */ comment
           [^*]*\*+         ##  Non-* followed by 1-or-more *'s
           (                ##
             [^/*][^*]*\*+  ##
           )*               ##  0-or-more things which don't start with /
                            ##    but do end with '*'
           /                ##  End of /* ... */ comment
         |                  ##  -OR-  various things which aren't comments:
           (                ##
                            ##  ------ " ... " STRING ------
             "              ##  Start of " ... " string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^"\\]       ##  Non "\ characters
             )*             ##
             "              ##  End of " ... " string
           |                ##  -OR-
                            ##
                            ##  ------ ' ... ' STRING ------
             '              ##  Start of ' ... ' string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^'\\]       ##  Non '\ characters
             )*             ##
             '              ##  End of ' ... ' string
           |                ##  -OR-
                            ##
                            ##  ------ ANYTHING ELSE -------
             .              ##  Anything other char
             [^/"'\\]*      ##  Chars which doesn't start a comment, string
           )                ##    or escape
    """
    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]

    return "".join(noncomments)

def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)
#==========       


  
#==========CLEAR DEFINES FUNCTIONS
def clear_spaces_after_comma(text):
    return text.replace(", ",",")

def clever_split(line):
    #line=clear_spaces_after_comma(line)
    line=line.split()
    for i in range(3,len(line)):
        line[2]+=" "+line[3]
        line.pop(3)
    return line

def clear_defines(text):
    for line in range(0,len(text.split('\n'))):
        line=text.split('\n')[line]
        if "#define" in line:
            splited_line=clever_split(line)
            if "(" in splited_line[1] and ")" in splited_line[1] and not "()" in splited_line[1]:
                continue
            text=text.replace(line,"")
            for i in range(0,len(syntax_symbs)):
                for j in range(0,len(syntax_symbs)):
                    #if syntax_symbs[i]==" " and syntax_symbs[j]=="(":
                        #print()
                    text=text.replace(syntax_symbs[i]+splited_line[1]+syntax_symbs[j],syntax_symbs[i]+splited_line[2]+syntax_symbs[j])
    return text
#==========       



 
#==========REPLACE LIBS TO BITSSTD FUNCTIONS
def replace_libs_to_bitsstd(text):
    for line in text.split('\n'):
        if "#include" in line:
            text=text.replace("\n"+line,"")
            text=text.replace(line,"") #can be 1st line
    text="#include <bits/stdc++.h>\n"+text
    return text
#==========



  
#==========DELETE EMPTY LINES FUNCTIONS

def delete_empty_lines(text):
        text="".join([s for s in text.strip().splitlines(True) if s.strip()])
        text=text.replace("\n}","\n}\n")
        return text
#==========

#==========ADD RETURN0 IF THERE ARENT
def return0_check(text):
    if not "return 0;" in text and not "return(0);" in text and not "return (0);" in text:
        text=text[:-2]+"    return 0; \n}"
    return text
#========== 

#==========DELETE COUTTIE0 IF THERE ARE
def delete_cout_tie(text):
    text=text.replace("cout.tie(0);","")
    text=text.replace("cout.tie(False);","")
    text=text.replace("cout.tie(false);","")
    return text
#==========

#==========ADD CINTIE
def add_fast_input(text):
    if not "ios::sync_with_stdio" in text and not "cin.tie" in text:
        if "main() {" in text:
            text=text.replace("main() {","main() {\n    ios::sync_with_stdio(0);\n    cin.tie(0);")
    return text
#==========

#==========1-LINER FROM PROGRAM
def delete_multiple_spaces(text):
    return re.sub(' +', ' ',text)

def one_line_program(text):
    text=replace_libs_to_bitsstd(text)
    text=text.replace("\n", " ")
    text=text.replace("#include <bits/stdc++.h>", "#include <bits/stdc++.h>\n")
    text=delete_multiple_spaces(text)
    text=text.replace("\n ","\n")
    return text
#==========

#==========" BAD CODESTYLE AS{"->" \n{" "...; ....;" to "...;\n...;" 1e6=1000000 etc.
def bad_codestyle(text):
    text=text.replace(" {\n", " \n    {\n")
    return text

def ANTI_1e6_to_1000000(text):
    for i in range(1,9):
        for j in range(1,20):
            text=text.replace(str(i)+"e"+str(j),str(i)+"0"*j)
    return text

def dotcomma_endl(text):
    text=text.replace("\n; \n","\n; \n    \n    ")
    text=text.replace("\n;\n","\n; \n    \n    ")
    text=text.replace("    ;\n    ","    ; \n    \n    ")
    return text
#==========

#==========CONST TO DEFINE/CODE
def const_plus_to_space(text):
    list_text=text.split("\n")
    for i in range(1,len(list_text)):
        if len(list_text[i].split())>0:
            if list_text[i].split()[0]=="const":
                list_text[i]=list_text[i].replace(" = "," ")
                list_text[i]=list_text[i].replace(" ="," ")
                list_text[i]=list_text[i].replace("= "," ")
                list_text[i]=list_text[i].replace("="," ")
                list_text[i]=list_text[i].replace(";","")
    text=""
    for i in range(1,len(list_text)):
        text+=list_text[i]+"\n"
    return text



def const_to_define(text):
    for i in types:
        text=text.replace("const "+i,"#define")
    return text
#==========


#==========REMOVE UNUSED VARS AND FUNCS
def remove_not_used_funcs(text):
    for line in text.split('\n'):
        for i in types:
            if i in line:
                line_splited=line.split()
                if len(line_splited)==1:
                    continue
                j=2
                gone=0
                if line_splited[1]==i:
                    gone=1
                elif line_splited[0]==i:
                    j=1
                    gone=1;
                if gone!=1:
                    while j<len(line_splited) and line_splited[j]!=i and line_splited[j-2]+line_splited[j-1]+line_splited[j]!=i and line_splited[j-1]+line_splited[j]!=i:
                        j+=1
                if j!=len(line_splited) and j!=len(line_splited):     
                    if line_splited[j] not in types:
                        line_splited[j]=var_to_clear(line_splited[j])
                        if line_splited[j]!="":
                            text=check_vars_and_funcs(text,line_splited[j],line)  #there are 2 outputs                    
                    else:
                        if j<len(line_splited)-1:
                            if line_splited[j]+line_splited[j+1] in types:
                                j+=1
                        if j<len(line_splited)-2:
                            if line_splited[j]+line_splited[j+1]+line_splited[j+2] in types:
                                j+=1
                        if line_splited[j] not in types:
                            line_splited[j]=var_to_clear(line_splited[j])
                            if line_splited[j]!="":
                                text=check_vars_and_funcs(text,line_splited[j],line)#its 2nd one
    return text


#clearing var before deleting from code
def var_to_clear(var):
    if ("(" in var and ")" in var and not "()" in var ) or "," in var:
        return ""
    else:
        for i in syntax_symbs:
            var=var.replace(i,"")
        var=var.replace(" ","")
    return var


def check_vars_and_funcs(text,var,line_to_replace):
    if text.find(var)==text.rfind(var) and var!="main" and not "main" in line_to_replace:
        text=text.replace(line_to_replace,"")
    elif change_var_names_on:
        text=change_var_names(text,var)
    return text

def change_var_names(text,var):
    #TODO?
    return text
#==========

#==========
def remove_not_used_defines(text):
    #WARNING ''
    for line in text.split("\n"):
        if "#define" in line.lower():
            line_splited=clever_split(line)
            stringg=""
            for i in line_splited[1]:
                if i!="(":
                    stringg+=i
                else:
                    break
            if text.find(stringg)==text.rfind(stringg):
                text=text.replace(line,"")
    return text
#==========


#==========; -> ;\n
def semicolon_endl(text):
    text=text.split("\n")
    for i in range(1,len(text)):
        if not "define" in text[i]:
            text[i]=text[i].replace(";",";\n    ")
    text_l=text
    text=""
    for i in text_l:
        text+=i+"\n"
    return text
#==========

#========== long long i,c -> long long i long long c
def comma_to_full(text):
    text=text.split("\n")
    for i in range(1,len(text)):
        if "," in text[i] and not "(" in text[i] and not "{" in text[i] and not "[" in text[i] and not "<" in text[i]: #kostyl
            for j in types:
                if j in text[i].split()[0]:
                    text[i]=text[i].replace(", ","; \n    "+j+" ")
                    text[i]=text[i].replace(",","; \n    "+j+" ")
    text_l=text
    text=""
    for i in text_l:
        text+=i+"\n"
    return(text)
#==========


#==========
def random_endl(text):
    text=text.split("\n")
    i=0
    while i!=len(text):
        z=random.randint(0,100)
        addd=0
        if z>100 -2:
            addd=3
        elif z>100-2 -5:
            addd=2
        elif z>100-2-5 -23:
            addd=1
        text[i]+="\n    "*addd
        i+=1
    text_l=text
    text=""
    for i in text_l:
        text+=i+"\n"
    return text
#==========


with open("input.txt", "r") as f:
    text=f.read()

    
    text=text.replace("typedef long long ll;","#define ll long long")
    text=text.replace("typedef long double ld;","#define ld long double")
    text=text.replace(" (","(")
    text=text.replace("("," (")
    text=text.replace(", ",",")
    text=text.replace(",",", ")

    
    #experimental part that theoretically can help avoid some errors
    text=text.replace(";\n","; \n")
    

    
    #LEAVE #1
    if remove_comments_on:
        text=commentRemover(text)

    if semicolon_endl_on:
        text=semicolon_endl(text)

    if comma_to_full_on:
        text=comma_to_full(text)

    if ANTI_1e6_to_1000000_on:
       text=ANTI_1e6_to_1000000(text)
    
    if clear_defines_on:
        text=clear_defines(text)
        
    
    if const_to_define_on:
        text=const_plus_to_space(text)
        text=const_to_define(text)

    if remove_not_used_defines_on:
        text=remove_not_used_defines(text)

    if const_to_code_on:
        text=const_plus_to_space(text)
        text=const_to_define(text)
        text=clear_defines(text)
        
    if replace_libs_to_bitsstd_on:
        text=replace_libs_to_bitsstd(text)

    if return0_check_on:
        text=return0_check(text)

    if delete_cout_tie_on:
        text=delete_cout_tie(text)

    if add_fast_input_on:
        text=add_fast_input(text)

    if bad_codestyle_on:
        text=bad_codestyle(text)
        text=dotcomma_endl(text)

    if remove_not_used_funcs_on:
        text=remove_not_used_funcs(text)

    #LEAVE THAT LAST-2
    if one_line_program_on:
        text=one_line_program(text)
        
    #IMPORTANT: LEAVE THAT LAST-1
    if delete_empty_lines_on:
        text=delete_empty_lines(text)
    #IMPORTANT: LEAVE THAT LAST
    if random_endl_on:
        text=random_endl(text)
    
                    
print(text)


