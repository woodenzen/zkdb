import os
import pathlib
from TheArchivePath import TheArchivePath
from get_word_count import get_word_count


#####
# Variables
#####
# path to zettelkasten
zettelkasten = pathlib.Path(TheArchivePath())



def zk_stats():
    twords = 0
    tlinks = 0
    tzettel = 0
    for filename in os.listdir(zettelkasten):
        if filename.endswith(".md"):
            file = open((os.path.join(zettelkasten, filename)), "r")
            data = file.read()
            links = data.count("]]")
            tlinks += links# Calculate the total word count
            twords = (get_word_count() for file in filename)
            tzettel += 1

            continue
        else:
            continue







if __name__ == "__main__":
    zk_stats()
    print(f'The Current ZK Directory. {zettelkasten}')
    print(f'## {len(os.listdir(zettelkasten))} notes in the archive.')   
    print(f'{twords} Total word count')
    print(f'{tlinks - tzettel} Total link count')
    print(f'{tzettel} Total zettel count')
    # print(f'{calculate_avg_notes_per_day(zettelkasten)} notes per day on average since day zero (20181114).')
    # proofing_count = count_proofing_files(zettelkasten)
    # print(f"There are {proofing_count} notes wanting attention in my ZK.")
    # print(f'## {current[0]} notes in the last ten days.')
    # for entry in current[4]:
    #     subatomic_line = daily_results.get_subatomic_line(zettelkasten+"/"+entry)
    #     print(f'- [{entry[:-7]}](thearchive://match/›[[{entry[-15:-3]})\n\t- {subatomic_line[11:]}')
# output = f""" 
# {'–'*5}
# ## Zettelkasten Statistics
#        ★★★★★
# {twords} Total word count
# {tlinks - tzettel} Total link count
# {tzettel} Total zettel count
#        ★★★★★
# """     
# print(f'{output}')  