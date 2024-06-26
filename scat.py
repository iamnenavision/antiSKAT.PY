import re
import random

# =====system_settings============================
types = ["operator", "#define", "uint64_t", "uint32_t", "wchar_t", "vector<vector<int>>", "vector<int>",
         "vector<long long>", "vector<char>",
         "vector<bool>",
         "vector<long>", "unsigned char", "signed char", "unsigned int", "char", "signed int", "short int",
         "unsigned short", "signed short", "unsigned long long", "long long",
         "float", "long double", "double", "bool", "void", "int32_t", "int64_t", "long", "int", "short", "string",
         "struct", "vector<", "set", "pair"]
null_false_zeros = ["Null", "NULL", "False", "0", "null", "false", "FALSE", "nullptr"]
vowel = "aeiouy"
loop_names = ["for", "while", "else", "elif", "if", "case"]
open_brackets = "([{"
open_brackets_for_clearing_spaces = "(["
closed_brackets = ")]}"
closed_brackets_for_clearing_spaces = ")]"
space = " "
other_syntax_symbols = ";\n\t,<>+=-:.*/!%&$#@"
syntax_symbols = space + closed_brackets + open_brackets + other_syntax_symbols
# ================================================

# =====settings===================================
clear_spaces_on = 1  # clear not needed " " and "\n"'s
delete_cout_tie_zero_on = 1
zero_in_fast_input_on = 1  # cout.tie(Null); to cout.tie(0); etc
remove_comments_on = 1
delete_empty_lines_on = 1  # Remove empty lines. HIGHLY RECOMMENDED coz some functions leaves empty lines
random_endlines_on = 1
typedef_to_define_on = 1  # typedef to define
clear_defines_on = 1  # clear #DEFINES from the code
replace_libs_to_bitsstd_on = 1  # replace all libraries to BITS/STDC++.H add using namespace std; remove std::'s
return0_check_on = 1  # add return 0; if there aren't
add_fast_input_on = 1  # add fast input if there aren't
const_to_define_on = 0  # replace const by define
#   OR
const_to_code_on = 1  # const into code
comma_to_full_on = 1  # long long i,c -> long long i long long c
remove_not_used_funcs_on = 1  # remove useless vars and funcs from code
exponent_to_decimal_on = 1  # replace 1e6 to 1000000, 1e7 to 10000000 etc
some_codestyle_changes_on = 1  # " {"->" \n\{"  , "..; ...;" to "...;\n ...;"
using_to_define_on = 1
# =====CHANGE VAR NAMES SETTINGS:===================
change_var_names_on = 1  # change_var_names on random
generate_only_not_vowels_on = 0
generate_first_letter_uppercase_on = 0
random_name_length = [1, 4]
name_exceptions = ["main", "join", "size", "back"]  # will not generate and will not be replaced
# ==TROLLING:
titov_codestyle_on = 0  # not working with one-liner function. add comments after } like "for i {          } //for"
two_line_program_on = 0  # turns program into 2-liner

crazy_two_liner_on = 0  # 2D hide and seek #TODO
# ==OTHER:
debug_on = 0

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
def clever_split(line):
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
            if debug_on:
                print("input define: ", splited_line, line)
            if "(" in splited_line[1] and ")" in splited_line[1] and "()" not in splited_line[1]:
                continue
            text = text.replace(line, "")
            for i in range(0, len(syntax_symbols)):
                for j in range(0, len(syntax_symbols)):
                    text = text.replace(syntax_symbols[i] + splited_line[1] + syntax_symbols[j],
                                        syntax_symbols[i] + splited_line[2] + syntax_symbols[j])
    return text


# ==========


# ==========REPLACE LIBS TO BITSSTD FUNCTIONS
def replace_libs_to_bitsstd(text):
    for line in text.split('\n'):
        if "#include" in line:
            text = text.replace("\n" + line, "")
            text = text.replace(line, "")  # can be 1st line
    text = text.replace("std::", "")
    if "using namespace std;" in clear_spaces(text):
        text = "#include <bits/stdc++.h>\n" + text
    else:
        text = "#include <bits/stdc++.h>\nusing namespace std;\n" + text

    return text


# ==========


# ==========DELETE EMPTY LINES FUNCTIONS

def delete_empty_lines(text):
    text = "".join([s for s in text.strip().splitlines(True) if s.strip()])
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
def delete_cout_tie_zero(text):
    for i in null_false_zeros:
        text = text.replace("cout.tie(" + i + ");", "")

    return text


