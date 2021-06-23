#!/usr/bin/python3

import re
import os

filename = "/home/levi/rhel-8-docs/rhel-8/modules/dotnet/con_removed-environment-variables.adoc"


# color in output
class bcolors:
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class regex:
    VANILLA_XREF = re.compile(r'<<.*>>')
    PSEUDO_VANILLA_XREF = re.compile(r'<<((.*) (.*))*>>')
    MULTI_LINE_COMMENT = re.compile(r'(/{4,})(.*\n)*?(/{4,})')
    SINGLE_LINE_COMMENT = re.compile(r'(?<!//)(?<!/)//(?!//).*\n?')
    EMPTY_LINE_AFTER_ABSTRACT = re.compile(r'\[role="_abstract"]\n(?=\n)')
    FIRST_PARA = re.compile(r'(?<!\n\n)\[role="_abstract"]\n(?!\n)')
    NO_EMPTY_LINE_BEFORE_ABSTRACT = re.compile(r'(?<!\n\n)\[role="_abstract"]')
    COMMENT_AFTER_ABSTRACT = re.compile(r'\[role="_abstract"]\n(?=\//|(/{4,})(.*\n)*?(/{4,}))')
    VAR_IN_TITLE = re.compile(r'(?<!\=)=\s.*{.*}.*')
    INLINE_ANCHOR = re.compile(r'=.*\[\[.*\]\]')
    UI_MACROS = re.compile(r'btn:\[.*\]|menu:.*\]|kbd:.*\]')
    HTML_MARKUP = re.compile(r'<.*>.*<\/.*>|<.*>\n.*\n</.*>')
    CODE_BLOCK = re.compile(r'(?<=\.\.\.\.\n)((.*)\n)*(?=\.\.\.\.)|(?<=----\n)((.*)\n)*(?=----)')
    HUMAN_READABLE_LABEL_XREF = re.compile(r'xref:.*\[]')
    NESTED_ASSEMBLY = re.compile(r'include.*assembly_([a-z|0-9|A-Z|\-|_]+)\.adoc(\[.*\])')
    NESTED_MODULES = re.compile(r'include.*(proc|con|ref)_([a-z|0-9|A-Z|\-|_]+)\.adoc(\[.*\])')
    RELATED_INFO = re.compile(r'= Related information|.Related information', re.IGNORECASE)
    ADDITIONAL_RES = re.compile(r'= Additional resources|\.Additional resources', re.IGNORECASE)
    ADD_RES_ASSEMBLY = re.compile(r'== Additional resources', re.IGNORECASE)
    ADD_RES_MODULE = re.compile(r'\.Additional resources', re.IGNORECASE)
    EMPTY_LINE_AFTER_ADD_RES_TAG = re.compile(r'\[role="_additional-resources"]\n(?=\n)')
    COMMENT_AFTER_ADD_RES_TAG = re.compile(r'\[role="_additional-resources"]\n(?=\//|(/{4,})(.*\n)*?(/{4,}))')
    EMPTY_LINE_AFTER_ADD_RES_HEADER = re.compile(r'== Additional resources|\.Additional resources\s\n')
    COMMENT_AFTER_ADD_RES_HEADER = re.compile(r'== Additional resources|\.Additional resources\s(?=\//|(/{4,})(.*\n)*?(/{4,}))')


class file_types:
    ASSEMBLY = re.compile(r'assembly_.*\.adoc')
    CONCEPT = re.compile(r'con_.*\.adoc')
    PROCEDURE = re.compile(r'proc_.*\.adoc')
    REFERENCE = re.compile(r'ref_.*\.adoc')


class tags:
    ABSTRACT = '[role="_abstract"]'
    ADD_RES = '[role="_additional-resources"]'
    EXPERIMENTAL = ':experimental:'
    LVLOFFSET = ':leveloffset:'


def print_fail(message, files):
    print(bcolors.FAIL + bcolors.BOLD + "FAIL: " + message + ":" + bcolors.END, files, sep='\n')


def print_warn(message, files):
    print(bcolors.WARN + bcolors.BOLD + "WARNING: " + message + ":" + bcolors.END, files, sep='\n')


def vanilla_xref_check(stripped_file, file):
    # check if file has related information section
    if re.findall(regex.VANILLA_XREF, stripped_file):
        print_fail("vanilla xrefs found in the following files", file)


def var_in_title_check(stripped_file, file):
    # check if title has a variable
    if re.findall(regex.VAR_IN_TITLE, stripped_file):
        print_fail("the following files have variable in the level 1 heading", file)


def inline_anchor_check(stripped_file, file):
    # check if file has in-line anchors
    if re.findall(regex.INLINE_ANCHOR, stripped_file):
        print_fail("in-line anchors found in the following files", file)


def experimental_tag_check(stripped_file, file):
    if stripped_file.count(tags.EXPERIMENTAL) > 0:
        return
    elif re.findall(regex.UI_MACROS, stripped_file):
            print_fail("experimental tag is missing in the following files", file)


def html_markup_check(stripped_file, file):
    if re.findall(regex.HTML_MARKUP, stripped_file):
        print_fail("HTML markup is found in the following files", file)


