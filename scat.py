import re
import random

# =====system_settings============================
vowel = "aeiouy"
types = ["#define", "wchar_t", "vector<vector<int>>", "vector<int>", "vector<long long>", "vector<char>",
         "vector<bool>",
         "vector<long>", "unsigned char", "signed char", "unsigned int", "char", "signed int", "short int",
         "unsigned short", "signed short", "unsigned long long", "long long",
         "float", "long double", "double", "bool", "void", "int32_t", "int64_t", "long", "int", "short", "string",
         "struct", "vector<", "set", "pair"]
null_false_zeros = ["Null", "NULL", "False", "0", "null", "false", "FALSE", "fALSE"]
loop_names = ["for", "while", "else", "elif", "if", "case"]
open_brackets = "([{"
open_brackets_for_clearing_spaces = "(["
closed_brackets = ")]}"
closed_brackets_for_clearing_spaces = ")]"
space = " "
other_syntax_symbs = ";\n\t,<>+=-:.*/!%&$#@"
syntax_symbs = space + closed_brackets + open_brackets + other_syntax_symbs
# ================================================

# =====settings===================================
clear_spaces_on = 1  # clear not needed " " and "\n"'s
delete_cout_tie_on = 1  # Delete "cout.tie(0);"
remove_comments_on = 1  # Remove all comments
delete_empty_lines_on = 1  # Remove empty lines. HIGHLY RECOMMENDED coz some functions leaves empty lines.
random_endlines_on = 1  # Add random end lines
clear_defines_on = 1  # clear #DEFINES from the code
replace_libs_to_bitsstd_on = 1  # replace all libraries with BITS/STDC++.H
return0_check_on = 1  # add return 0; if there aren't
add_fast_input_on = 1  # add fast input if there aren't
const_to_define_on = 0  # replace const by define
#   OR
const_to_code_on = 1  # const into code
semicolon_endl_on = 1  # ; -> ;\n
comma_to_full_on = 1  # long long i,c -> long long i long long c
remove_not_used_funcs_on = 1  # remove useless vars and funcs from code
remove_not_used_defines_on = 1  # remove_not_used_defines
ANTI_1e6_to_1000000_on = 1  # replace 1e6 1e7 etc
bad_codestyle_on = 1  # " {"->" \n\{"  , "..; ...;" to "...;\n ...;"
using_to_define_on = 1
# =====CHANGE VAR NAMES SETTINGS:===================
change_var_names_on = 1  # change_var_names on random
generate_only_not_vowels_on = 1  # not generate only vowels
generate_first_letter_uppercase_on = 0  # generate 1st char uppercase
bad_generator_on = 0  # NOT RECOMMENDED. reinsurance when searching for existing variables
random_name_length = [1, 4]
name_exceptions = []

# ==TROLLING:
one_line_program_on = 0  # 2-liner from program


# ================================================


# TODO:
# typedef to define
# proverka na solve()
# norm proverka peremennyh - ?
# upgrade cout.tie(0);!!!!!!
# titov codestyle
# rename defs PEP8
# 2D TROLLING
# CODED CODE
# todo kak inache

# ==========COMMENT REMOVER FUNCTIONS
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
    regex = re.compile(pattern, re.VERBOSE | re.MULTILINE | re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]

    return "".join(noncomments)


def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " "  # note: a space and not an empty string
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)


# ==========


# ==========CLEAR DEFINES FUNCTIONS
def clear_spaces_after_comma(text):
    return text.replace(", ", ",")


def clever_split(line):
    # line=clear_spaces_after_comma(line)
    line = line.replace(" (", "(")
    line = line.split()
    for i in range(3, len(line)):
        line[2] += " " + line[3]
        line.pop(3)
    return line


