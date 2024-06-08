import os

####
# Get folder size
####
def getFolderSize(folder):
    total_size = 0
    for file in os.listdir(folder):
        fp = os.path.join(folder, file)
        if os.path.isfile(fp):
            total_size += os.path.getsize(fp)
    return total_size
####
# Human readable single folder size
####

def sizeof_fmt(num, suffix='bytes'):
    for unit in ['',' Kilo',' Mega',' Giga',' Tera',' Peta',' Exa',' Zetta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return

if __name__ == '__main__':
    print("Zettelkasten folder:", sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten')))
    print("Media folder:", sizeof_fmt(getFolderSize('/Users/will/Dropbox/zettelkasten/media')))
    print('-'*40) 