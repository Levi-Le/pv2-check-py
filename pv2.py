#!/usr/bin/python3

import re

filename = "/home/levi/rhel-8-docs/rhel-8/modules/dotnet/con_removed-environment-variables.adoc"


# color in output
class bcolors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


vanilla_xref = re.compile(r'<<.*>>')
pseudo_vanilla_xref = re.compile(r'<<((.*) (.*))*>>')
multi_line_comments = re.compile(r'(/{4,})(.*\n)*?(/{4,})')
single_line_comments = re.compile(r'(?<!//)(?<!/)//(?!//).*\n?')
empty_line_after_abstract = re.compile(r'\[role="_abstract"]\n(?=\n)')
first_paragraph_renders = re.compile(r'(?<!\n\n)\[role="_abstract"]\n(?!\n)')
no_empy_line_before_abstract = re.compile(r'(?<!\n\n)\[role="_abstract"]')
comment_after_abstract = re.compile(r'\[role="_abstract"]\n(?=\//|(/{4,})(.*\n)*?(/{4,}))')
var_in_titles = re.compile(r'(?<!\=)=\s.*{.*}.*')
inline_anchor = re.compile(r'=.*\[\[.*\]\]')
ui_macros = re.compile(r'btn:\[.*\]|menu:.*\]|kbd:.*\]')
html_markup = re.compile(r'<.*>.*<\/.*>|<.*>\n.*\n</.*>')
code_blocks = re.compile(r'(?<=\.\.\.\.\n)((.*)\n)*(?=\.\.\.\.)|(?<=----\n)((.*)\n)*(?=----)')

abstract_tag = '[role="_abstract"]'
experimental_tag = ':experimental:'


def print_fail(message, files):
    print(bcolors.FAIL + bcolors.BOLD + "FAIL: " + message + ":" + bcolors.END, files, sep='\n')


def print_warn(message, files):
    print(bcolors.WARN + bcolors.BOLD + "WARNING: " + message + ":" + bcolors.END, files, sep='\n')


def vanilla_xref_check(stripped_file, file):
    # check if file has related information section
    vanilla = re.findall(vanilla_xref, stripped_file)
    # if vanilla xrefs => fail msg
    if vanilla:
        print_fail("vanilla xrefs found in the following files", file)


def var_in_title_check(stripped_file, file):
    # check if title has a variable
    var_title = re.findall(var_in_titles, stripped_file)
    if var_title:
        print_fail("the following files have variable in the level 1 heading", file)


def inline_anchor_check(stripped_file, file):
    # check if file has in-line anchors
    anchor = re.findall(inline_anchor, stripped_file)
# if inline-anchors => fail msg
    if anchor:
        print_fail("in-line anchors found in the following files", file)


def experimental_tag_check(stripped_file, file):
    occurrences_experimental_tag = stripped_file.count(experimental_tag)
    if occurrences_experimental_tag > 0:
        return
    ui_elements = re.findall(ui_macros, stripped_file)
    if ui_elements:
        if occurrences_experimental_tag == 0:
            print_fail("experimental tag is missing in the following files", file)


def html_markup_check(stripped_file, file):
    occurences_html_markup = re.findall(html_markup, stripped_file)
    if occurences_html_markup:
        print_fail("HTML markup is found in the following files", file)



def abstarct_tag_check(stripped_file, original_file, file):
    # record occurences of abstract tag
    occurrences_abstract_tag = stripped_file.count(abstract_tag)
    if occurrences_abstract_tag == 0:
        # if no abstract tag => fail msg
        print_fail("abstract tag is missing in the following files", file)
        return
    if occurrences_abstract_tag > 1:
        print_fail("abstract tag appears multiple times in the following files", file)
        return
    # check if abstract tag is set once
    if occurrences_abstract_tag == 1:
        first_paragraph_check = re.findall(first_paragraph_renders, original_file)
        if first_paragraph_check:
            print_fail("there is no line between the level 1 heading and the abstract tag in the following files. the first paragraph might render incorrectly", file)
            return
        empty_line_before_abstract_tag = re.findall(no_empy_line_before_abstract, original_file)
        if empty_line_before_abstract_tag:
            print_fail("the following files have no empty line before the abstract tag", file)
        empty_line_after_abstract_tag = re.findall(empty_line_after_abstract, original_file)
        if empty_line_after_abstract_tag:
            print_fail("the following files have an empty line after the abstract tag", file)
            return
        comment_after_abst_tag = re.findall(comment_after_abstract, original_file)
        if comment_after_abst_tag:
            print_fail("the following files have an comment after the abstract tag", file)

#  open file
with open(filename, "r") as file:
    original = file.read()
    # exclude multi-line comments
    stripped = multi_line_comments.sub('', original)
    # exclude single-line comments
    stripped = single_line_comments.sub('', stripped)
    # FIXME:
    # excludes pseudo xrefs
    stripped = pseudo_vanilla_xref.sub('', stripped)
    stripped = code_blocks.sub('', stripped)

# report vanilla xrefs check
vanilla_xref_check(stripped, filename)
abstarct_tag_check(stripped, original, filename)
var_in_title_check(stripped, filename)
inline_anchor_check(stripped, filename)
experimental_tag_check(stripped, filename)
html_markup_check(stripped, filename)
