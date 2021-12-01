# Calculate reading time for all courses in directory
# Helpful for tuning read speed
  

import os
import math
import sys
import glob

from configparser import ConfigParser

import oyaml as yaml

##### These are pulled from config.ini #####

#The average reading speed in words per minute for adults
lecture_read_speed = 0
ge_read_speed = 0
#The time to "read" each image in seconds
image_read_time = 0
#The time it takes to read a code block in seconds
code_block_read_time = 0

#############################################

#Path for the file types to check
adoc_pattern = "/*-lecture*.adoc"
# Relative path to DCO YAML
yaml_path = "/dco/dco.yml"

def get_dco_yaml(dir_path):
    topic_list = []
    filepath = dir_path + yaml_path
    if os.path.isfile(filepath):
        with open(filepath, 'r') as stream:
            yaml_obj = yaml.safe_load(stream)
            chapters = yaml_obj['chapters']
            for chapter in chapters:
                topic_list.append(chapter['chapter_word'])
    return topic_list

# Function to count number of characters, words, spaces and lines in a file
def counter(fname, topic, topic_time):
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

    time = readLength(num_words, num_images, num_codeblocks)

    # get topic name to use for aggregation
    path, file = os.path.split(fname)
    new_topic = os.path.split(path)[1]

    topic_time += time

    return topic_time

def readLength(lecture_word_count, ge_word_count, image_count, code_block_count):
    # Start with base level word count and average speed
    total_lecture_time = lecture_word_count/lecture_read_speed
    total_ge_time = ge_word_count/ge_read_speed

    #Add time for images, convert seconds to minutes
    total_image_time = (image_count * image_read_time) / 60

    #add time for code blocks, convert time to minutes
    total_code_block_time = (code_block_count * code_block_read_time) / 60

    return total_lecture_time + total_ge_time + total_image_time + total_code_block_time

def directoryProcess(path):

    # Go through each course dir (and only course dir)
    dir_path_arr = glob.glob(path+'*/', recursive=False)
    course_dir_paths = [i for i in dir_path_arr if 'Reader' not in i]
    for path in course_dir_paths:

        #verify that there are lecture adoc files present
        #filePath = path+'**/topics/**'+adoc_pattern

        #fileList = glob.glob(filePath, recursive=True)

        topic_names = get_dco_yaml(path)

        
        course_dir = os.path.basename(os.path.dirname(path))

        if (len(topic_names) <= 0):
            print("\n"+course_dir+"\nNo relevant files found"+"\n")
        else:
            print(course_dir)


            # iterate through topic names, in order
            # TODO: as comprehension?
            for topic_name in topic_names:
                # find correct topic
                topic_path = path+'**/topics/'+topic_name+adoc_pattern
                filelist_by_topic = glob.glob(topic_path, recursive=True)

                topic_time = 0

                #iterate through list of adoc files calling counter
                for filename in filelist_by_topic:
                    topic_time = counter(filename, topic_name, topic_time)

                # dump the total topic time for topic
                print(topic_name+"\t"+str((math.ceil(topic_time/5))*5))


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("You must include the target path and filename")
        print("Ex. `python3 reader.py /User/zpgutterman/lecture.adoc")
        sys.exit()

    file_input = sys.argv[1]
    if not os.path.isfile(file_input):
        #print("No file located, checking for directory...")
        if not os.path.isdir(file_input):
            print("Cannot find directory "+file_input)
            sys.exit()

    config = ConfigParser()
    config.read('./config.ini')

    settings = config['READER SETTINGS']
    lecture_read_speed = int(settings['lecture_read_speed'])
    ge_read_speed = int(settings['ge_read_speed'])
    image_read_time = int(settings['image_read_time'])
    code_block_read_time = int(settings['code_block_read_time'])

    try:
        if (os.path.isfile(file_input)): 
            counter(file_input, "unknown topic", 0)
        elif (os.path.isdir(file_input)):
            directoryProcess(file_input)
    except Exception as e: 
        print(e)
