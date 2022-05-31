# Time Machine Artefact Extractor
Have a Time Machine Backup Drive but want to find and pull artefact? Me too! But I ain't being repetitive, and so I scripted it!
## Notes
-   Designed to run on Linux
-   Run the script from the backup directory , E.G. `media/rubeus/Time_Machine/Backups.backupdb/SiriusBlack-MacBook# python3 /opt/Time_Machine_Artifacts_Extractor.py`
-   Must be run as ROOT due to file permissions on Time Machine Drive
-   File paths for CSV and Target file path will need to be updated to match our system (I could have used command line arguments but this is a quick script for me)
-   artefact_to_extract contains a list of artefact that I wanted to look at when writing the script, you can add more or remove them