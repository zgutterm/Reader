# Calculate the read speed of Red Hat Training adoc files.
  

import os
import math
import sys
import glob

from configparser import ConfigParser

import oyaml as yaml


#Path for the file types to check
adoc_pattern = "*.adoc"
lecture_pattern = "lecture"
ge_pattern = "-ge"
practice_pattern = "-practice"
mc_pattern = "-mc"
quiz_pattern = "-quiz"
# Relative path to DCO YAML
yaml_path = "/dco/dco.yml"

# given path to YAML file, returns ordered list of tuples, e.g. ("topic", ("section1", "section2", ...])
def get_dco_yaml(dir_path):
    topic_list = []
    filepath = dir_path + yaml_path
    if os.path.isfile(filepath):
        with open(filepath, 'r') as stream:
            yaml_obj = yaml.safe_load(stream)
            chapters = yaml_obj['chapters']
            for chapter in chapters:
                if chapter['section_files']:
                    sections = tuple([section.split('.')[0].lower() for section in chapter['section_files']])
                else:
                    sections = ()
                chapter_topic_sections = (chapter['chapter_word'], sections)
                topic_list.append(chapter_topic_sections)

    return topic_list 

# Function to count number of characters, words, spaces and lines in a file
def counter(fname, topic, read_speed):
    inCodeBlock = False
    # variable to store total word count
    num_words = 0
      
    # variable to store total line count
    num_lines = 0
      
    # variable to store total character count
    # num_charc = 0
      
    # variable to store total space count
    # num_spaces = 0

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
            # num_lines = num_lines + 1

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
        
            # num_charc = num_charc + sum(1 for c in line 
            #               if c not in (os.linesep, ' '))
              

            # num_spaces = num_spaces + sum(1 for s in line 
            #                     if s in (os.linesep, ' '))

    time = read_length(num_words, num_images, num_codeblocks, read_speed)

    return time

def read_length(word_count, image_count, code_block_count, read_speed):
    # Start with base level word count and average speed
    total_read_time = word_count/read_speed

    #Add time for images, convert seconds to minutes
    total_image_time = (image_count * image_read_time) / 60

    #add time for code blocks, convert time to minutes
    total_code_block_time = (code_block_count * code_block_read_time) / 60

    return total_read_time + total_image_time + total_code_block_time

def directory_process(path):

    # Go through each course dir (and only course dir)
    dir_path_arr = glob.glob(path+'*/', recursive=False)
    course_dir_paths = [i for i in dir_path_arr if 'Reader' not in i]

    def get_est_time(section_file, topic_name, read_speed):
        exact_time = round(counter(section_file, topic_name, read_speed))

        if exact_time < 5:
            est_time_str = "5"
        else:
            # round down to nearest multiple of five
            low = 5 * (exact_time // 5)
            est_time_str = str(low) + "-" + str(low + 5)


        return est_time_str

    for path in course_dir_paths:

        chapter_topics = get_dco_yaml(path)
        
        course_dir = os.path.basename(os.path.dirname(path))
        
        if (len(chapter_topics) > 0):
            # iterate through topic names, in order
            # TODO: as comprehension?
            for topic in chapter_topics:
                topic_name = topic[0]
                subtopics = topic[1]
                # find correct chapter topic path
                topic_path = path+'**/topics/'+topic_name+'/'
                # for each section, extract the topic root
                subtopics = [subtopic.split("-")[0] for subtopic in subtopics]
                # remove duplicates
                subtopic_set = list(dict.fromkeys(subtopics))
                
                for subtopic in subtopic_set:
                    # get root
                    section_path = topic_path+subtopic+adoc_pattern
                    sections = glob.glob(section_path, recursive=True)
                    # bail if empty result
                    if len(sections) == 0:
                        continue
                    
                    stub = course_dir+"\t"+topic_name + "\t"+subtopic + "\t"
                    # get count for each type of file under this subtopic
                    for section_file in sections:
                        if lecture_pattern in section_file:
                            time = get_est_time(section_file, topic_name, lecture_read_speed)
                            print(stub + "Lecture\t"+str(time))
                        elif ge_pattern in section_file or practice_pattern in section_file:
                            time = get_est_time(section_file, topic_name, ge_read_speed)
                            print(stub + "GE\t"+str(time))
                        elif mc_pattern in section_file or quiz_pattern in section_file:
                            time = get_est_time(section_file, topic_name, quiz_read_speed)
                            print(stub + "Quiz\t"+str(time))


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("Please specify directory to search")
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
    quiz_read_speed = int(settings['quiz_read_speed'])

    try:
        if (os.path.isfile(file_input)): 
            counter(file_input, "unknown topic", 0)
        elif (os.path.isdir(file_input)):
            directory_process(file_input)
    except Exception as e: 
        print(e)
