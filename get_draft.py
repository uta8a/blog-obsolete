"""
files <- get all file match "content/**/**/index.md"
for file in files:
  header <- start "^---$" to end "^---$"
  if header["draft"] = false:
    list.add(path of file)
output list to file(./draft.md)
"""

import pathlib
import glob
import re

# print(list(glob.glob('content/**/**/index.md')))
files = list(glob.glob('content/**/**/index.md'))
draft_list = []
for file in files:
    with open(file) as f:
        lines = f.readlines()
        front = []
        start = False
        end = False
        for line in lines:
            if line.strip() == '---':
                if start is False:
                    start = True
                    continue
                elif end is False:
                    end = True
                    break
            front.append(line)
        if start is False or end is False:
            print("No frontmatter found")
            quit()
        for element in front:
            left, right = element.split(':')[0].strip(), element.split(':')[1].strip()
            if left == 'draft' and right == 'true':
                draft_list.append(file)
print(draft_list)
with open('DRAFT.md', 'w') as f:
    f.write("List of article draft:true\n\n")
    for draft in draft_list:
        f.write(draft + '\n')