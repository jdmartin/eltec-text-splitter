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

    #Get the text date from the source TEI
    the_year = soup.sourceDesc.find("date").get_text()

    #Get the title from the source filename
    the_title = output_folder_name.replace('_', '—') #Replace space with em-dash to avoid annoying the relationships parser.

    i = 1 #Starting Chapter
    for element in soup.find_all("div", {"type": "chapter"}):
        # return data by retrieving the tag content
        clean_data = element.get_text()
  
        with open(f'output/{output_folder_name}/{the_year}-{the_title}-chapter_{i}', 'w') as output_file:
            output_file.write(str(clean_data))
        i += 1

#Get the list of input texts
get_all_source_texts()

#Now, process everything:
for novel in TEXTS_LIST:
    divide_novel_into_chapters(novel)