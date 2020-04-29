import sys
import math

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.

mime_dict = {}

for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    mime_dict[ext.lower()] = mt


def fname_to_mime(fnamex):
    if fname[-1] == ".":
        return "UNKNOWN"

    index_of_dot = fnamex.rfind(".")

    if index_of_dot == -1:
        return "UNKNOWN"
    else:
        ext = fnamex[fnamex.rfind(".") + 1:]

    if ext in mime_dict:
        return mime_dict[ext]
    else:
        return "UNKNOWN"


for i in range(q):
    fname = input()
    fname = fname.lower()
    print(fname_to_mime(fname))
