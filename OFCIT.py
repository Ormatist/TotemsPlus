###################################################################
#                             Totems+                             #
# A new and unique way to integrate custom totems into Minecraft! #
#    Learn More here:https://github.com/The-Iceburg/TotemsPlus    #
#        Created By The Totems+ Team - Ormatist + Dockuin         #
###################################################################

# imports the libaries used within Totems+ 
import os, shutil, getpass, PySimpleGUI as sg
from PIL import Image

# outlines the versions and there pack formats
packFormat4 = ["1.14","1.14.1","1.14.2","1.14.3","1.14.4"]
packFormat5 = ["1.15","1.15.1","1.15.2","1.16","1.16.1"]
packFormat6 = ["1.16.2","1.16.3","1.16.4","1.16.5"]

# defines the CIT function
def CIT(textureList, version):

    # sets the counter to 0
    counter = 0

    # transforms texture list into a list
    textureList = textureList.split(";")

    # if the directory resized already exists, then delete it
    if os.path.exists('C:/Users/' + getpass.getuser() + '/AppData/Roaming/Totems+/resized'):
        shutil.rmtree('C:/Users/' + getpass.getuser() + '/AppData/Roaming/Totems+/resized')

    # make the resized folder
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/Totems+/resized")

    # new list to hold the new file names
    pathList = []

    # for loop for each image
    for i in range(len(textureList)):

        # the first image gets opened
        origIMG = str(open(textureList[i]))

        # removes the leading and prior words
        origIMG = origIMG.replace("<_io.TextIOWrapper name='", "")
        origIMG = origIMG.replace("' mode='r' encoding='cp1252'>", "")
        
        # finds only the names
        splitList = textureList[i].split("/")
        
        # the path for the resized folder
        targetIMG = "C:/Users/" + getpass.getuser() + "/AppData/Roaming/Totems+/resized"
        
        # copies the images to the resized folder
        shutil.copy(origIMG, targetIMG)
        IMGpath = targetIMG + "/" + splitList[-1]

        # opens the new image path
        openIMG = Image.open(IMGpath)
        
        # resizes the image, and saves with a new name
        resizedIMG = openIMG.resize((128,128))
        fileName1 = "resize_" + str(splitList[-1]) 
        resizedIMG.save(fileName1)

        # moves to the resized folder and saves the path to the path list 
        shutil.move(fileName1, targetIMG)
        fileName2 = targetIMG + "/" + fileName1
        pathList.append(fileName2)

    # defines how the main window will be displayed/layed-out
    layout = [ 
        [
            sg.Image(filename=pathList[0], key='-IMAGE-'),
            sg.Text("You've selected Totems+ CIT Integration!\n" + 
            'This integration will generate:\n' + 
            'A Custom Resource Pack\n' + 
            'Follow the tooltip below to customize your packs!\n' + 
            ' ', font=('Helvetica', 10), justification='left'),
        ],
        [
            sg.Text('Rename your different textures to what you wish to rename them in-game\n', key='tooltip')
        ],
        [
            sg.Text('Name:  '),
            sg.InputText(size=(25, 1), key='itemName'),
        ],
        [
            sg.Button('Next', key='next'),
            sg.Button('Cancel', key='cancel'),
        ],
    ]

    # creates the window
    window = sg.Window("CIT", layout, icon="img/totems.ico")

    # sets the base name (for if it isn't changed)
    name = "Totems+ OFCIT"

    # checks if the resource pack exists and if it does user is prompted to suggest a new name
    if os.path.exists('C:/Users/' + getpass.getuser() + '/AppData/Roaming/.minecraft/resourcepacks/Totems+ OFCIT'):
        name = sg.popup_get_text("An OFCIT Integration resource pack allready exists\nPlease choose a different name for this one:", title = "Duplicate Pack")

    # pre-makes the resource pack directory in the minecraft resource pack folder
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name)
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets")
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft")
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine")
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine/cit")
    os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine/cit/totems")

    # copys the pack.png file into place
    shutil.copy("img/pack.png", "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name)

    # creates & opens the pack.mcmeta file
    packMeta = open("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/pack.mcmeta", "w+")

    # derrives the resource pack format code from the version
    if version in packFormat4:
        packFormat = 4
    elif version in packFormat5:
        packFormat = 5
    elif version in packFormat6:
        packFormat = 6
    elif version.startswith("1.17"):
        packFormat = 7
    elif version.startswith("1.18"):
        packFormat = 8
    elif version.startswith("1.19"):
        packFormat = 9

    # adds the needed meta data to the pack.mcmeta file
    packMeta.writelines(['{\n',
    '  "pack": {\n',
    '    "pack_format": ' + str(packFormat) + ',\n',
    '	"description": "Version: ' + version + '\n',
    'Made By: The Totems+ Team"\n',
    '  }\n',
    '}'])
    packMeta.close()

    # while window (GUI) is open
    while True:

        # read all events/actions
        event, values = window.read()

        # if window closed break while loop and end code
        if event == sg.WIN_CLOSED:
            break
        
        # if the cancel button is pressed
        if event == 'cancel':
            
            # a confirmation window is displayed and if the user agrees all files are removed
            result = sg.popup_ok_cancel("Are you sure? Cancelling now will remove any current progress/packs")

            if result == "OK":
                shutil.rmtree("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name)
                break
        
        # else if the next button and the length of the texture list isn't equal to the counter + 1
        elif event == 'next' and len(textureList) != int(counter + 1):

            # sets the rename value to the user input ensuring no spaces are included
            rename = values["itemName"].replace(" ", "_")

            # makes custom directory for each file and curates a .properties file 
            os.mkdir("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine/cit/totems/" + str(rename.lower()))
            totemProperties = open("C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine/cit/totems/" + str(rename.lower()) + "/totem_of_undying.properties", "w+")

            # deduces the file name from its location
            textureListSplit = textureList[counter].split("/")
            
            # adds the needed meta to the totem_of_undying.properties file
            totemProperties.writelines(["type=item\n",
            "matchItems=totem_of_undying\n",
            "texture=" + textureListSplit[-1] + "\n",
            "nbt.display.Name=ipattern:" + values["itemName"]])
            totemProperties.close()

            # copys the image into the resource pack
            shutil.copy(textureList[counter], "C:/Users/" + getpass.getuser() + "/AppData/Roaming/.minecraft/resourcepacks/" + name + "/assets/minecraft/optifine/cit/totems/" + str(rename.lower()))

            # cycles the image and clears the text box
            window.Element('-IMAGE-').update(filename=pathList[counter + 1])
            window.Element('itemName').update('')

            # increases the counter by 1
            counter += 1

        # else if the next button and the length of the texture list is equal to the counter + 1
        elif event == 'next' and len(textureList) == int(counter + 1):

            # prints completion message to user
            sg.popup_ok("Pack creation complete! Load up Minecraft and you Totems+ pack will appear in your resourcepack folder!", title = "Pack Completion", icon="img/totems.ico")

            # breaks the loop (hence closing all windows)
            break
        
    # closes window if called
    window.close()