def nesting_in_assemblies_check(stripped_file, file):
    name_of_file = os.path.basename(file)
    if file_types.ASSEMBLY.fullmatch(name_of_file):
        if re.findall(regex.NESTED_ASSEMBLY, stripped_file):
            print_fail("the following files contain nested assemblies", file)
        if re.findall(tags.LVLOFFSET, stripped_file):
            print_fail("the following files contain unsupported includes", file)


def nesting_in_modules_check(stripped_file, file):
    name_of_file = os.path.basename(file)
    if not file_types.ASSEMBLY.fullmatch(name_of_file):
        if re.findall(regex.NESTED_ASSEMBLY, stripped_file):
            print_fail("the following module contains nested assemblies", file)
        if re.findall(regex.NESTED_MODULES, stripped_file):
            print_fail("the following module contains nested modules", file)


def human_readable_label_check(stripped_file, file):
    if re.findall(regex.HUMAN_READABLE_LABEL_XREF, stripped_file):
        print_fail("the following files have xrefs without a human readable label", file)


def abstarct_tag_check(stripped_file, original_file, file):
    # record occurences of abstract tag
    occurrences_abstract_tag = stripped_file.count(tags.ABSTRACT)
    if occurrences_abstract_tag == 0:
        # if no abstract tag => fail msg
        print_fail("abstract tag is missing in the following files", file)
        return
    if occurrences_abstract_tag > 1:
        print_fail("abstract tag appears multiple times in the following files", file)
        return
    # check if abstract tag is set once
    if occurrences_abstract_tag == 1:
        first_paragraph_check = re.findall(regex.FIRST_PARA, original_file)
        if first_paragraph_check:
            print_fail("there is no line between the level 1 heading and the abstract tag in the following files. the first paragraph might render incorrectly", file)
            return
        empty_line_before_abstract_tag = re.findall(regex.NO_EMPTY_LINE_BEFORE_ABSTRACT, original_file)
        if empty_line_before_abstract_tag:
            print_fail("the following files have no empty line before the abstract tag", file)
        empty_line_after_abstract_tag = re.findall(regex.EMPTY_LINE_AFTER_ABSTRACT, original_file)
        if empty_line_after_abstract_tag:
            print_fail("the following files have an empty line after the abstract tag", file)
            return
        comment_after_abst_tag = re.findall(regex.COMMENT_AFTER_ABSTRACT, original_file)
        if comment_after_abst_tag:
            print_fail("the following files have an comment after the abstract tag", file)


def add_res_section_check(stripped_file, original_file, file):
    if re.findall(regex.RELATED_INFO, stripped_file):
        print_fail("'Related information' section was found in the following files. Change the section name to 'Additional resources'", file)
        return
    if re.findall(regex.ADDITIONAL_RES, stripped_file):
        name_of_file = os.path.basename(file)
        if file_types.ASSEMBLY.fullmatch(name_of_file):
            if not re.findall(regex.ADD_RES_ASSEMBLY, stripped_file):
                print_fail("additional resources section for assemblies should be `== Additional resources`", file)
        elif not re.findall(regex.ADD_RES_MODULE, stripped_file):
                print_fail("additional resources section for modules should be `.Additional resources`", file)
        if stripped_file.count(tags.ADD_RES) == 0:
            print_fail("additional resources tag is missing in the found in the following files", file)
            return
        if stripped_file.count(tags.ADD_RES) > 1:
            print_fail("additional resources tag appears multiple times in the following files", file)
        if stripped_file.count(tags.ADD_RES) == 1:
            if re.findall(regex.EMPTY_LINE_AFTER_ADD_RES_TAG, original_file):
                print_fail("the following files have an empty line after the additional resources tag", file)
            elif re.findall(regex.COMMENT_AFTER_ADD_RES_TAG, original_file):
                print_fail("the following files have comments after the additional resources tag", file)
            if re.findall(regex.EMPTY_LINE_AFTER_ADD_RES_HEADER, original_file):
                print_fail("the following files have an empty line after the additional resources header", file)
            elif re.findall(regex.COMMENT_AFTER_ADD_RES_HEADER, original_file):
                    print_fail("the following files have comments after the additional resources header", file)


def validation(filename):
    with open(filename, "r") as file:
        original = file.read()
        # exclude multi-line comments
        stripped = regex.MULTI_LINE_COMMENT.sub('', original)
        # exclude single-line comments
        stripped = regex.SINGLE_LINE_COMMENT.sub('', stripped)
        # FIXME:
        # excludes pseudo xrefs
        stripped = regex.PSEUDO_VANILLA_XREF.sub('', stripped)
        stripped = regex.CODE_BLOCK.sub('', stripped)

        experimental_tag_check(stripped, filename)
        var_in_title_check(stripped, filename)
        inline_anchor_check(stripped, filename)
        abstarct_tag_check(stripped, original, filename)
        nesting_in_assemblies_check(stripped, filename)
        nesting_in_modules_check(stripped, filename)
        vanilla_xref_check(stripped, filename)
        html_markup_check(stripped, filename)
        human_readable_label_check(stripped, filename)
        add_res_section_check(stripped, original, filename)


validation(filename)
