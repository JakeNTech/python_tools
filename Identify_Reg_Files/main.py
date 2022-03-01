# Identify Registary files in a given Directory
import os
import argparse
import subprocess
import re

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", dest="input_directory", help="Directory of files to scan", metavar="<path>",required=True)
    #parser.add_argument("-r", "--rename", dest="rename", help="Rename Files after identification", metavar="<key>",default="0")
    parser.add_argument("-o", "--output", dest="output_location", help="Place to save the CSV file of results. Default: ./output.csv", metavar="<filename>", default="./output.csv")
    return parser.parse_args()

# List contents of directory
def list_files(directory):
    file_array = [os.path.join(directory, fn) for fn in next(os.walk(directory))[2]]
    return file_array
# work off file headers
def process_headers(file_list):
    unkonwn_files = {}
    for file in file_list:
        #xxd -p -l 200 SOFTWARE.reg -> OLD
        # hexdump ./SOFTWARE.reg -n 100 -s 10
        # https://github.com/libyal/libregf/blob/main/documentation/Windows%20NT%20Registry%20File%20(REGF)%20format.asciidoc
        # Area that may contain file name is 64 bytes long and will always start at offset 0d48 or 0x30
        this_hex = subprocess.run(["hexdump","-n","64","-s","48",file], stdout=subprocess.PIPE).stdout.decode("ascii")
        #this_hex = get_header(file).decode("ascii") -> Running this was put out to it's own function
        this_hex = re.split(" |\n",this_hex)
        this_header = []
        for nibble in this_hex:
            if len(nibble) == 4 and nibble != "0000":
                if nibble[0:2] != "00":
                    this_header.append(bytearray.fromhex(nibble[0:2]).decode())
                if nibble[2:4] != "00":
                    this_header.append(bytearray.fromhex(nibble[2:4]).decode())
                #print(this_header)90000004pppppppppp - The cat sat on the keybord here
                #this_hex.pop(this_hex.index(nibble))
        this_header = "".join(this_header).upper()
        if "SAM" in this_header:
            append_CSV(args.output_location,file,"SAM",this_header)
        elif "SECURITY" in this_header:
            append_CSV(args.output_location,file,"SECURITY",this_header)
        elif "SYSTEM" in this_header:
            append_CSV(args.output_location,file,"SYSTEM",this_header)
        elif "SOFTWARE" in this_header:
            append_CSV(args.output_location,file,"SOFTWARE",this_header)
        elif "NTUSER" in this_header:
            append_CSV(args.output_location,file,"NTUSER",this_header)
        elif "USRCLASS.DAT" in this_header:
            append_CSV(args.output_location,file,"UsrClass",this_header)
        elif "AMCACHE" in this_header:
            append_CSV(args.output_location,file,"Amcache",this_header)
        else:
            append_CSV(args.output_location,file,"UNKNOWN",this_header)
            #unkonwn_files[file] = this_header
        # Return array of files that are unidentified
    return unkonwn_files
#CSV Functions
def create_CSV(name):
    csv_file = open(name,"w")
    csv_file.write("filename,size(KB),identified_type,full_area(Strings)\n")
    csv_file.close()
def append_CSV(name,file_name,identified_type,full_area):
    csv_file = open(name,"a")
    this_line = f"{file_name},{round(os.path.getsize(file_name)/1000,2)},{identified_type},{full_area}\n"
    csv_file.write(this_line)
    csv_file.close()

if __name__ == "__main__":
    args = get_args()
    file_list = list_files(args.input_directory)
    create_CSV(args.output_location)
    unknown_files = process_headers(file_list)
    # print(unknown_files)