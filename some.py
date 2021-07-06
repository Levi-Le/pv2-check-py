#!/usr/bin/python3

from contextlib import contextmanager
import re


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
    '''
    defines regular expresiions for the checks
    '''
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


def print_fail(message, files):
    '''
    fail message that gets called when the check fails
    '''
    print(Colors.FAIL + Colors.BOLD + "FAIL: " + message + ":" + Colors.END, files, sep='\n')


def vanilla_xref_check(stripped_file, file):
    '''
    checks if the file contains vanilla xrefs
    '''
    if re.findall(Regex.VANILLA_XREF, stripped_file):
        print_fail("vanilla xrefs found in the following files", file)


@contextmanager


def multi_file_manager(files, mode='rt'):
    '''
    Open multiple files and make sure they all get closed.
    '''
    files = [open(file, mode) for file in files]
    yield files
    for file in files:
        file.close()


FILENAMES = 'test-files/assembly_some-assembly-var.adoc', 'test-files/proc_some-module.adoc'

def html_markup_check(stripped_file, file):
    '''
    checks if HTML markup is present in the file
    '''
    if re.findall(Regex.HTML_MARKUP, stripped_file):
        print_fail("HTML markup is found in the following files", file)

def validation(file_name):
    with multi_file_manager(FILENAMES) as files:
        for file in files:
            original = file.read()
            stripped = Regex.MULTI_LINE_COMMENT.sub('', original)
            stripped = Regex.SINGLE_LINE_COMMENT.sub('', stripped)
            # FIXME: figure out a better way to exclude pseudo vanilla xrefs
            stripped = Regex.PSEUDO_VANILLA_XREF.sub('', stripped)
            stripped = Regex.CODE_BLOCK.sub('', stripped)

            vanilla_xref_check(stripped, file_name)
            html_markup_check(stripped, file_name)


validation(FILENAMES)
