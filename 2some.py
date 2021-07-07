#!/usr/bin/python3

import re
import os


class Colors:
    '''
    defines colors to use in the command line output
    '''
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Regex:
    """defines regular expresiions for the checks."""

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
    EMPTY_LINE_AFTER_ADD_RES_HEADER = re.compile(r'== Additional resources\s\n|\.Additional resources\s\n', re.IGNORECASE)
    COMMENT_AFTER_ADD_RES_HEADER = re.compile(r'\.Additional resources\s(?=\//|(/{4,})(.*\n)*?(/{4,}))|== Additional resources\s(?=\//|(/{4,})(.*\n)*?(/{4,}))', re.IGNORECASE)


def print_fail(check, message, files):
    '''
    fail message that gets called when the check fails
    '''
    separator = '\n'
    if files:
        print(Colors.FAIL + Colors.BOLD + "FAIL: " + check + message + ":" + Colors.END, files, sep='\n')


def vanilla_xref_check(stripped_file):
    '''
    checks if the file contains vanilla xrefs
    '''
    if re.findall(Regex.VANILLA_XREF, stripped_file):
        #print_fail("vanilla xrefs found in the following files", file_path)
        return True

def inline_anchor_check(stripped_file):
    '''
    checks if the in-line anchor directly follows the level 1 heading
    '''
    if re.findall(Regex.INLINE_ANCHOR, stripped_file):
        return True


def create_report(report, stripped_file, file_path):
    if vanilla_xref_check(stripped_file):
        if not 'vanilla xrefs' in report:
            report['vanilla xrefs'] = []
        report['vanilla xrefs'].append(file_path)

    if inline_anchor_check(stripped_file):
        if not 'in-line anchor' in report:
            report['in-line anchor'] = []
        report['in-line anchor'].append(file_path)


def print_report(report):
    for checks, files in report.items():
        separator = '\n'
        print_fail(check, "found in the following files", separator.join(files))


"""def report(stripped_file, grouped_files, another_grouped_files, file_path):
    if vanilla_xref_check(stripped_file):
        grouped_files.append(file_path)

    if inline_anchor_check(stripped_file):
        another_grouped_files.append(file_path)"""


def print_report(report):
    for check, files in report.items():
        separator = "\n"
        print_fail(check, " found in the following files", files)


folderpath = r"test-files"
filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]


def validation(file_name):
    report = {}

    for path in file_name:
        with open(path, "r") as file:
            original = file.read()
            stripped = Regex.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regex.SINGLE_LINE_COMMENT.sub('', stripped)
            # FIXME: figure out a better way to exclude pseudo vanilla xrefs
            stripped = Regex.PSEUDO_VANILLA_XREF.sub('', stripped)
            stripped = Regex.CODE_BLOCK.sub('', stripped)
            create_report(report, stripped, path)
    print_report(report)


validation(filepaths)
