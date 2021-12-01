# Calculate the read speed of Red Hat Training adoc files.
  

import os
import math
import sys
import glob

# Average reading speeds in words per minute
lecture_read_speed = 120
ge_read_speed = 60

# Average time per element in seconds (independent of length)
image_read_time = 12
code_block_read_time = 20

#Path for the file types to check
adoc_pattern = "/*-lecture*.adoc"

# Count number of characters, words, spaces and lines in a file

def counter(fname):
    in_code_block = False
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
                    if (in_code_block):
                        #End the codeblock and resume counting words 
                        num_codeblocks = num_codeblocks + 1 
                        in_code_block = False  
                    else:
                        #First line in code block
                        in_code_block = True
                elif ((not wordslist[0].startswith("//")) and (not in_code_block)):
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


def readLength(lecture_word_count, ge_word_count, image_count, code_block_count):
    # Lecture
    total_lecture_time = lecture_word_count/lecture_read_speed
    # GE
    total_ge_time = ge_word_count/ge_read_speed  
    # Images
    total_image_time = (image_count * image_read_time) / 60
    # Code Blocks
    total_code_block_time = (code_block_count * code_block_read_time) / 60
    # Total
    total_time = total_lecture_time + total_ge_time + \
        total_image_time + total_code_block_time
    # Round to nearest 5 minutes (this is not meant to be precise)
    time_estimate = (math.ceil(total_time/5))*5

    print("raw reading time: " + repr(total_time))
    print("--------------------------")
    print("Add the following beneath the section title:")
    print ("[role='rolehtml']")
    print("Approx. " + str(time_estimate) + " minutes")

def directoryProcess(path):
    print("in directory")
    #verify that there are lecture adoc files present
    file_list = glob.glob(path + adoc_pattern)
    
    if (len(file_list) <= 0):
        print("No relevant files found in directory")
    else:
        print("Relevant files found: ", len(file_list))
        #iterate through list of adoc files calling counter
        for filename in file_list:
            counter(filename)
    


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("You must include the target path and filename")
        print("Ex. `python3 reader.py /User/zpgutterman/lecture.adoc")
        sys.exit()
    # if filename is included
    file_input = sys.argv[1]

    if not os.path.isfile(file_input):
        #print("No file located, checking for directory...")
        if not os.path.isdir(file_input):
            print("Cannot find directory "+file_input)
            sys.exit()
    try:
        if (os.path.isfile(file_input)):
            counter(file_input)
        elif (os.path.isdir(file_input)):
            directoryProcess(file_input)
    except Exception as e: 
        print(e)