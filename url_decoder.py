import urllib.parse

reader_file = open("./links.csv","r").read().split("\n")
writer_file = open("./decoded.txt","w")

for i in range(0,len(reader_file)):
    writer_file.write(urllib.parse.unquote(reader_file[i])+"\n")

writer_file.close()