def clear_defines(text):
    for line in range(0, len(text.split('\n'))):
        line = text.split('\n')[line]
        if "#define" in line:
            splited_line = clever_split(line)
            if "(" in splited_line[1] and ")" in splited_line[1] and "()" not in splited_line[1]:
                continue
            text = text.replace(line, "")
            for i in range(0, len(syntax_symbs)):
                for j in range(0, len(syntax_symbs)):
                    text = text.replace(syntax_symbs[i] + splited_line[1] + syntax_symbs[j],
                                        syntax_symbs[i] + splited_line[2] + syntax_symbs[j])
    return text


# ==========


# ==========REPLACE LIBS TO BITSSTD FUNCTIONS
def replace_libs_to_bitsstd(text):
    for line in text.split('\n'):
        if "#include" in line:
            text = text.replace("\n" + line, "")
            text = text.replace(line, "")  # can be 1st line
    text = "#include <bits/stdc++.h>\n" + text
    return text


# ==========


# ==========DELETE EMPTY LINES FUNCTIONS

def delete_empty_lines(text):
    text = "".join([s for s in text.strip().splitlines(True) if s.strip()])
    text = text.replace("\n}", "\n}\n")
    return text


# ==========

# ==========ADD RETURN0 IF THERE ARENT
def return0_check(text):
    if "return 0;" not in text and "return(0);" not in text and "return (0);" not in text:

        text = text.split("\n")
        for i in range(len(text) - 1, 0, -1):
            if "}" in text[i]:
                text[i] = text[i].replace("}", "    return 0; \n}\n")
                break
        text_l = text
        text = ""
        for i in text_l:
            text += i + "\n"
    return text


# ==========

# ==========DELETE COUTTIE0 IF THERE ARE
def delete_cout_tie(text):
    # TODOfor i in null_false_zeros:
    #    text = text.replace("ios::sync_with_stdio ("+i+");", "ios::sync_with_stdio (0); \n    cin.tie(0);")
    #    text = text.replace("ios::sync_with_stdio("+i+");", "ios::sync_with_stdio (0); \n    cin.tie(0);")
    text = text.replace("cout.tie(0);", "")
    text = text.replace("cout.tie (0);", "")
    text = text.replace("cout.tie(False);", "")
    text = text.replace("cout.tie(false);", "")
    text = text.replace("cout.tie(NULL);", "")
    text = text.replace("cout.tie(null);", "")
    text = text.replace("cout.tie(Null);", "")
    return text


# ==========

# ==========ADD CINTIE
def add_fast_input(text):
    if "ios::sync_with_stdio" not in text and "cin.tie" not in text:
        text = text.replace("main() {", "main() {\n    ios::sync_with_stdio(0);\n    cin.tie(0);")
    elif "ios::sync_with_stdio" in text and "cin.tie" not in text and "cin. tie" not in text:
        for i in null_false_zeros:
            text = text.replace("ios::sync_with_stdio (" + i + ");", "ios::sync_with_stdio (0); \n    cin.tie(0);")
            text = text.replace("ios::sync_with_stdio(" + i + ");", "ios::sync_with_stdio (0); \n    cin.tie(0);")
    return text


# ==========

# ==========1-LINER FROM PROGRAM
def delete_multiple_spaces(text):
    return re.sub(' +', ' ', text)


def one_line_program(text):
    text = text.split("\n")
    text_l = text
    text = ""
    for i in text_l:
        if "#define" in i or "#include" in i:
            text += "\n" + i + "\n"
        else:
            text += i + " "

    text = delete_multiple_spaces(text)
    text = text.replace("\n ", "\n")
    return text


# ==========

# ==========" BAD CODESTYLE AS{"->" \n{" "...; ....;" to "...;\n...;" 1e6=1000000 etc.
def bad_codestyle(text):
    text = text.replace(" {\n", " \n    {\n")
    return text


def ANTI_1e6_to_1000000(text):
    for i in range(9, 0, -1):
        for j in range(20, 0, -1):
            text = text.replace(str(i) + "e" + str(j), str(i) + "0" * j)
    return text


