def get_own_files():
    files = [os.path.join(name) for path, subdirs, files in os.walk("/media/henry/Transcend/Recordings/zLists/") for
             name in files]
    with open("/media/henry/Transcend/Recordings/zLists/" + files[0], 'r') as fp:
        txt_html = fp.read()
    lines = txt_html.split("\n")
    set_decrip = set()
    for i, l in enumerate(lines):
        if "<td class=\"title\">" in l:
            groups = re.search("^([A-Za-z]+-[0-9]+[A-Za-z]?)", lines[i + 1])
            # print(lines[i + 1])
            if groups:
                set_decrip.add(groups[1])
    return set_decrip


def write_to_index(names):
    names = sorted(names)
    bounds = ["[A-D]", "[E-J]", "[K-N]", "[P-Z]"]
    text = ""
    num_col = 2
    print("Multiple sections:")
    for b in bounds:
        text += "\\begin{multicols}{" + str(num_col) + "}\\begin{enumerate}\n"
        t = 0
        for j, f in enumerate(names):
            if not re.search("^" + b, f):
                continue
            if j > 0:
                if f == names[j - 1]:
                    print(f, end=", ")
                    continue
            t += 1
            text += r"\item \nameref{" + f + "} "
            if t % num_col == 0:
                text += "\n"

        text += "\n\\end{enumerate}\\end{multicols} \\newpage \n\n"
    print()
    with open("files.txt", 'w') as fp:
        fp.write(text)


root = '/media/henry/Transcend/Recordings'
revision_path = '/media/henry/Transcend/Video/revision'
import os

import regex as re

files = [os.path.join(name) for path, subdirs, files in os.walk(root) for name in files]

revision_files = [os.path.join(name) for path, subdirs, files in os.walk(revision_path) for name in files]

files.extend(revision_files)
sort_f = []
set_own_files = set()
for f in files:
    ans = re.search("^([A-Z]+-[0-9]+[A-Za-z]?)", f)
    if ans:
        sort_f.append(ans.group(0))
        set_own_files.add(ans.group(0))
write_to_index(sort_f)

files = [os.path.join(name) for path, subdirs, files in os.walk(root) for name in files]

att_files = []
for path, subdirs, files in os.walk(root):
    for name in files:
        if re.search("^([A-Z]+-[0-9]+[A-Za-z]?)", name):
            p = os.path.join(path, name)
            # att_files.append((p, os.path.getctime(p)))
            att_files.append((p, os.stat(p).st_atime))
att_files = sorted(att_files, key=lambda x: x[1])
for t in att_files:
    # print(os.path.basename(t[0]), t[1])
    # from datetime import datetime
    #
    # print(os.path.basename(t[0]), datetime.fromtimestamp(t[1]))
    pass
# for path, subdirs, files in os.walk(revision_path):
#     for name in files:
#         if re.search("^([A-Z]+-[0-9]+[A-Za-z]?)", name):
#             print("\subsection{" + name + "} \ label{" + name + "}")

set_marked_own = get_own_files()
print("Own - Storage:", sorted(set_own_files.difference(set_marked_own)))
print("Storage - Own:", sorted(set_marked_own.difference(set_own_files)))
fimages = "/media/henry/Transcend/Recordings/zImages"

files = [os.path.join(name) for path, subdirs, files in os.walk(fimages) for name in files]
print("Missing Images:")
for f in sorted(set_own_files):
    txt = re.sub("-", "", f)
    txt = "^" + txt.lower()
    is_exist = False
    for img in files:
        if re.search(txt, img):
            is_exist = True
            break
    if not is_exist:
        print(f)