# ==========

# ==========ADD CINTIE
def add_fast_input(text):
    if "ios::sync_with_stdio" not in text and "cin.tie" not in text:
        text = text.replace("main() {", "main() {\n    ios::sync_with_stdio(0);\n    cin.tie(0);")
    elif "ios::sync_with_stdio" in text and "cin.tie" not in text and "cin. tie" not in text:
        for i in null_false_zeros:
            text = text.replace("ios::sync_with_stdio (" + i + ");", "ios::sync_with_stdio (0); \n    cin.tie(0);")
    return text


# ==========

# ==========1-LINER FROM PROGRAM
def delete_multiple_spaces(text):
    return re.sub(' +', ' ', text)


def two_line_program(text):
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


def crazy_two_liner(text):  # TODO
    #    estimated_string_size=crazy_two_liner_max_text_len-len(text)
    #    crazy_two_liner_tabs_before = random.randint(80,2)
    #    #random_integer=0
    #    if len(text)+text.count("\n")*crazy_two_liner_tabs_before < crazy_two_liner_max_text_len:
    #        text = text.replace("\n", "\n\t" * crazy_two_liner_tabs_before)
    #    #random_integer=random.randint(1,2)
    return text


# ==========

# ==========" BAD CODESTYLE AS{"->" \n{" "...; ....;" to "...;\n...;" 1e6=1000000 etc.
def some_codestyle_changes(text):
    text = text.replace("\n}\n", "\n}\n\n")
    text = text.replace("\n} \n", "\n} \n\n")
    text = text.replace(" {\n", " \n    {\n")
    return text


def exponent_to_decimal(text):
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
# def replace_not_in_define(string_before, string_after):  # not in define and using
#    text = text.split("\n")
#    for i in range(0, len(text)):
#        if "#define" not in text[i] and "using" not in text[i] and "#include" not in text[i]:
#            text[i] = text[i].replace(string_before, string_after)
#    text_l = text
#    text = ""
#    for i in text_l:
#        text += i + "\n"
#    return text


# ==========REMOVE UNUSED VARS AND FUNCS AND change_var_names
def remove_not_used_funcs(text):
    text = text.replace("(", " ( ")
    text = text.replace(")", " ) ")
    text = text.replace(",", " , ")
    text = text.replace("&", " & ")
    text = text.replace("&", " & ")
    text = text.replace("\n  ", "\n        ")
    text = text.replace("\n    ", "\n ")
    text = text.replace("  ", " ")

    for z in range(0, len(text.split('\n'))):
        line = text.split('\n')[z].split()
        for i in range(0, len(line) - 1):
            if not (line[i] in types or "vector<" in line[i]):
                for j in syntax_symbols:
                    line[i] = line[i].replace(j, "")
            if line[i] in types or "vector<" in line[i]:
                if line[i + 1] == "&" or "":
                    i += 1
                if line[i + 1] not in types:
                    flag = 1  # flag 1 can del, flag 0 only rename
                    if line[i + 1][-1] == "(":  # line[i + 1][-1] - func name
                        flag = 1  # function, del ALLOWED
                    elif len(line) > i + 2:
                        if line[i + 2][0] == "(":
                            flag = 1
                    else:
                        if "(" in line:
                            flag = 0  # var, del DENIED
                        else:
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
    if var_temp[0] in syntax_symbols:
        var_temp = var_temp[:-1]
    for i in var_temp:
        if i not in syntax_symbols:
            var += i
        else:
            break
    return var


def check_vars_and_funcs(text, var, line_to_replace, flag):  # flag 1 can del, flag 0 only rename
    if var in name_exceptions:
        return text
    if debug_on:
        print(var, " found in line ", line_to_replace, " . checking before deleting... ")
    if text.find(var) == text.rfind(var) and flag == 1:
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
    for i in syntax_symbols:
        for j in syntax_symbols:
            if text.find(i + var + j) != -1:
                return 1
    return 0


def generate_random_name(text):
    random_string = ""
    for _ in range(1, random.randint(random_name_length[0], random_name_length[1])):
        random_integer = random.randint(97, 97 + 26 - 1)
        while str(chr(random_integer)) in vowel and \
                generate_only_not_vowels_on:
            random_integer = random.randint(97, 97 + 26 - 1)  # considering only upper and lowercase letters
        random_integer = random_integer
        random_string += (chr(random_integer))
    if generate_first_letter_uppercase_on:
        random_string = random_string.title()
    if var_exists(text, random_string) or random_string in name_exceptions:
        return generate_random_name(text)
    else:
        return random_string


