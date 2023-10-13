import markdown as md
import os
import logging
import re
import shutil
import time

vault = "/home/josh/projects/testVault/testVault"
attachments = "_attachments"
templates = "_templates"
vaultAttachments = vault+"/"+attachments
htmlDestination = "/home/josh/projects/testSite"
backupFolder = "/home/josh/projects/testSiteBackup"

typeExtensionPattern = r'.*\.(md|png|jpg)$'
markdownExtension = r'.*\.md$'
publishPattern = r'---\npublish: "true"\n---'

shutil.rmtree(htmlDestination)
"""# --- BACKUP HANDLING ---
# check whether a backup folder exists at the specified location
# if it exists, remove it and make a new one
if os.path.exists(backupFolder):
    shutil.rmtree(backupFolder)
# if it doesn't exist, create one
else:
    os.mkdir(backupFolder)

# check whether anything exists at the html destination
# if so, copy contents over to backupFolder and delete it, then create the folder
if os.path.exists(htmlDestination):
    shutil.copytree(htmlDestination, backupFolder)
    shutil.rmtree(htmlDestination)
    os.mkdir(htmlDestination)
# if not, make the folder
else:
    os.mkdir(htmlDestination)"""

# --- Copy over stuff ---
# create attachments folder in html and copy vault attachments over
if not os.path.exists(htmlDestination):
    print("html directory does not exist, creating...")
    os.mkdir(htmlDestination)
    if not os.path.exists(f"{htmlDestination}/attachments"):
        print("creating attachments folder...")
        os.mkdir(f"{htmlDestination}/attachments")


for item in os.listdir(vaultAttachments):
    print(f"copying {item}...")
    shutil.copy(f"{vaultAttachments}/{item}",f"{htmlDestination}/attachments")

for item in os.listdir(vault):
    if item == ".obsidian":
        print(f"found {item}, ignoring...")
    elif item == templates:
        print(f"found {item}, ignoring...")
    elif item == attachments:
        print(f"found {item}, ignoring...")
    elif re.match(markdownExtension,item):
        shutil.copy(f"{vault}/{item}",htmlDestination)
    else:
        shutil.copytree(f"{vault}/{item}",f"{htmlDestination}/{item}")

def checkPublish(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    #print(f"Contents of {file_path}:\n{file_contents}")
    if re.match(publishPattern,file_contents):
        return True
    else:
        return False

def toHtml(filename):
    with open(filename, "r") as file:
        text = file.read()
        html = md.markdown(text)
    with open(filename[:-3]+".html","w") as file:
        file.write(html)

def processMarkdownFiles(root_folder, markdownExtension):
    for folder, subfolders, files in os.walk(root_folder):
        for item in files:
            if re.match(markdownExtension, item):
                print(f"found markdown file at {folder}/{item}, Checking publication status...")
                if not checkPublish(f"{folder}/{item}"):
                    print(f"{item} is not marked for publish, deleting...")
                    os.remove(f"{folder}/{item}")
                else:
                    print(f"{item} is marked for publishing! converting to html...")
                    toHtml(f"{folder}/{item}")
                    print("conversion successful!")



processMarkdownFiles(htmlDestination,markdownExtension)