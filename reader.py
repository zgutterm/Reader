# Calculate the read speed of Red Hat Training adoc files.
  

import os
import math
import sys
import glob
  
#The average reading speed in words per minute for adults
averageSpeed = 200
#The time to "read" each image in seconds
imageReadTime = 12
#The time it takes to read a code block in seconds
timeToReadCodeBlock = 30
#Path for the file types to check
filetypes = "/*-lecture-content.adoc"

# Function to count number of characters, words, spaces and lines in a file
def counter(fname):
    inCodeBlock = False
    # variable to store total word count
    num_words = 0
      
    # variable to store total line count
    num_lines = 0
      
    # variable to store total character count
    num_charc = 0
      
    # variable to store total space count
    num_spaces = 0

    # variable to store total images
    num_images = 0

    #variable to store total code blocks
    num_codeblocks = 0
      
    with open(fname, 'r') as f:
          
        # iterate by line
        for line in f:
              
            # separating a line from \n character and storing again in line
            line = line.strip(os.linesep)
              
            # split line into word array
            wordslist = line.split()
              
            # count the lines
            num_lines = num_lines + 1

            #Count number of words
            if (len(wordslist)):
                if (wordslist[0].startswith("image::")):
                    # count number of images
                    num_images = num_images + 1
                elif(wordslist[0].startswith("----")):
                    if (inCodeBlock):
                        #End the codeblock and resume counting words 
                        num_codeblocks = num_codeblocks + 1 
                        inCodeBlock = False  
                    else:
                        #First line in code block
                        inCodeBlock = True
                elif ((not wordslist[0].startswith("//")) and (not inCodeBlock)):
                    # add words in this line to total words
                    num_words = num_words + len(wordslist)
        
            num_charc = num_charc + sum(1 for c in line 
                          if c not in (os.linesep, ' '))
              

            num_spaces = num_spaces + sum(1 for s in line 
                                if s in (os.linesep, ' '))
      
    #print file name
    print("--------------------------")
    print("Analysis of " + fname)
    print("--------------------------")
    # printing total word count
    print("Number of words in text file: ", num_words)
      
    # printing total line count
    print("Number of lines in text file: ", num_lines)

    # printing total images
    print("Number of images in text file: ", num_images)

    # printing total codeblocks
    print("Number of code blocks in text file: ", num_codeblocks)
    readLength(num_words, num_images, num_codeblocks)


def readLength(wordCount, imageCount, codeBlockCount):
    # Start with base level word count and average speed
    readingTime = wordCount/averageSpeed 

    #Add time for images, convert seconds to minutes
    imageTime = (imageCount * imageReadTime) / 60

    #add time for code blocks, convert time to minutes
    codeBlockTime = (codeBlockCount * timeToReadCodeBlock) / 60


    readingTime = readingTime+imageTime + codeBlockTime
    print("raw reading time: " + repr(readingTime))
    print("--------------------------")
    print("Add the following beneath the section title:")
    print ("[role='rolehtml']")
    print (repr(math.ceil(readingTime)) + " min read")

def directoryProcess(path):
    print("in directory")
    #verify that there are lecture adoc files present
    fileList = glob.glob(path + filetypes)
    if (len(fileList) <= 0):
        print("No relevant files found in directory")
    else:
        print("Relevant files found: ", len(fileList))
        #iterate through list of adoc files calling counter
        for filename in fileList:
            counter(filename)
    


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("You must include the target path and filename")
        print("Ex. `python3 reader.py /User/zpgutterman/lecture.adoc")
        sys.exit()
    input = sys.argv[1]
    if not os.path.isfile(input) and not os.path.isdir(input):
        print('The file or directory specified does not exist')
        sys.exit()
    try:
        if (os.path.isfile(input)): 
            counter(input)
        elif (os.path.isdir(input)):
            directoryProcess(input)
    except Exception as e: 
        print(e)