def dotcomma_endl(text):
    text = text.replace("\n; \n", "\n; \n    \n    ")
    text = text.replace("\n;\n", "\n; \n    \n    ")
    text = text.replace("    ;\n    ", "    ; \n    \n    ")
    return text


# ==========

# ==========CONST TO DEFINE/CODE
def const_plus_to_space(text):
    list_text = text.split("\n")
    for i in range(1, len(list_text)):
        if len(list_text[i].split()) > 0:
            if list_text[i].split()[0] == "const":
                list_text[i] = list_text[i].replace(" = ", " ")
                list_text[i] = list_text[i].replace(" =", " ")
                list_text[i] = list_text[i].replace("= ", " ")
                list_text[i] = list_text[i].replace("=", " ")
                list_text[i] = list_text[i].replace(";", "")
    text = ""
    for i in range(0, len(list_text)):
        text += list_text[i] + "\n"
    return text


def const_to_define(text):
    text = text.split("\n")
    for i in range(0, len(text)):
        if len(text[i].split()) > 0:
            if "const" in text[i].split()[0]:
                for j in types:
                    text[i] = text[i].replace("const " + j, "#define")
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


# ==========


# ==========REMOVE UNUSED VARS AND FUNCS AND change_var_names
def remove_not_used_funcs(text):
    # print(text)
    text = text
    text = text.replace("(", " ( ")
    text = text.replace(")", " ) ")
    text = text.replace(",", " , ")
    text = text.replace("&", " & ")
    text = text.replace("\n  ", "\n        ")
    text = text.replace("\n    ", "\n ")  # TODO maybe bug
    text = text.replace("  ", " ")
    for z in range(0, len(text.split('\n'))):
        line = text.split('\n')[z].split()
        for i in range(0, len(line) - 1):
            if not (line[i] in types or "vector<" in line[i]):
                for j in syntax_symbs:
                    line[i] = line[i].replace(j, "")
            if line[i] in types or "vector<" in line[i]:
                if line[i + 1] == "&" or "":
                    i += 1
                if line[i + 1] not in types:
                    flag = 1  # flag 1 can del, flag 0 only rename
                    if line[i + 1][-1] == "(":  # func name
                        # print(line[i+1],"function, del ALLOWED")
                        flag = 1  # function, del ALLOWED
                    elif len(line) > i + 2:
                        if line[i + 2][0] == "(":
                            flag = 1
                    else:
                        if "(" in line:
                            # print(line[i+1],"var, del DENIED")
                            flag = 0  # var, del DENIED
                        else:
                            # print(line[i+1],"var, del ALLOWED")
                            flag = 1  # var, del ALLOWED

                    var = clear_var_name(line[i + 1])
                    if var == "" or var in types:
                        continue
                    text = check_vars_and_funcs(text, var, text.split('\n')[z], flag)
    text = text.replace(" ( ", "(")
    text = text.replace(" ) ", ")")
    text = text.replace(" , ", ",")
    text = text.replace(" & ", "&")

    return text


def clear_var_name(var):
    var_temp = var
    var = ""
    if var_temp[0] in syntax_symbs:
        var_temp = var_temp[:-1]
    for i in var_temp:
        if i not in syntax_symbs:
            var += i
        else:
            break
    return var


def check_vars_and_funcs(text, var, line_to_replace, flag):  # flag 1 can del, flag 0 only rename
    if text.find(var) == text.rfind(var) and var != "main" and not "main" not in line_to_replace and flag == 1:
        if var + "(" in line_to_replace.replace(" ", ""):
            text = delete_function(text, line_to_replace)
        else:
            text = text.replace(line_to_replace, "")
    elif change_var_names_on:
        text = change_var_names(text, var)
    return text


