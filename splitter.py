import os

from bs4 import BeautifulSoup

TEXTS_LIST = []

def get_all_source_texts():
    #Generate List of Texts in input directory for Menu
    directory = 'input'

    for file in sorted(os.listdir(directory)):
        f = os.path.join(directory, file)
        #Make sure it's a file
        if os.path.isfile(f):
            TEXTS_LIST.append(f)

def divide_novel_into_chapters(filename):
    output_folder_name = filename.split('/')[1]
    output_folder_name = output_folder_name.split('.')[0]
    
    with open(f'{filename}') as working_file:
        contents = working_file.read()
        #Soupify Contents
        soup = BeautifulSoup(contents, features="xml")

    #Create Output Directory
    os.mkdir(f'output/{output_folder_name}')

    i = 1 #Starting Chapter
    for element in soup.find_all("div", {"type": "chapter"}):
        with open(f'output/{output_folder_name}/chapter_{i}', 'w') as output_file:
            output_file.write(str(element))
        i += 1

#Get the list of input texts
get_all_source_texts()

#Now, process everything:
for novel in TEXTS_LIST:
    divide_novel_into_chapters(novel)