import sys
import math

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.

mimes = []
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    mimes.append([ext.lower(), mt])


def match_ext(mime_entry, file_name):
    str_to_find = f".{mime_entry[0]}"
    found = file_name.rfind(str_to_find)

    if found > -1:
        mime_len = len(mime_entry[0])
        if found + 1 + mime_len < len(file_name):
            return False
        return True

    return False


def fname_to_mime(fnamex):
    mime = list(filter(lambda m: match_ext(m, fnamex), mimes))
    #print(mime, file=sys.stderr)
    if not mime:
        return "UNKNOWN"
    else:
        return mime[0][1]


fnames = []
for i in range(q):
    fname = input()
    fname = fname.lower()
    fnames.append(fname)


mimes = list(map(lambda fnm: fname_to_mime(fnm), fnames))

for i in range(q):
    print(mimes[i])
