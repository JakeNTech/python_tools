import argparse
import os
import hashlib
from tabnanny import check
from virus_total_apis import PublicApi as VirusTotalPublicApi
import json
import time


# Get command line arguments
def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", dest="input_directory", help="Directory of files to hash and scan", metavar="<path>",required=True)
    parser.add_argument("-k", "--key", dest="api_key", help="api_key", metavar="<key>",required=True)
    parser.add_argument("-p", "--pass", dest="known_hashes", help="Text file containing known hashes, hashes for files NOT to be scanned on Virus Total", metavar="<key>")
    parser.add_argument("-o", "--output", dest="output_location", help="Place to save the CSV file of results. Default: ./output.csv", metavar="<filename>", default="./output.csv")
    return parser.parse_args()

# List contents of directory
def list_files(directory):
    file_array = [os.path.join(directory, fn) for fn in next(os.walk(directory))[2]]
    return file_array

# Calculate the hash for a given file
def hash_item(file):
    calculated_hash = ""
    hash = hashlib.sha256()
    with open(file, 'rb') as file:
        buffer = file.read()
        hash.update(buffer)
    calculated_hash =  hash.hexdigest()
    return calculated_hash

#Create File hash 2D array
def hash_array(directory_listing):
    hashed_array = []
    for file in directory_listing:
            this_hash = [file,hash_item(file)]
            hashed_array.append(this_hash)
    return hashed_array

# Take in file hash and check on Virus Total
def check_VT(file_hash):
    responce = virustotal.get_file_report(file_hash)
    responce = json.loads(json.dumps(responce))
    
    #https://github.com/drew-kun/virustotal-api-hashcheck/blob/master/virustotal.py
    if responce['results']['response_code'] == 1 and "Fortinet" in responce['results']['scans']:
        if responce['results']['scans']['Fortinet']['result'] == None:
            # If file is on Virus Total but doesn't contain a threat name
            VT_results = ["--", str(responce['results']['positives'])]
        else:
            # If file does contain a threat name
            VT_results = [responce['results']['scans']['Fortinet']['result'],str(responce['results']['positives'])]
    # File isn't on VT
    else:
        VT_results = ["File not on Virus Total","0"]
    return VT_results
    
# Create CSV file for results
def CSV_Maker(results,path):
    CSV_out = open(path,"w")
    CSV_out.write("ID,File_Path,SHA256_Hash,VT_Detection_Name(Fortinet),True_Positive_Detections\n")
    ticker = 0
    for file in results:
        ticker = ticker + 1
        CSV_out.write(str(ticker)+",")
        for item in file:
            CSV_out.write(item+",")
        CSV_out.write("\n")

if __name__ == "__main__":
    arguments = arguments()
    
    #Get file list and hashes
    directory_listing = list_files(arguments.input_directory)
    hashed_array = hash_array(directory_listing)
    
    #Sample Array
    #hashed_array = [["./eicar.txt","275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"],["./totally_legit_file.exe","f2f03b4d660d6c9ea2aa67e9be35f6ab4c4e5daf9673622b645e29fb85c7faf4"]]
    
    global virustotal
    virustotal = VirusTotalPublicApi(arguments.api_key)
    # If a known hash list is provided
    if arguments.known_hashes:
        known_hashes = open(arguments.known_hashes,"r").read().split("\n")
    else:
        known_hashes = []

    for file in hashed_array:
        if file[1] in known_hashes:
            file.append("In known list. Skipped")
            file.append("0")
        else:
            results = check_VT(file[1])
            file.append(results[0])
            file.append(results[1])
        # To keep within API usage
        time.sleep(16)
    #print(hashed_array)
    CSV_Maker(hashed_array,arguments.output_location)