def delete_function(text, line_to_replace):
    text = text.split("\n")
    n = -1
    open_brackets_counter = 0
    for i in range(0, len(text)):
        if line_to_replace in text[i] and n == -1:

            for j in text[i]:
                if j == "{":
                    open_brackets_counter += 1
                elif j == "}":
                    open_brackets_counter -= 1
            n = i
            text[i] = ""
        elif n != -1:
            for j in text[i]:
                if j == "{":
                    open_brackets_counter += 1
                elif j == "}":
                    open_brackets_counter -= 1
            if open_brackets_counter > 0:
                text[i] = ""
            else:
                text[i] = ""
                break

    temp = text
    text = ""
    for i in range(0, len(temp)):
        text += temp[i] + "\n"
    return text


def var_exists(text, var):
    for i in syntax_symbs:
        for j in syntax_symbs:
            if text.find(i + var + j) != -1:
                return 1
            if bad_generator_on:
                if text.find(var) != -1:
                    return 1
    return 0


def generate_random_name(text):
    random_string = ""
    for _ in range(1, random.randint(random_name_length[0], random_name_length[1])):
        random_integer = random.randint(97, 97 + 26 - 1)
        while str(chr(random_integer)) in vowel and not generate_only_not_vowels_on:
            random_integer = random.randint(97, 97 + 26 - 1)  # Considering only upper and lowercase letters
        random_integer = random_integer
        random_string += (chr(random_integer))
    if generate_first_letter_uppercase_on:
        random_string = random_string.title()
    if var_exists(text, random_string) or random_string in name_exceptions:
        return generate_random_name(text)
    else:
        return random_string


def change_var_names(text, var):
    if "main" in var:
        return text
    random_name = generate_random_name(text)
    for i in syntax_symbs:
        for j in syntax_symbs:
            text = text.replace(i + var + j, i + random_name + j)
    return text


# ==========

# ==========
def remove_not_used_defines(text):
    for line in text.split("\n"):
        if "#define" in line.lower():
            line_splited = clever_split(line)
            stringg = ""
            for i in line_splited[1]:
                if i != "(":
                    stringg += i
                else:
                    break
            if text.find(stringg) == text.rfind(stringg):
                text = text.replace(line, "")
    return text


# ==========


# ==========; -> ;\n
def semicolon_endl(text):
    text = text.split("\n")
    for i in range(1, len(text)):
        if "define" not in text[i]:
            text[i] = text[i].replace(";", ";\n    ")
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


# ==========

# ========== long long i,c -> long long i long long c
def comma_to_full(text):
    text = text.split("\n")
    for i in range(1, len(text)):
        if "," in text[i] and "(" not in text[i] and "{" not in text[i] and "[" not in text[i] and "<" not in text[i]:
            for j in types:  # TODO kostyl
                if j in text[i].split()[0]:
                    text[i] = text[i].replace(", ", "; \n    " + j + " ")
                    text[i] = text[i].replace(",", "; \n    " + j + " ")
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return (text)


# ==========

# ==========
def random_endl(text):
    text = text.split("\n")
    i = 0
    while i != len(text):
        rnd = random.randint(0, 100)
        if rnd < 3:
            text[i] += "\n    " * 3
        elif rnd < 9:
            text[i] += "\n    " * 2
        elif rnd < 40:
            text[i] += "\n    "
        i += 1
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


# ==========

# ==========
def text_space_before_bracket(text):
    text = text.split("\n")
    for i in range(0, len(text)):
        if "define" not in text[i]:
            text[i] = text[i].replace(" (", "(")
            text[i] = text[i].replace("(", " (")
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


# ==========

# ==========
def using_to_define(text):
    text = text.split("\n")
    for i in range(0, len(text)):
        if "using" in text[i] and "=" in text[i]:
            text[i] = text[i].replace("using", "#define")
            text[i] = text[i].replace(" = ", " ")
            text[i] = text[i].replace(" =", " ")
            text[i] = text[i].replace("= ", " ")
            text[i] = text[i].replace("=", " ")
            text[i] = text[i].replace(";", " ")

    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


