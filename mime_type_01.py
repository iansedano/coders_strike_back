import sys
import math

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.

mime = []
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    mime.append([ext.lower(), mt])


def get_mime(file_name):
    file_name = file_name.lower()
    
    for n in mime:
        str_to_find = f".{n[0]}"
        found = file_name.rfind(str_to_find)
        if found > -1:
            mime_len = len(n[0])
            if found + 1 + mime_len < len(file_name):
                return "UNKNOWN"
            return n[1]
    return "UNKNOWN"


for i in range(q):
    fname = input()
    print(get_mime(fname))