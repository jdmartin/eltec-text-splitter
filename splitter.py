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

    #Get the year from the source filename
    the_year = output_folder_name[3:7] #They're regular, so we can cheat

    #Get the title from the source filename for use in folder naming
    the_title = output_folder_name.replace('_', '—') #Replace underscore with em-dash to avoid annoying the relationships parser.

    #Get the title from the source TEI for use in the new TEI header
    the_text_title = soup.bibl.title.get_text()

    #Get the author from the source TEI
    the_author = soup.author.get_text()

    #Get the publisher from the source TEI
    the_publisher = soup.publisher.get_text()

    #Create Output Directories for Splits
    if not os.path.exists(f'output/splits/{the_year}-{the_title}'):
       os.mkdir(f'output/splits/{the_year}-{the_title}')
    if not os.path.exists(f'output/tei_splits/{the_year}-{the_title}'):
        os.mkdir(f'output/tei_splits/{the_year}-{the_title}')

    i = 1 #Starting Chapter
    for element in soup.find_all("div", {"type": "chapter"}):
        # return data by retrieving the tag content
        clean_data = element.get_text()
        #Knock together a TEI head, text, and foot
        tei_data = f"""<?xml-model href="https://raw.githubusercontent.com/TEIC/TEI-Simple/master/teisimple.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><titleStmt><title>{the_text_title}</title><author>{the_author}</author></titleStmt><publicationStmt><publisher>{the_publisher}</publisher><date>{the_year}</date></publicationStmt></teiHeader><text><body><div type="chapter" n="{i}">""" + clean_data + """</div></body></text></TEI>"""
  
        with open(f'output/splits/{the_year}-{the_title}/{the_year}-{the_title}-chapter_{i}', 'w') as output_file:
            output_file.write(str(clean_data))
        
        with open(f'output/tei_splits/{the_year}-{the_title}/{the_year}-{the_title}-chapter_{i}', 'w') as output_file:
            output_file.write(str(tei_data))

        with open(f'output/bucket/{the_year}-{the_title}-chapter_{i}', 'w') as output_file:
            output_file.write(str(clean_data))

        with open(f'output/tei_bucket/{the_year}-{the_title}-chapter_{i}', 'w') as output_file:
            output_file.write(str(tei_data))

        i += 1


#Prepare bucket and splits folders
list_of_paths = ['output/splits', 'output/tei_splits', 'output/bucket', 'output/tei_bucket']
#No TEI, broken up by book, With TEI, broken up by book, No TEI, all in one folder, With TEI, all in one folder
for item in list_of_paths:
    if not os.path.exists(item):
        os.mkdir(item) 

#Get the list of input texts
get_all_source_texts()

#Now, process everything:
for novel in TEXTS_LIST:
    divide_novel_into_chapters(novel)
