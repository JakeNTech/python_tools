#!/usr/bin/env python3
'''
DFF_Evidence_Finder
JakeNTech
09-10-2020
'''
import os
import time
import random
#Make the files needed to run the script
def file_maker():
    os.system("mkdir found_data")
    os.system("mkdir AUX_files")
    os.system("mkdir ./found_data/html_source_code")
    os.system("mkdir ./found_data/exif")
    os.system("mkdir ./found_data/file_extention_mismatch")
    os.system("find ./case_data -type f -exec file -- {} + > ./AUX_files/file_types")
    time.sleep(2)
    os.system("exiftool ./case_data/* -r > ./AUX_files/exif_data")
    time.sleep(2)
def file_type():
    # Identify File Type mismatch
    # Binwalk would be better but that's omega brain
    filepath = './AUX_files/file_types'
    file_to_write_too = open("./found_data/file_extention_mismatch/mismatch","w")
    with open(filepath) as fp:
        line = fp.readline()
        for line in fp:
            line = fp.readline().split(":")
            og_file_path = line[0]
            #print(line[1])
            detected_file_type = line[1].lower().strip().split()[0]
            #print(line[1].lower().strip().split())
            #print(detected_file_type)
            file_type_dict = {"docx":"microsoft","enc":"openssl","dos/mbr":"dd","mp3":"audio","class":"java"}
            mod_file_path = og_file_path.split("/")
            mod_file_path = mod_file_path[len(mod_file_path)-1]
            mod_file_path = mod_file_path.split(".")
            extention = mod_file_path[len(mod_file_path)-1]
            if extention == "jpg" and detected_file_type != "gif":
                extention = "jpeg"
            if extention in file_type_dict:
                extention = file_type_dict[extention]
            if extention != detected_file_type:
                mis_match = "Oh No! File Extention Mismath Detected! " + og_file_path + " The extention should be: " + detected_file_type + "\n"
                #print(mis_match.strip("\n"))
                file_to_write_too.write(mis_match)
    fp.close()
    file_to_write_too.close()
# Find data hidden in exif information
def big_ctrl_f_exif():
    fp = open("./AUX_files/exif_data","r")
    f = fp.read().split("========")
    fp.close()
    file_to_write_too = open("./found_data/exif/found_exif","w")
    for i in range(0,len(f)-1):
        this_file = f[i]
        this_file = this_file.split("\n")
        filepath = str(this_file[0].replace(" ",""))
        for x in range(0,len(this_file)-1):
            string = str(this_file[x].replace(" ",""))
            if "Event" in string or "event" in string:
                string = "Secrete Event Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
                break
            elif "Target" in string:
                string = "Secrete Target Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Key" in string:
                string = "Secrete Key Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Cipher" in string:
                string = "Secrete Cipher Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Lsb" in string:
                string = "Secrete Lsb Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Separator" in string:
                string = "Secrete Separator Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Confession" in string:
                string = "Secrete confession Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Meeting" in string:
                string = "Meeting information Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "Team" in string: #https://tenor.com/view/it-crowd-team-denholm-reynholm-team-team-team-it-crowd-gif-14763596
                string = "Team infromation Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "==" in string:
                string = "B64 Encoded data Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
            elif "4576656e74" in string:
                string = "Hex encoded data Found!"+string+"Found in file: "+filepath+"\n"
                file_to_write_too.write(string)
    file_to_write_too.close()
#HTML Comments
def html_content():
    print("HTML Comments")
    os.system("grep -r '<!--.*-->' ./case_data  | tee ./found_data/html_source_code/html_coments")
    print("------------------------------")
    print("Meta comments")
    os.system("grep -r '<meta' ./case_data | tee ./found_data/html_source_code/html_meta")
    print("------------------------------")
    print("CDATA")
    os.system("grep -r 'CDATA' ./case_data  | tee ./found_data/html_source_code/CDATA")
    print("------------------------------")
    print("MD5 Hashes")
    os.system("grep -r 'MD5=' ./case_data | tee ./found_data/html_source_code/MD5")
    print("------------------------------")
    print("Hex Decode data")
    os.system("grep -r '4576656e' ./case_data  | tee ./found_data/html_source_code/Hex")
# WE NEED KEVIN RIPA QUOTES
def kevin_ator():
    kevin_quotes=["The Google",
    "You will never work again",
    "You’ll go to prison",
    "Mr Ripa did a virus do this?",
    "Rather pull a wet noodle then push one",
    "Like my fist in a bucket of water",
    "Liar liar pants on fire",
    "Your case will take a nosedive",
    "But its off but its on but its off but its on",
    "When it isn’t it is and it is it isn’t",
    "The data does not lie",
    "This is how we fight and this is how we win",
    "Balderdash",
    "A case I worked on one",
    "Integrity",
    "To a high degree of professional certainty",
    "Always never say never",
    "Your gonna kick their butts",
    "It’s not made for your forensicating pleasure",
    "Evil can run but it must hide",
    "You drank the cool aid but it was posion",
    "It’s like being hit on the back of a head with a frozen squirrel",
    "Ill rip the wires straight outta their horn",
    "Drinking from a fire hoze"]
    files = ["./found_data/exif/found_exif","./found_data/file_extention_mismatch/mismatch","./found_data/html_source_code/CDATA","./found_data/html_source_code/Hex","./found_data/html_source_code/html_coments","./found_data/html_source_code/html_meta","./found_data/html_source_code/MD5"]
    for i in range(0,28):
        file_to_open = random.randint(0, len(files)-1)
        file_to_open = files[file_to_open]
        random_kevin_quote = random.randint(0,len(kevin_quotes)-1)
        random_kevin_quote = kevin_quotes[random_kevin_quote]
        command = "echo '"+random_kevin_quote+"' >> '"+file_to_open+"'"
        os.system(command)
if __name__ == "__main__":
    print("DFF Evidence Finder!")
    print("JakeNTech\n")
    print("This might not be accurate!")
    print("Use at your own peril!")
    print("Its advised you check anything found by this script then taking its word as gosbel")
    print("Like with any forensics tool!")
    print("---------------------------------")
    print("Creating needed AUX files...\n")
    file_maker()
    print("File Mismatch detector!\n")
    file_type()
    print("---------------------------------")
    print("Exif finder\n")
    big_ctrl_f_exif()
    print("HTML data...this will get messy")
    html_content()
    print("---------------------------------")
    print("Time to add some Keivn Ripa Quotes!")
    kevin_ator()
    print("---------------------------------")