def change_var_names(text, var):
    if debug_on:
        print(var, "'s name changed")
    if "main" in var:
        return text
    random_name = generate_random_name(text)
    for i in syntax_symbols:
        for j in syntax_symbols:
            if i + var + j != ".h>":
                text = text.replace(i + var + j, i + random_name + j)
    return text


# ==========

# ========== long long i,c -> long long i long long c
def comma_to_full(text):
    text = text.split("\n")
    for i in range(1, len(text)):
        if "," in text[i] and "(" not in text[i] and "{" not in text[i] and "[" not in text[i] and "<" not in text[i]:
            for j in types:  # TODO kostyl
                # print(text[i],j,len(text[i].split()), j in text[i].split()[0]+text[i].split()[1])
                if len(text[i].split()) > 2:
                    if j in text[i].split()[0] or j in text[i].split()[0] + " " + text[i].split()[1] or j in \
                            text[i].split()[0] + " " + text[i].split()[1] + text[i].split()[2]:
                        text[i] = text[i].replace(", ", "; \n    " + j + " ")
                        text[i] = text[i].replace(",", "; \n    " + j + " ")
                        break
                elif len(text[i].split()) > 1:
                    if j in text[i].split()[0] or j in text[i].split()[0] + " " + text[i].split()[1]:
                        text[i] = text[i].replace(", ", "; \n    " + j + " ")
                        text[i] = text[i].replace(",", "; \n    " + j + " ")
                        break
                elif len(text[i].split()) > 0:
                    if j in text[i].split()[0]:
                        text[i] = text[i].replace(", ", "; \n    " + j + " ")
                        text[i] = text[i].replace(",", "; \n    " + j + " ")
                        break

    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


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
    text = text.replace(" (", "(")
    text = text.replace("(", " (")
    return text


# ==========

# ==========
def using_to_define(text):
    text = text.split("\n")
    for i in range(0, len(text)):
        if "using" in text[i] and "=" in text[i] and "using namespace std" not in text[i]:
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
    text = text.split("\n")
    for i in range(0, len(text)):
        if "#define" not in text[i]:
            text[i] = clear_spaces_in_string("\n" + text[i] + "\n")[1:-1]
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


def clear_spaces_in_string(text):
    i = 1
    open_bracket_counter = 0
    while i < len(text) - 1:  # -1!
        if text[i] in "\"\'" and open_bracket_counter == 0:
            open_bracket_counter += 1
        elif text[i] in "\"\'" and open_bracket_counter == 1:
            open_bracket_counter -= 1
        elif text[i] == " " and open_bracket_counter == 0:
            if text[i - 1].isalnum():
                if text[i + 1] in syntax_symbols:
                    text = text[:i] + text[i + 1:]
            if text[i - 1] in syntax_symbols:
                if text[i + 1].isalnum() or text[i + 1] in syntax_symbols:
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
    text = text.replace("> ", ">")
    text = text.replace(">", "> ")
    text = text.replace("> >", ">>")
    return text


# ==========

# ==========
def zero_in_fast_input(text):
    for i in syntax_symbols:
        for j in syntax_symbols:
            for k in null_false_zeros:
                text = text.replace(i + "cin.tie(" + k + ")" + j, i + "cin.tie(0)" + j)
                text = text.replace(i + "ios_base::sync_with_stdio(" + k + ")" + j,
                                    i + "ios_base::sync_with_stdio(0)" + j)
    return text


# ==========

