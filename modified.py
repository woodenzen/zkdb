import os
import datetime

def count_modified_md_files(days_ago):
    days_ago = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    counter = 0
    zettelkasten = '/Users/will/Dropbox/zettelkasten/'
    for root, dirs, files in os.walk(zettelkasten):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if mod_time > days_ago:
                    counter += 1

    return counter

if __name__ == '__main__':
    print(f'{count_modified_md_files(10)}')