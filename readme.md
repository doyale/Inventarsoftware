# InvSoft V0.9-beta Manual
## General
**NOTE: This piece of software is not yet in a fully functional state. Most core features exist and work, but some bugs may still be present. Data loss should not occur but I cannot guarantee anything at this point in time. Also I am a chemist, not a programmer; Feel free to provide constructive criticism but please don't just complain about bad code.**
### Introduction
InvSoft is a Python/TKInter based UI for inventory management and electronic note taking in a chemistry laboratory setting. While it may not have all features other ELNs and lab management programs come with, it is geared towards making life easier for small operations and hobbyists.

### Installation
In principle, this program is portable and can be run on any Windows machine capable of running Python 3.10 (a distribution with all required dependencies comes with the software so Python does not have to be installed separately). It is best to install the program in a computer linked cloud service (such as OneDrive or Mega, both of which have adequate free plans available). This allows for operation of one instance on different computers, and ensures that all data is backed up appropriately without adding unnecessary subscription models or compromising data safety.
If you are setting up the software for the first time, follow these steps:
1. Download the latest release - a self extracting executable archive - and move it to the desired install directory.
2. Run the program. It will prompt you to confirm the extraction directory -> click "Extract"
3. A Folder with the Name and version number of the software will appear. Navigate to this directory and locate "run.exe". You can either start the program directly by using this file, or you can create a link. Additionally, if you have been using an older Version of the software before, you will have to copy any data to the new version:
4. Navigate to the old install and copy the "ELN" folder including contents to the new install. If no such folder exists you can skip this step.
5. Navigate to the "dist" folder in the old install and copy "chem_db.xml" to the "dist" folder in the new location (you may need to overwrite an already existing file in the new version)
6. Verify that all data is present before deleting or archiving the old version.

## Inventory Management

## Electronic Lab Notebook (ELN)
**This feature is inactive development, but it is not yet available.**
![Screenshot of the ELN development build](https://imgur.com/dGNuBwq)