# ==========

# ==========syntax letters numbers
def clear_spaces(text):
    i = 1
    open_bracket_counter = 0
    while i < len(text) - 1:  # -1!

        if text[i] in "\"\'" and open_bracket_counter == 0:
            open_bracket_counter += 1
        elif text[i] in "\"\'" and open_bracket_counter == 1:  # kostyl
            open_bracket_counter -= 1
        elif text[i] == " " and open_bracket_counter == 0:
            if text[i - 1].isalnum():
                if text[i + 1] in syntax_symbs:
                    text = text[:i] + text[i + 1:]
            if text[i - 1] in syntax_symbs:
                if text[i + 1].isalnum() or text[i + 1] in syntax_symbs:
                    j = i
                    while text[j] == " " and j != 0:
                        j -= 1
                    if text[j] not in "\n":
                        text = text[:i] + text[i + 1:]
        elif text[i] == "\n":
            j = i
            while text[j] == " " and j != 0:
                j -= 1
            if text[j] not in "{};>\n":
                text = text[:i] + " " + text[i + 1:]
        i += 1
    return text


# ==========


def get_cleaned_text(text, n):
    # LEAVE #1
    if remove_comments_on:
        text = commentRemover(text)

    if 1:
        # experimental part that theoretically can help avoid some errors
        text = text.replace("typedef long long ll;", "#define ll long long")  # TODO?
        text = text.replace("typedef long double ld;", "#define ld long double")
        text = text.replace(", ", ",")
        text = text.replace(",", ", ")
        text = text.replace("> ", ">")
        text = text.replace(">", "> ")
        text = text.replace("> >", ">>")

    if clear_spaces_on:
        text = clear_spaces(text)

    if semicolon_endl_on:
        text = semicolon_endl(text)

    if using_to_define_on:
        text = using_to_define(text)

    if comma_to_full_on:
        text = comma_to_full(text)

    if ANTI_1e6_to_1000000_on:
        text = ANTI_1e6_to_1000000(text)

    if clear_defines_on:
        text = clear_defines(text)

    if const_to_define_on:
        text = const_plus_to_space(text)
        text = const_to_define(text)

    if remove_not_used_defines_on:
        text = remove_not_used_defines(text)

    if const_to_code_on:
        text = const_plus_to_space(text)
        text = const_to_define(text)
        text = clear_defines(text)

    if replace_libs_to_bitsstd_on:
        text = replace_libs_to_bitsstd(text)
    
    if return0_check_on:
        text = return0_check(text)

    if delete_cout_tie_on:
        text = delete_cout_tie(text)

    if add_fast_input_on:
        text = add_fast_input(text)

    if bad_codestyle_on:
        text = bad_codestyle(text)
        text = dotcomma_endl(text)

    if remove_not_used_funcs_on and n == 0:
        text = remove_not_used_funcs(text)

    # IMPORTANT: LEAVE THAT LAST-2
    if delete_empty_lines_on:
        text = delete_empty_lines(text)

    if clear_spaces_on:
        text = clear_spaces(text)
       
    # IMPORTANT: LEAVE THAT LAST-1
    if random_endlines_on and n == 0:
        text = random_endl(text)
    
        # LEAVE THAT LAST
    if one_line_program_on:
        text = one_line_program(text)
    
    text = text.replace(")", ") ")
    text = text.replace(") )", "))")
    text = text.replace("    ;", "     ;")
    text = text.replace(" ;", ";")
    
    return text


def go_skat(message):
    text = message
    text1 = text
    text = get_cleaned_text(text, 0)
    i = 1
    while text1 != text and i != 100:  # TODO kostyl na vsyakiy sluchay xd
        i += 1
        text1 = text
        text = get_cleaned_text(text, i)  # TODO kak inache??        
    else:
        text = get_cleaned_text(text, 0)
    return text
