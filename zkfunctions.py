import os

'''
get folder size
'''
def getFolderSize(folder):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):#not sub folders
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)   
    return total_size
    
'''
Human readable single folder size
'''

def sizeof_fmt(num, suffix='bytes'):
    for unit in ['',' Kilo',' Mega',' Giga',' Tera',' Peta',' Exa',' Zetta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return


if __name__ == '__main__':
    print(sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten/media/')))

folder='/Users/will/Dropbox/zettelkasten/'    
subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
print(subfolders)