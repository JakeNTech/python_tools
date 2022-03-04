# Identify Registry files in a given Directory
import os
import argparse
import subprocess
import re
from datetime import datetime

def get_args():
    parser = argparse.ArgumentParser(description='A simple python script to identify SQLite files that have been carved from a disk')
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
    csv_file.write("filename,size(KB),identified_type,full_table_list\n")
    csv_file.close()
def append_CSV(csv_name,file,identified_type,table_list):
    csv_file = open(csv_name,"a")
    this_line = f"{file},{round(os.path.getsize(file)/1000,2)},{identified_type},{' '.join(table_list)}\n"
    csv_file.write(this_line)
    csv_file.close()

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
    for file_type in file_list.keys():
        # Create Sub Output Directory within output directory
        subprocess.run(["mkdir",f"{output_dir}/{file_type}"])
        for file in file_list[file_type]:
            this_file_name = f"{output_dir}/{file_type}/{file.split('/')[-1]}"
            subprocess.run(["cp",f"{file}",this_file_name])
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
    for file_type in file_list.keys():
        # Create Sub Output Directory within output directory
        subprocess.run(["mkdir",f"{output_dir}/{file_type}"])
        for file in file_list[file_type]:
            this_file_name = f"{output_dir}/{file_type}/{file.split('/')[-1]}"
            subprocess.run(["mv",f"{file}",this_file_name])

def process_files(file_list):
    # Convert file list to Dictionary 
    files_tables = {}
    for index,value in enumerate(file_list):
        files_tables[value] = []
    for file in file_list:
        #this_file_strings = subprocess.run(["strings",file], stdout=subprocess.PIPE).stdout
        #this_head = subprocess.run(["head","-n","50"],stdin=this_file_strings,stdout=subprocess.PIPE).stdout.decode("ascii")
        # https://stackoverflow.com/questions/28154437/using-subprocess-to-get-output-of-grep-piped-through-head-1
        # p1 = Popen(["strings",file],stdout=PIPE)
        # p2 = Popen(["head", "-n","100"], stdin=p1.stdout, stdout=PIPE)
        # p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        # out,err = output = p2.communicate()
        # out = out.decode("ascii").split("\n")
        strings = subprocess.run(["strings",file],stdout=subprocess.PIPE).stdout.decode("ascii").split("\n")
        for line in strings:
            if line[0:12] == "CREATE TABLE":
                #this_tables.append(line)
                try:
                    this_table_name = re.search('CREATE TABLE ([^\s]\w*[^\s])', line).group(1)
                except:
                    this_table_name = ""

                if this_table_name != "":
                    files_tables[file].append(this_table_name.strip("|(|\"").upper())
    return files_tables

# Identify file based on tables found
def identify_file(csv_name,file_tables):
    identify_files = {"Chromium_Cookies":[],"Chromium_History":[],"Chromium_Autofill":[],"MacOS_Download_History":[],"itunesstored_private":[],"Mozilla_History":[],"Safari_History":[],"Unknown":[]}
    for file in file_tables.keys():
        # Chromium related SQLITE files
        if "COOKIES" in file_tables[file]:
            append_CSV(csv_name,file,"Chromium_Cookies",file_tables[file])
            identify_files["Chromium_Cookies"].append(file)
        elif "VISITS" and "URLS" in file_tables[file]:
            append_CSV(csv_name,file,"Chromium_History",file_tables[file])
            identify_files["Chromium_History"].append(file)
        elif "AUTOFILL" and "CREDIT_CARDS" in file_tables[file]:
            append_CSV(csv_name,file,"Chromium_Autofill",file_tables[file])
            identify_files["Chromium_Autofill"].append(file)
        
        # Mac OS X related SQLite files
        elif "LSQUARANTINEEVENT" in file_tables[file]:
            append_CSV(csv_name,file,"MacOS_Download_History",file_tables[file])
            identify_files["MacOS_Download_History"].append(file)
        elif "ZPUSHNOTIFICATIONENVIRONMENT" and "ZPUSHNOTIFICATION" in file_tables[file]:
            append_CSV(csv_name,file,"itunesstored_private",file_tables[file])
            identify_files["itunesstored_private"].append(file)
        
        # Apple Safari related SQLite files
        elif "HISTORY_VISITS" and "HISTORY_ITEMS" in file_tables[file]:
            append_CSV(csv_name,file,"Safari_History",file_tables[file])
            identify_files["Safari_History"].append(file)
        
        # Mozilla Firefox related SQLite files
        elif "MOZ_PLACES" and "MOZ_HISTORYVISITS" in file_tables[file]:
            append_CSV(csv_name,file,"Mozilla_History",file_tables[file])
            identify_files["Mozilla_History"].append(file)
        
        # Everything I don't know what they are ;)        
        else:
            identify_files["Unknown"].append(file)
            append_CSV(csv_name,file,"Unknown",file_tables[file])
        
    return identify_files

if __name__ == "__main__":
    args = get_args()
    #Validate options before running
    if args.copy and args.move:
        print("Intention unclear!\n\nExiting..")
        exit()
    file_list = list_files(args.input_directory)
    now = datetime.now()
    csv_name = f"{now.strftime('%d-%m-%YT%H%M.csv')}"
    create_CSV(csv_name)
    print("Generating CSV...\n")
    file_tables = process_files(file_list)
    file_tables = identify_file(csv_name,file_tables)
    if args.move:
        file_mover(file_tables,args.move)
        print("Files moved into directory structure! CSV Generated!\n\nExiting..")
    elif args.copy:
        file_mover(file_tables,args.copy)
        print("Files copied into directory structure! CSV Generated!\n\nExiting..")
    else:
        print("CSV file Generated!\n\nExiting...")