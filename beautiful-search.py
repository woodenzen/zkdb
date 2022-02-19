

def search_beautiful_language (s):
    file = open("/Users/will/Dropbox/zettelkasten/B-How To Live 202106131829.md","r")
    print()
    search = s 
    print()   
    counter = 3
    found = False
    for line in file:
        if search in line:  
           found = True
        if found:
            if counter > 0: 
                counter -= 1
                print(line, counter)
            if counter == 0:
                break
print(search_beautiful_language("Looking"))            
            