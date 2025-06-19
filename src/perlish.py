#!/usr/bin/python

import sys

# based on http://norvig.com/python-iaq.html
def printf(format, *args):
     """Format args with the first argument as format string, and print.
     If the format is not a string, it is converted to one with str.
     You must use printf('%s', x) instead of printf(x) if x might
     contain % or backslash characters."""
     sys.stdout.write(str(format) % args)

def fprintf(fp, format, *args): fp.write(str(format) % args)

def sprintf(format, *args): return (str(format) % args);

def join(str, list):
	return str.join(list)

def die(format, *args):
    sys.stderr.write((str(format)+"\n") % args)
    raise Exception ("die");

# remove trailing newlines in various styles.
def chomp(s):
    return s.rstrip("\r\n")

# join elements of list using string as a seperator.
def join(str, list):
    r = str.join(list);
    return r;

# for split(RE, string) use re.split(RE, string);

#"""shift the first element off of the list and return it,
#modifying the list in place."""
def shift(list):
    t = list[0];
    list[:] = list[1:]
    return t;

if __name__ == '__main__':
    def t_shift(l):
        printf("shift(%s)-> ", l);
        r = shift(l);
        printf("%s, %s\n", r, l);

    t_shift([1,2,3]);
    t_shift(['a','b','c','d']);

