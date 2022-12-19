import os

content = list()

folder = "../files"
for file in os.listdir(folder):
    with open(os.path.join(folder, file)) as f:
        content.append(f.read())