from bs4 import BeautifulSoup
from markdown import markdown
import re
import os

mdFolderPath = "/Users/cburh/Documents/Assignments_Fall2023/Senior Project/polarisDocumentation/docs/polaris/compiling-and-linking/"
txtFilePath = "/Users/cburh/Documents/Assignments_Fall2023/Senior Project/polarisDocs-txt/MainFile.txt"
def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(string=True))

    return text

def readMD_writeTXT(fileToReadPath,fileToWritePath):
    
    with open(fileToReadPath, 'r') as file:
        for line in file:
            
            # Process each line here
            with open(fileToWritePath, 'a') as f:
                #f.write("\n")
                f.write(markdown_to_text(line))
                f.close()


docFolders = os.listdir(mdFolderPath)
def writeAllMdToTxt(directory, txtFileToWrite):
        folders = os.listdir(directory)
        for file in folders:
             with open(txtFileToWrite, 'a') as f:
                f.write("\n\n ###########  " + file + "  ###########\n\n")
                f.close()
             md = file[-3:]
             if (md != ".md"):
                  continue
             readMD_writeTXT(directory + file, txtFileToWrite)
            

            
writeAllMdToTxt(mdFolderPath, txtFilePath)
