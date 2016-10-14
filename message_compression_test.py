#!/usr/bin/python3

'''
bc@d:~/p/waves/waves_random$ ./message_compression_test.py 
Length: 179
Compressed LZMA: 163
Time taken: 0.11610984802246094 ms
Decompressed correctly: True
Compressed ZLIB: 158
Time taken: 0.016689300537109375 ms
Decompressed correctly: True

I've decided that it's not worth to bloat the code only to save 10% of space.
'''

#msg = b'{"glossary":{"title":"example glossary","GlossDiv":{"title":"S","GlossList":{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"Standard Generalized Markup Language","Acronym":"SGML","Abbrev":"ISO 8879:1986","GlossDef":{"para":"A meta-markup language, used to create markup languages such as DocBook.","GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}'
msg = b'{"markers":[{"point":newGLatLng(40.266044,-74.718479),"homeTeam":"Lawrence Library","markerImage":"images/red.png","fixture":"Wednesday 7pm","capacity":"","previousScore":""},,] }'
#msg = b'/\x91\x02\xea\xe1qZPD\x05\x97\xf1r\xdcN\xc6\xd0!\xe5\xddQQ\xe4Rg\xc0\xcb\xe0[I\xa8\xeb\xb9SN\xd2$X5\x7f\x9e\x81\x85(\x7f\xfc\x81n\xc5\xec\xd5.\xc3\x1dX@\xcf\x9b4\x85A\xbb\x9a\xd7\xf4\x8c\xf5\xb8S{\x9b\xf2\xbc\xa5[\xd6\xd3\xae\x0fW!\xe0g\xf8\xdf\xee\x07\'f|\'\x11e\x85\x12\x9b\xe5\xc8\x00\x85`]U\xb9>T\x91jZ\n/\xc6dn\xe0\xb4\x17"V3\xf4v\xcd\x17K%\xec\xc4' # Random data
print("Length:", len(msg))

import lzma

comp = lzma.compress(msg, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=[{"id": lzma.FILTER_LZMA2, "preset": 9 | lzma.PRESET_EXTREME}])

print("Compressed LZMA:", len(comp))

import time
start = time.time()
dec = lzma.decompress(comp, format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME}])
end = time.time()
print("Time taken:", (end - start) * 1000, "ms")

print("Decompressed correctly:", dec == msg)


import zlib

comp = zlib.compress(msg)

print("Compressed ZLIB:", len(comp))

start = time.time()
dec = zlib.decompress(comp)
end = time.time()
print("Time taken:", (end - start) * 1000, "ms")

print("Decompressed correctly:", dec == msg)

