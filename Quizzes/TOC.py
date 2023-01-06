"""
[Add Table of contents to MD]
This assumes there will be a TOC already in line one where line one has
# TOC
this reads from READRAW.md and outputs to README.md
Version 0.1 18/08/21 = Makde it work
Version 0.2 19/08/21 = split the files over pages and made master index
.
.
Version 0.3 XX/XX/XX = Refcator
"""
import os

def TOC_to_all(filelist):
    master_TOC = []
    for file in filelist:
        text_title = file.strip('md$').strip('.')
        master_TOC.append('# '+text_title+' section'+' <a name=\"'+text_title+'"></a>')
        master_TOC.append("-----------")
        with open(file, 'r') as TOC_FILE:
            TOC = ['# TOC']
            README = ['']
            SKIP_TOC = False
            for line in TOC_FILE:
                if "# TOC" in line:
                    SKIP_TOC = True
                    continue
                if SKIP_TOC:
                    if line[0] != "#":
                        continue
                    else:
                        SKIP_TOC = False
                README.append(line.strip('\n'))
                if line[0] == "#":
                    indent = "- "
                    matched = True
                    step = 1
                    title = ""
                    tag_start = '<a name="'
                    tag_end = '"></a>'
                    tagged_title = "#"
                    while matched:
                        if line[step] == "#":
                            indent = ''.join(['  ',indent])
                            step += 1
                            tagged_title = tagged_title+"#"
                        else:
                            for letter in line[step::]:
                                tagged_title = tagged_title+letter
                                if letter == "<":
                                    tagged_title = tagged_title[0:-1]
                                    step = 1
                                    matched = False
                                    break
                                else:
                                    title = title+letter
                            tagged_title = tagged_title.strip()
                            title = title.strip()
                            tag = title.replace(" ", "-")
                            README[-1] = tagged_title+" "+tag_start+tag+tag_end
                            step = 1
                            matched = False
                            TOC.append(indent+"["+title+"]"+"(#"+tag+")")
                            master_TOC.append(indent+"["+title+"]"+"("+"/"+file+"#"+tag+")")
                            indent = "- "
                            title = ""
                if line[0:4] == "![](":
                    if not line[0:6] == "![](im":
                        README[-1] = (line[0:4]+'images/'+line[4:])
        with open(file, 'w+') as NEW_TOC_FILE:
            for line in TOC:
                NEW_TOC_FILE.write(line+"\n")
            for line in README:
                NEW_TOC_FILE.write(line+"\n")
        #
    with open('README.md', 'w+') as NEW_TOC_FILE:
        NEW_TOC_FILE.write("# TABLE OF CONTENTS"+"\n")
        for file in filelist:
            text_title = file.strip('md$').strip('.')
            NEW_TOC_FILE.write("["+text_title+"](#"+text_title+")\n\n")
        NEW_TOC_FILE.write("\n")
        for line in master_TOC:
            NEW_TOC_FILE.write(line+"\n")


def move_files(move_list):
    for file in move_list:
        os.system("mv "+file+" images/"+file)


def commit_git(commit_list):
    os.system("git add -A")
    #commit_data = ' '.join([entry for entry in os.popen("git status | grep 'modified:'").read().split()][1::2])
    os.system("git commit -m 'python TOR.py pushed commits for " + commit_list +" '")
    os.system("git push")


filelist = [entry for entry in (os.popen("ls | grep .md$").read().split())]
#commit_list = os.popen("ls | grep -E '.md$|py$'").read().replace('\n', ' ')
move_list = [entry for entry in (os.popen("ls | grep .png").read().split())]
commit_list = ' '.join([entry for entry in os.popen("git status | grep 'modified:'").read().split()][1::2])

TOC_to_all(filelist)
move_files(move_list)
commit_git(commit_list)