def titov_codestyle(text):
    text = text.split('\n')
    for i in range(len(text)):
        text[i] += '\n'
    output_code = ""
    prev = ''
    words = []
    gap = False

    for line in text:
        if gap:
            gap = False
            prev = line
            continue
        outline = ''

        tabulation = True
        tab = 0
        comment = len(prev)
        for ch in range(comment - 1):
            if prev[ch] == '/' and prev[ch + 1] == '/':
                comment = ch
                break
            if (prev[ch] == '\t' or prev[ch] == ' ') and tabulation:
                tab = ch + 1
            else:
                tabulation = False

        outline += prev[tab:comment]

        charr = line.replace(' ', '').replace('\t', '')
        if charr.count('//') > 0:
            charr = charr[:charr.index('/') - 1]

        if len(charr) > 1:
            charr = charr[:-1]

        if charr == '{':
            outline = outline[:-1]
            outline += ' {\n'
            gap = True
        if outline.count('{') == 1:
            match outline[:2]:
                case 'fo':
                    words.append('// for')
                case 'wh':
                    words.append('// while')
                case 'if':
                    words.append('// if')
                case 'sw':
                    words.append('// switch')
                case 'el':
                    if outline.count('else if') > 0:
                        words.append('// else if')
                    else:
                        words.append('// else')
                case _:
                    words.append('')
        if prev.count('}') > 0:
            outline = outline[:-1] + ' '
            if len(words) > 0:
                outline += words.pop(-1) + '\n'

        prev = line
        output_code += outline + '\n    '
    return output_code


def typedef_to_define(text):
    text = text.split("\n")
    for i in range(1, len(text)):
        if len(text[i].split()) > 0:
            if "typedef" in text[i].split()[0] and len(text[i].split()) > 2:
                text[i] = "#define " + text[i].split()[-1].replace(";", "") + " " + " ".join(
                    text[i].split()[1:len(text[i].split()) - 1])
    text_l = text
    text = ""
    for i in text_l:
        text += i + "\n"
    return text


def get_cleaned_text(text, n):
    if remove_comments_on:
        text = commentRemover(text)

    if 1:
        # experimental part that theoretically can help avoid some errors)
        text = text.replace(", ", ",")
        text = text.replace(",", ", ")
        text = text.replace("> ", ">")
        text = text.replace(">", "> ")
        text = text.replace("> >", ">>")

    if clear_spaces_on:
        text = clear_spaces(text)

    if zero_in_fast_input_on:
        text = zero_in_fast_input(text)

    if using_to_define_on:
        text = using_to_define(text)

    if comma_to_full_on:
        text = comma_to_full(text)

    if exponent_to_decimal_on:
        text = exponent_to_decimal(text)
    if typedef_to_define_on:
        text = typedef_to_define(text)
    if clear_defines_on:
        text = clear_defines(text)

    if const_to_define_on or const_to_code_on:
        text = text.replace(" (", "(")
        text = text.replace("(", " (")
        if const_to_define_on:
            text = const_plus_to_space(text)
            text = const_to_define(text)
        elif const_to_code_on:
            text = const_plus_to_space(text)
            text = const_to_define(text)
            text = clear_spaces(text)
            text = clear_defines(text)
        text = clear_spaces(text)

    if replace_libs_to_bitsstd_on:
        text = replace_libs_to_bitsstd(text)

    if return0_check_on:
        text = return0_check(text)

    if delete_cout_tie_zero_on:
        text = delete_cout_tie_zero(text)

    if add_fast_input_on:
        text = add_fast_input(text)

    if some_codestyle_changes_on:
        text = some_codestyle_changes(text)
        text = dotcomma_endl(text)

    if remove_not_used_funcs_on and (n == 1 or n == 2):
        text = remove_not_used_funcs(text)

    if titov_codestyle_on and (n == 1 or n == 2) and two_line_program_on != 1:
        text = titov_codestyle(text)

    if delete_empty_lines_on:
        text = delete_empty_lines(text)

    if clear_spaces_on:
        text = clear_spaces(text)

    if random_endlines_on and n == 1 or n == 2:
        text = random_endl(text)

    if two_line_program_on and n == 2:
        text = two_line_program(text)
        if crazy_two_liner_on:
            text = crazy_two_liner(text)
    elif n == 0:
        text = text.replace("\n}\n", "\n}\n\n")
        text = text.replace("\n};\n", "\n};\n\n")
        text = text.replace(",", ", ")

    text = text.replace(")", ") ")
    text = text.replace(") )", "))")
    text = text.replace("    ;", "     ;")
    text = text.replace(" ;", ";")
    text = text.replace("< =", "<=")
    text = text.replace("> =", ">=")

    if debug_on:
        print("debug out: ", text)

    return text


def go_skat(text):
    text1 = text
    text = get_cleaned_text(text, 0)
    i = 1
    while text1 != text and i != 100:
        i += 1
        text1 = text
        text = get_cleaned_text(text, i)
    else:
        text = get_cleaned_text(text, 1)
        text = get_cleaned_text(text, 2)
    return text
