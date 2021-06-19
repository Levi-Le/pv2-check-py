#!/usr/bin/python

import re

# color in output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    PASS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# defining regex
vanilla_xref = re.compile(r"<<.*>>")
pseudo_vanilla_xref = re.compile(r"<<.* .*>>")
single_comment = re.compile(r'^//.*$')
html_markup = re.compile(r'<.*>.*<\/.*>')


# defining strings
abstract_tag = '[role="_abstract"]'
add_res_tag = '[role="_additional-resources"]'
exp_tag = ':experimental:'

# recording the files
filename = "/home/levi/rhel-8-docs/rhel-8/modules/dotnet/con_removed-environment-variables.adoc"


def abstarct_tag_check(filename, line):
    if not abstract_tag.match(line):
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: abstract tag is missing in the found in the following files" + bcolors.ENDC, filename, sep='\n', end='\n')
        print(line)


# vanilla xref check
def vanilla_check(filename):
    if vanilla_xref.match(line) and not pseudo_vanilla_xref.match(line):
        print(bcolors.FAIL + bcolors.BOLD + "FAIL: vanilla xrefs found in the following files" + bcolors.ENDC, filename, sep='\n', end='\n')
        print(line)


# open file
with open(filename) as file:
    # remove single-line comments
    for line in file:
        line = line.partition(r'^//.*')[0]
        line = line.rstrip()
        # read file
        content = file.read()

# report vanilla xrefs
for line in content.splitlines():
    vanilla_check(filename)

matches = re.findall(html_markup, line)
print(matches)
