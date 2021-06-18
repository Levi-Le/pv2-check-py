#!/usr/bin/python

import re

vanilla_xref = re.compile(r"<<.*>>")
pseudo_vanilla_xref = re.compile(r"<<.* .*>>")
single_comment = re.compile(r'^//.*$')
html_markup = re.compile(r'<.*>.*<\/.*>')


def vanilla_check(line):
    if vanilla_xref.match(line) and not pseudo_vanilla_xref.match(line):
        print(line)


with open("/home/levi/rhel-8-docs/rhel-8/modules/dotnet/con_removed-environment-variables.adoc") as file:
    content = file.read()


for line in content.splitlines():
    vanilla_check(line)


matches = re.findall(html_markup, line)
print(matches)
