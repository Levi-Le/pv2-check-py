#!/usr/bin/python3

import re

# color in output
class bcolors:
    PASS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# defining regex
# abstract_tag = re.compile(r"^\[role\=\"\_abstract\"\]")
vanilla_xref = re.compile(r'<<.*>>')
pseudo_vanilla_xref = re.compile(r"<<.* .*>>")
single_comment = re.compile(r'^//.*$')
html_markup = re.compile(r'<.*>.*<\/.*>')
empty_line1 = re.compile(r'\[role=\"_additional-resources\"\](?=\n\n)')
empty_line = re.compile(r'\[role=\"_additional-resources\"\]\n\n')


# defining strings
abstract_tag = '[role="_abstract"]'
add_res_tag = '[role="_additional-resources"]'
exp_tag = ':experimental:'
# TODO: ignore case
add_res_header = 'Additional resources'

# recording the files
filename = "/home/levi/rhel-8-docs/rhel-8/modules/dotnet/con_removed-environment-variables.adoc"




def skip_comments(file):
    for line in file:
        if not line.strip().startswith('//'):
            yield line


# abstract tag check
def abstarct_tag_check(filename):
    # record occurences of abstract tag
    occurrences_abstract_tag = content.count(abstract_tag)
    # check if abstract tag is not set
    if occurrences_abstract_tag == 0:
        # if no abstract tag => fail msg
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: abstract tag is missing in the found in the following files:" + bcolors.ENDC, file.name, sep='\n', end='\n')
    # check if abstract tag is set once
    if occurrences_abstract_tag == 1:
        # check for empty line after abstract tag
        empty_line_after_abst_tag = re.findall(r'\[role="_abstract"]\n(?=\n)', content)
        # if empty line after abstract tag => fail msg
        if empty_line_after_abst_tag:
            print(bcolors.FAIL + bcolors.BOLD + "FAIL: the following files have an empty line after the abstract tag:" + bcolors.ENDC, file.name, sep='\n', end='\n')
        else:
            # check for comments after abstract tag
            comment_after_abst_tag = re.findall(r'\[role="_abstract"]\n(?=\//|\////)', content)
            # if comments after abstract tag => fail msg
            if comment_after_abst_tag:
                print(bcolors.FAIL + bcolors.BOLD + "FAIL: the following files have comment after the abstract tag:" + bcolors.ENDC, file.name, sep='\n', end='\n')
    # if abstract tag appears more than once => fail msg
    if occurrences_abstract_tag > 1:
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: abstract tag appears multiple times in the following files:" + bcolors.ENDC, file.name, sep='\n', end='\n')


# additional resources tag check
def add_res_tag_check(filename):
    # check if file has related information section
    add_res_wrong_header = re.findall(r'(?<=\=\=\s)Related information', content, re.IGNORECASE) or re.findall(r'(?<=\.)Related information', content, re.IGNORECASE)
    # if re;ated infor section is used instead of additional resources section => fail msg
    if add_res_wrong_header:
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: 'Related information' section was found. Change the section name to 'Additional resources' in the following files:" + bcolors.ENDC, file.name, sep='\n', end='\n')
    # check if file has additional resources section
    occurrences_add_res_header = re.findall(r'(?<=\=\=\s)Additional resources', content, re.IGNORECASE) or re.findall(r'(?<=\.)Additional resources', content, re.IGNORECASE)
    if occurrences_add_res_header:
        # if additional resources section exists
        # check if the additional resources tag is not set
        if content.count(add_res_tag) == 0:
            # if no additional resources tag => fail msg
            print(bcolors.FAIL + bcolors.BOLD + "FAIL: additional resources tag is missing in the found in the following files:" + bcolors.ENDC, file.name, sep='\n', end='\n')
        # if additional resources tag is set
        if content.count(add_res_tag) == 1:
            # check if empty line after additional resources tag
            empty_line_after_add_res = re.findall(r'\[role="_additional-resources"]\n(?=\n)', content)
            empty_line_after_add_res_header = re.findall(r'(?<=\=\=\s)Additional resources\n(?=\n)', content, re.IGNORECASE) or (r'(?<=\.)Additional resources\n(?=\n)', content, re.IGNORECASE)
            # if empty line after additional resources tag => fail msg
            if empty_line_after_add_res:
                print(bcolors.FAIL + bcolors.BOLD + "FAIL: the following files have an empty line after the additional resources tag:" + bcolors.ENDC, file.name, sep='\n', end='\n')
            if empty_line_after_add_res_header:
                print(bcolors.FAIL + bcolors.BOLD + "FAIL: the following files have an empty line after the additional resources header:" + bcolors.ENDC, file.name, sep='\n', end='\n')


# vanilla xref check
def vanilla_check(filename):
    vanilla = re.findall(vanilla_xref, line) and not re.findall(pseudo_vanilla_xref, line)
    if vanilla:
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: vanilla xrefs found in the following files:" + bcolors.ENDC, file.name, vanilla_xref.findall(line)[0], sep='\n', end='\n')
        # print(line)


# open file
with open(filename, "r") as file:
    for line in file:
        line = line.partition('//')[0]
        line = line.rstrip()
        content = file.read()

# report abstract tag check
abstarct_tag_check(filename)


# report vanilla xrefs check
for line in content.splitlines():
    vanilla_check(filename)

# report additional resources tag check
add_res_tag_check(filename)
