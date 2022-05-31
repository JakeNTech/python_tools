import os
import subprocess
import hashlib
import csv

def find_artefact(artefact):
	find_results = subprocess.run(["find","./","-name",artefact],stdout=subprocess.PIPE).stdout.decode("ascii").split("\n")

	return find_results

def hash_item(file):
	calculated_hash = ""
	hash = hashlib.sha256()
	with open(file, 'rb') as file:
		buffer = file.read()
		hash.update(buffer)
	calculated_hash =  hash.hexdigest()
	return calculated_hash

def copy_file(file):
	target_path = f"/home/rubeus/Desktop/Mac_OS_Artefacts/{file.split('/')[1]}_{file.split('/')[-1]}"
	#print(target_path)
	subprocess.run(["cp",file,target_path])
	subprocess.run(["chmod","+rwx",target_path])

def create_csv():
	csv_file = open("/home/rubeus/Desktop/Mac_OS_Artefacts/Time_Machine_Artefacts.csv","w")
	csv_file.write("artefact,filename,size(KB),BackupDate,BackupTime,sha256\n")
	csv_file.close()

def append_csv(csv_line):
	with open("/home/rubeus/Desktop/Mac_OS_Artefacts/Time_Machine_Artefacts.csv", 'a', newline='\n', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(csv_line)

if __name__ == "__main__":
	create_csv()

	artefact_to_extract = ["History.db","SystemVersion.plist","com.apple.airport.preferences.plist","com.apple.recentitems.plist","com.apple.loginitems.plist","com.apple.sidebarlists.plist"]

	for artefact in artefact_to_extract:
		artefact_file_list=find_artefact(artefact)
		hashed_items = {}
		for artefact_file in artefact_file_list:
			if artefact_file != "":
				hashed_items[artefact_file] = hash_item(artefact_file)

		# Remove Duplicate files based on Hash
		# https://stackoverflow.com/questions/8749158/removing-duplicates-from-dictionary
		hashed_items_no_duplicates = {}
		for key,value in hashed_items.items():
			if value not in hashed_items_no_duplicates.values():
				hashed_items_no_duplicates[key] = value

		# Copy out files
		for file in hashed_items_no_duplicates:
			copy_file(file)
			# format Date and Time to look good
			date = '-'.join(file.split("/")[1].split('-')[0:3])
			time = file.split("/")[1].split('-')[3]
			time = ':'.join([time[i:i+2] for i in range(0, len(time), 2)])
			
			append_csv([artefact,file,round(os.path.getsize(file)/1000,2),date,time,hashed_items_no_duplicates[file]])
