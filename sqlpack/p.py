from os import path, listdir


packs_dir = path.join(path.dirname(__file__), '..', 'packs')
print(packs_dir)
if path.exists(packs_dir):
    directories = listdir(packs_dir)
    packs = []
    for pack in directories:
        if path.isdir(path.join(packs_dir, pack)):
            content = listdir(path.join(packs_dir, pack))
            if "main.sql.fmt" in content:
                packs.append(pack)
    packs.sort()
    print(packs)
print("Packs directory not found")
