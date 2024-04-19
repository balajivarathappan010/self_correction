from os import system, listdir
from ImageGeneration.cookies import cookie
def GenerateImage(prompt):
    system(f'python -m BingImageCreator --prompt "{prompt}" -U "{cookie}"')
    return listdir('output')