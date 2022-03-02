# Identify Registry files in a given Directory
import os
import argparse
import subprocess
import re
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description='A simple python script to identify Windows Registry files that have been carved from a disk')
    parser.add_argument("-d", "--directory", dest="input_directory", help="Directory of files to scan", metavar="<path>",required=True)
    parser.add_argument("-m", "--move", dest="move", help="Move Files into sorted directory structure", metavar="<path>")
    parser.add_argument("-c", "--copy", dest="copy", help="Copy Files into sorted directory structure", metavar="<path>")
    return parser.parse_args()

# List contents of directory
def list_files(directory):
    file_array = [os.path.join(directory, fn) for fn in next(os.walk(directory))[2]]
    return file_array

#CSV Functions
def create_CSV(csv_name):
    csv_file = open(csv_name,"w")
    csv_file.write("filename,size(KB),identified_type,full_area(Strings)\n")
    csv_file.close()
def append_CSV(csv_name,file,identified_type,header):
    csv_file = open(csv_name,"a")
    this_line = f"{file},{round(os.path.getsize(file)/1000,2)},{identified_type},{header}\n"
    csv_file.write(this_line)
    csv_file.close()

# Moves the files into sorted directory structure
def file_mover(file_list,output_dir):
    # Remove any "/" from the end of the destination path, makes dealing with an input that don't have it easier :)
    if output_dir[-1] == "/":
        output_dir = output_dir[:-1]
    # Create Output Directory -> Account for already being created or other error messages (Such as Access denied) ->A bit agressive having to run the script again...something to change?
    create = subprocess.run(["mkdir",output_dir], stderr=subprocess.PIPE).stderr.decode("utf8")
    if len(create) != 0:
         print(create,"\nExiting...")
         exit()
    # Time to move some files
    for reg_file in file_list.keys():
        # Create Sub Output Directory within output directory
        subprocess.run(["mkdir",f"{output_dir}/{reg_file}"])
        if reg_file == "NTUSER":
            for file in file_list[reg_file]:
                # file = "./reg/f7756816.reg::KEITH"
                file = file.split("::")
                # file = ["./reg/f7756816.reg","KEITH"]
                this_file_name = f"{output_dir}/NTUSER/{file[-1]}_{file[0].split('/')[-1]}"
                # this_file_name = "./NTUSER_KEITH_f7756816.reg"
                subprocess.run(["mv",f"{file[0]}",this_file_name])
                #print(["mv",f"{file[0]}",this_file_name])
        else:
            for file in file_list[reg_file]:
                this_file_name = f"{output_dir}/{reg_file}/{file.split('/')[-1]}"
                subprocess.run(["mv",f"{file}",this_file_name])

# If the user want's to copy the files rather then move them
def file_copy(file_list,output_dir):
    # Remove any "/" from the end of the destination path, makes dealing with an input that don't have it easier :)
    if output_dir[-1] == "/":
        output_dir = output_dir[:-1]
    # Create Output Directory -> Account for already being created or other error messages (Such as Access denied) ->A bit agressive having to run the script again...something to change?
    create = subprocess.run(["mkdir",output_dir], stderr=subprocess.PIPE).stderr.decode("utf8")
    if len(create) != 0:
         print(create,"\nExiting...")
         exit()
    # Time to move some files
    for reg_file in file_list.keys():
        # Create Sub Output Directory within output directory
        subprocess.run(["mkdir",f"{output_dir}/{reg_file}"])
        if reg_file == "NTUSER":
            for file in file_list[reg_file]:
                # file = "./reg/f7756816.reg::KEITH"
                file = file.split("::")
                # file = ["./reg/f7756816.reg","KEITH"]
                this_file_name = f"{output_dir}/NTUSER/{file[-1]}_{file[0].split('/')[-1]}"
                # this_file_name = "./NTUSER_KEITH_f7756816.reg"
                subprocess.run(["cp",f"{file[0]}",this_file_name])
                #print(["mv",f"{file[0]}",this_file_name])
        else:
            for file in file_list[reg_file]:
                this_file_name = f"{output_dir}/{reg_file}/{file.split('/')[-1]}"
                subprocess.run(["cp",f"{file}",this_file_name])

# work off file headers
def process_headers(csv_name,file_list):
    identified_files = {"SAM":[],"SECURITY":[],"SYSTEM":[],"SOFTWARE":[],"NTUSER":[],"UsrClass":[],"Amcache":[],"UNKNOWN":[]}
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
        # Issue with headers containing SYSTEM32 being detected as SYSTEM32...soloution: Remove SYSTEM32 and replace with SYS32
        try:
            this_header = this_header.replace("SYSTEM32","SYS32")
        except:
            pass
        # Files written to CSV as well as being added to the array to allow the header to be written to the CSV file too. 
        # The dictionary would end up being huge if it had the header in too with the CSV actions being completely separate. The header is gone once it's been written
        if "SAM" in this_header:
            identified_files["SAM"].append(file)
            append_CSV(csv_name,file,"SAM",this_header)
        
        elif "SECURITY" in this_header:
            identified_files["SECURITY"].append(file)
            append_CSV(csv_name,file,"SECURITY",this_header)
        
        elif "SYSTEM" in this_header:
            identified_files["SYSTEM"].append(file)
            append_CSV(csv_name,file,"SYSTEM",this_header)
        
        elif "SOFTWARE" in this_header:
            identified_files["SOFTWARE"].append(file)
            append_CSV(csv_name,file,"SOFTWARE",this_header)
        
        elif "NTUSER" in this_header:
            # To add the username to the file name for the moving function it can be tagged onto the end.
            # Adding other information from the header for the other types could also work in this way.
            try:
                NTUSER_user = file+"::"+this_header.split('\\')[-2]
            except:
                NTUSER_user = file+"::Unknown_User"
            identified_files["NTUSER"].append(NTUSER_user)
            append_CSV(csv_name,file,"NTUSER",this_header)
        
        elif "USRCLASS.DAT" in this_header:
            identified_files["UsrClass"].append(file)
            append_CSV(csv_name,file,"UsrClass",this_header)
        
        elif "AMCACHE" in this_header:
            identified_files["Amcache"].append(file)
            append_CSV(csv_name,file,"Amcache",this_header)
       
        else:
            identified_files["UNKNOWN"].append(file)
            append_CSV(csv_name,file,"UNKNOWN",this_header)
            #identified_files[file] = this_header
        # Return array of files that are unidentified
    return identified_files

if __name__ == "__main__":
    args = get_args()
    # Validate options before running
    if args.copy and args.move:
        print("Intention unclear!\n\nExiting..")
        exit()
    file_list = list_files(args.input_directory)
    now = datetime.now()
    csv_name = f"{now.strftime('%d-%m-%YT%H-%M.csv')}"
    create_CSV(csv_name)
    identified_files = process_headers(csv_name,file_list)
    #identified_files = {"SAM":["test.1","test.2"],"SECURITY":["test.3"],"SYSTEM":[],"SOFTWARE":["test.4"],"NTUSER":["test5.reg::Keith"],"UsrClass":[],"Amcache":[],"UNKNOWN":[]}
    if args.move:
        file_mover(identified_files,args.move)
        print("Files moved into directory structure! CSV Generated!\n\nExiting..")
    elif args.copy:
        file_mover(identified_files,args.copy)
        print("Files copied into directory structure! CSV Generated!\n\nExiting..")
    else:
        print("CSV file Generated!\n\nExiting...")