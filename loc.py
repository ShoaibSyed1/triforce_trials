import os
from pathlib import Path

def get_loc_dir(dir, ext):
    loc = 0
    for file in os.listdir(dir):
        if Path(dir + "/" + file).is_dir():
            loc += get_loc_dir(dir + "/" + file, ext)
        elif file.endswith(ext):
            loc += sum(1 for line in open(dir + "/" + file) if line.rstrip())
    
    return loc

def get_amount(dir, ext):
    amount = 0
    for file in os.listdir(dir):
        if Path(dir + "/" + file).is_dir():
            amount += get_amount(dir + "/" + file, ext)
        elif file.endswith(ext):
            amount += 1
    
    return amount

def get_size(dir, ext):
    size = 0
    for file in os.listdir(dir):
        if Path(dir + "/" + file).is_dir():
            size += get_size(dir + "/" + file, ext)
        elif file.endswith(ext):
            size += os.path.getsize(dir + "/" + file)
    
    return size

loc = get_loc_dir("./src", ".py")
loc_size = get_size("./src", ".py")

text = get_loc_dir("./assets", ".toml")
images = get_amount("./assets", ".png")
sounds = get_amount("./assets", ".wav")
music = get_amount("./assets", ".mp3")
text_size = get_size("./assets", ".toml")
images_size = get_size("./assets", ".png")
sounds_size = get_size("./assets", ".wav")
music_size = get_size("./assets", ".mp3")

total_assets_size = text_size + images_size + sounds_size + music_size
total_size = total_assets_size + loc_size

print("===CODE===")
print("Lines of code: " + str(loc) + " (" + str(int(loc_size / (2 ** 10))) + " kb)")

print("===ASSETS===")
print("Lines of text: " + str(text) + " (" + str(int(text_size / (2 ** 10))) + " kb)")
print("Number of images: " + str(images) + " (" + str(int(images_size / (2 ** 10))) + " kb)")
print("Number of sounds: " + str(sounds) + " (" + str(int(sounds_size / (2 ** 20))) + " mb)")
print("Number of music files: " + str(music) + " (" + str(int(music_size / (2 ** 20))) + " mb)")
print("Total Size of Assets: " + str(int(total_assets_size / (2 ** 20))) + " mb")

print("===TOTAL===")
print(str(int(total_size / (2 ** 20))) + " mb")