#!/usr/bin/env python
# -*- coding: Latin-1 -*-

"""
The LaTeX 'acronym.sty' by default displays all acronyms specified in the
'acronym' environment. In case you want to reuse existing acronym
specifications and need to tailor the database to your needs, this script can
help you.

1.) Put all acronyms in a separate file like 'acrodb.tex' and '\input' it.
2.) Write your thesis and add acronyms as needed.
3.) When you are done writing, use this script to tailor the database to the
    needs of your work.
4.) Replace 'acrodb.tex' by 'acronyms.tex' in the '\input' command
"""


from glob import glob
import re
import sys


# A list of regexes to specify used acronyms
RE_USE = [
    r"\\ac{([A-Za-z/1-9]*)}",
    r"\\acf{([A-Za-z/1-9]*)}",
    r"\\acs{([A-Za-z/1-9]*)}",
    r"\\acp{([A-Za-z/1-9]*)}",
    r"\\acfp{([A-Za-z/1-9]*)}",
    r"\\acsp{([A-Za-z/1-9]*)}",
    r"\\aclp{([A-Za-z/1-9]*)}",
]


# A regex for finding acronym definitions
RE_DEF = r".*\\acro{([A-Za-z/1-9]*).*}"


def read_used_acronyms(dbfile, outfile):
    """ Extracts all used acronyms from all the .tex files except 'infile' and
    'outfile', both parameters have to be filenames. Returns a 'set',
    containing all the used acronyms.
    """
    acronyms = set()
    filenames = glob("*.tex")
    for filename in filenames:
        if filename != dbfile and filename != outfile:
            file = open(filename, 'r')
            for line in file:
                for rx in RE_USE:
                    acros = set(re.findall(rx, line))
                    acronyms.update(acros)
    return acronyms


def read_acronym_database(dbfile):
    """ Reads in the database of acronyms and puts the acronym and it's
    specification into a dictionary. The dict is of the form:
       'acronym' --> 'description'
    Afterwards that dict is returned.
    """
    acrodb = dict()  # dict for acronym database
    acrofile = open(dbfile)
    for line in acrofile:
        match = re.match(RE_DEF, line)
        if match:
            acrodb[match.groups()[0]] = line
        else:
            line, " did not match"
    return acrodb


def output_tailored_db(acrodb, acronyms, outfile):
    acroout = open(outfile, 'w')
    acroout.write("""\\chapter{Used Acronyms}
    \\begin{acronym}\n""")

    # match and output acronyms against db
    for acro in sorted(acronyms):
        if acro in acrodb:
            print ".",
            acroout.write("\t" + acrodb[acro].strip() + "\n")
        else:
            print "Missing Acronym: %s" % (acro)

    acroout.write("\\end{acronym}\n")
    acroout.close()


def usage():
    """ acrobib.py [dbfile] [outfile]
    When run without arguments, the following defaults are used:
        dbfile = 'acrodb.tex'
        outfile = 'acronyms.tex'
    """


def main():
    dbfile = 'acrodb.tex'
    outfile = 'acronyms.tex'
    args = sys.argv
    if len(args) > 1:
        dbfile = args[1]
    else:
        print "Using database: 'acrodb.tex'"
    if len(args) > 2:
        outfile = args[2]
    else:
        print "Writing to 'acronyms.tex'"
    acrodb = read_acronym_database(dbfile)
    acronyms = read_used_acronyms(dbfile, outfile)
    output_tailored_db(acrodb, acronyms, outfile)


if __name__ == '__main__':
    try:
        main()
    except e:
        usage()
        print "Backtrace: \n", e

