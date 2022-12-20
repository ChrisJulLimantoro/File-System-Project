from copy import copy
from proyek import *

def print_structure(node:NodeFolder or NodeDrive,lvl = 1):
    print('>'+node.name)
    temp = node.child.head
    if temp != None:
        while temp != None:
            for i in range(lvl):
                print('    ',end="")
            if type(temp) == NodeFile:
                print('-'+temp.name)
            else:
                print_structure(temp,lvl+1)
            temp = temp.next

def print_path(path):
    for i in range(len(path)):
        if type(path[i])== NodeDrive:
            print(path[i].auth, end= " ")
        print(path[i].name, end=" > ")
    print()

def print_children(node:NodeFolder or NodeDrive,tipe = 0):
    temp = node.child.head
    if temp == None:
        print('Folder masih kosong!')
    else:
        while temp != None:
            if tipe == 0:
                print(" - "+temp.name)
            if tipe == 1:
                if type(temp) == NodeFolder or NodeDrive or NodeZip:
                    if type(temp)== NodeDrive:
                        print(temp.auth, end=" ")
                    print(" - "+temp.name)
            if tipe == 2:
                if type(temp) == NodeFile:
                    print(" - "+temp.name)
            temp = temp.next

def move(nodeParent: NodeFolder,nodePindah: NodeFolder or NodeFile or NodeZip, nodeParentTujuan: NodeFolder):
    temp= nodePindah
    nodeParent.child.deleteByName(nodePindah.name)
    nodeParentTujuan.child.addWithSort(temp)
    
def copypaste(nodeCopy: NodeFolder or NodeFile or NodeZip, nodeParentDest: NodeFolder):
    newNode= copy(nodeCopy)
    nodeParentDest.child.addWithSort(newNode)

def deleteFolderOnly(nodeParentOfFolder: NodeFolder, nodeDeleted: NodeFolder):
    llDelete= nodeDeleted.child
    nodeParentOfFolder.child.deleteByName(nodeDeleted.name)
    iter= llDelete.head
    for i in range(llDelete.size):
        nodeParentOfFolder.child.addWithSort(iter)
        iter= iter.next
def deleteFolderAll(nodeParent: NodeFolder, nodeDelete: NodeFolder):
    nodeParent.child.deleteByName(nodeDelete.name)
    
def unzip(zipInput: NodeZip, NodeTujuan: NodeFolder):
    # indexType=0
    # for i in zipInput.name[::-1]:
    #     if i == ".":
    #         break
    #     indexType += 1
    # newFolderName= zipInput.name[0:len(zipInput.name)-indexType-1]
    # newFolder= NodeFolder(newFolderName)
    # NodeTujuan.child.addWithSort(newFolder)
    iter= zipInput.child.head
    for i in range(zipInput.child.size):
        NodeTujuan.child.addWithSort(copy(iter))
        iter= iter.next

if __name__ == '__main__':
    username= input("Input UserName: ")
    currentPath = []
    NodeComputer = NodeFolder("My Computer")
    tree = Tree(NodeComputer)
    nodeC= NodeDrive("C:", username)
    NodeComputer.child.addWithSort(nodeC)
    nodeUsers= NodeFolder("Users")
    nodeC.child.addWithSort(nodeUsers)
    nodeChildUsers= NodeFolder(username)
    nodeUsers.child.addWithSort(nodeChildUsers)
    nodeChildUsers.child.addWithSort(NodeFolder("Desktop"))
    nodeChildUsers.child.addWithSort(NodeFolder("Download"))
    nodeChildUsers.child.addWithSort(NodeFolder("Document"))
    nodeChildUsers.child.addWithSort(NodeFolder("Pictures"))
    nodeChildUsers.child.addWithSort(NodeFolder("Music"))
    nodeChildUsers.child.addWithSort(NodeFolder("Video"))
    currentPath.append(NodeComputer)
    while True:
        print()
        print()
        if currentPath[-1]==NodeComputer:
            print("===================MENU MY COMPUTER===================")
            print("1. Add Drive")
            print("2. Change Directory")
            print("3. dir Ascending")
            print("4. dir Descending")
            print("5. Rename")
            print("6. Print Structure Current")
            user= input("Input menu: ")
            if user=="1":
                diskName = input("New Drive Disk Name: ")
                authName= input("Input Author Name: ")
                newDrive= NodeDrive(diskName, authName)
                if newDrive.status== True:
                    currentPath[-1].child.addWithSort(newDrive)
            elif user=="2":
                print("list of available directory : ")
                print_children(tree.getNodeByPath(currentPath))
                nameDir= input("Change dir to? (Folder Name) : ")
                node= currentPath[-1].child.getNode(nameDir)
                if node is not None:
                    currentPath.append(node)
            elif user=="3":
                currentPath[-1].child.printAsc()
            elif user=="4":
                currentPath[-1].child.printDesc()
            elif user=="5":
                willRename= input("Input Nama Drive yang akan direname (Contoh: C:): ")
                nodeRename=currentPath[-1].child.getNode(willRename)
                newName= input("New Name: ")
                currentPath[-1].child.renameThenSort(nodeRename, newName)
            elif user=="6":
                print("Structure dari ",end="")
                print_path(currentPath)
                print()
                print_structure(tree.getNodeByPath(currentPath))
            else:
                print("Masukkan Input yang benar!")

        else:
            print("===================MENU UTAMA===================")
            print("1. Add Folder")
            print("2. Add File")
            print("3. Change directory")
            print("4. dir Ascending")
            print("5. dir Descending")
            print("6. Prev Dir")
            print("7. Rename")
            print("8. Delete File By Name")
            print("9. Delete Folder (With All The Content)")
            print("10. Delete Folder (Folder Only)")
            print("11. View Path")
            print("12. Dir sort by type")
            print("13. Dir View by Type (user input type)")
            print("14. Dir Group By")
            print("15. Get Detail")
            print("16. Copy Paste")
            print("17. Move Folder/File")
            print("18. Zip")
            print("19. Unzip")
            print("20. Print Structure Current")
            print_path(currentPath)
            user = input("Pilihan anda: ")
            if user == "1":
                folderName = input("New Folder Name: ")
                newFolder = NodeFolder(folderName)
                currentPath[-1].child.addWithSort(newFolder)
            elif user == "2":
                fileName = input("New File Name and with file type (Example: File1.txt): ")
                newFile = NodeFile(fileName)
                currentPath[-1].child.addWithSort(newFile)
            elif user == "3":
                print("list of available directory : ")
                print_children(tree.getNodeByPath(currentPath))
                nameDir= input("Change dir to? (Folder Name) : ")
                node= currentPath[-1].child.getNode(nameDir)
                if node is not None:
                    currentPath.append(node)
            elif user == "4":
                currentPath[-1].child.printAsc()
            elif user == "5":
                currentPath[-1].child.printDesc()
            elif user == "6":
                currentPath.pop(-1)
            elif user == "7":
                willRename= input("Input Nama Folder/ File yang akan direname: ")
                nodeRename=currentPath[-1].child.getNode(willRename)
                newName= input("New Name: ")
                currentPath[-1].child.renameThenSort(nodeRename, newName)
            elif user == "8":
                willDelete= input("Input File yang akan didelete: ")
                currentPath[-1].child.deleteByName(willDelete)
            elif user == "9":
                foldername= input("Input nama Folder yang akan dihapus: ")
                node= currentPath[-1].child.getNode(foldername)
                nodeParent= currentPath[-1]
                deleteFolderAll(nodeParent,node)
            elif user == "10":
                foldername = input("Input nama Folder yang akan dihapus: ")
                node = currentPath[-1].child.getNode(foldername)
                nodeParent = currentPath[-1]
                deleteFolderOnly(nodeParent, node)
            
            #masih bermasalah
            elif user == "11":
                name= input("Input nama Folder/ File yang akan ditampilkan pathnya: ")
                node= currentPath[-1].child.getNode(name)
                tree.printPath(node)

            elif user == "12":
                currentPath[-1].child.sortByType()
            elif user == "13":
                types= input("Input Type: ")
                currentPath[-1].child.viewByType(types)
            elif user == "14":
                currentPath[-1].child.groupBy()
            elif user == "15":
                name= input("Input name of folder/file: ")
                node= currentPath[-1].child.getNode(name)
                tree.getDetail(node)
            elif user == "16":
                name= input("Input name of folder/file: ")
                nodes= currentPath[-1].child.getNode(name)
                while True:
                    for i in range(len(currentPath)):
                        print(currentPath[i].name, end=" > ")
                    print()
                    print("===================MENU COPY PASTE===================")
                    print("1. Paste here")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user= int(input("Input menu: "))
                    if user==1:
                        copypaste(copy(nodes), currentPath[-1])
                        break
                    elif user==2:
                        nameDir = input("Change dir to? (Folder Name) : ")
                        node = currentPath[-1].child.getNode(nameDir)
                        if node==nodes:
                            print("The Destination Folder is a subfolder of the source folder")
                        else:
                            currentPath.append(node)
                    elif user==3:
                        currentPath[-1].child.printAsc()
                    elif user==4:
                        currentPath[-1].child.printDesc()
                    elif user==5:
                        currentPath.pop(-1)
                    elif user==0:
                        break
            elif user == "17":
                name= input("Input nama folder/file yang akan dipindah: ")
                nodes= currentPath[-1].child.getNode(name)
                nodeParent= currentPath[-1]
                while True:
                    for i in range(len(currentPath)):
                        print(currentPath[i].name, end=" > ")
                    print()
                    print("===================MENU MOVE===================")
                    print("1. Move here")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user= int(input("Input menu: "))
                    if user==1:
                        move(nodeParent,nodes,currentPath[-1])
                        break
                    elif user==2:
                        nameDir = input("Change dir to? (Folder Name) : ")
                        node = currentPath[-1].child.getNode(nameDir)
                        currentPath.append(node)
                    elif user==3:
                        currentPath[-1].child.printAsc()
                    elif user==4:
                        currentPath[-1].child.printDesc()
                    elif user==5:
                        currentPath.pop(-1)
                    elif user==0:
                        break
            elif user=="18":
                listOfFileZip= []
                while True:
                    print("===================MENU ZIP===================")
                    print("1. Pilih File/Folder yang akan dizip")
                    print("2. ZIP NOW!")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("0. Cancel")
                    user= int(input("Input User: "))
                    if user==1:
                        inputName= input("Input nama File/Folder yang akan dizip: ")
                        getNode= copy(currentPath[-1].child.getNode(inputName))
                        listOfFileZip.append(getNode)
                    elif user==2:
                        name= input("Input name of zip file: ")
                        name= name + ".zip"
                        Node= NodeZip(name, listOfFileZip)
                        currentPath[-1].child.addWithSort(Node)
                        break
                    elif user==3:
                        currentPath[-1].child.printAsc()
                    elif user==4:
                        currentPath[-1].child.printDesc()
                    elif user==0:
                        break

            elif user == "19":
                currentPath[-1].child.viewOnlyZip()
                name= input("Input nama file zip (Example: file.zip): ")
                node= currentPath[-1].child.getNode(name)
                while True:
                    for i in range(len(currentPath)):
                        print(currentPath[i].name, end=" > ")
                    print()
                    print("===================MENU UNZIP===================")
                    print("1. UNZIP HERE")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user= int(input("Input menu: "))
                    if user==1:
                        unzip(node, currentPath[-1])
                        break
                    elif user==2:
                        nameDir = input("Change dir to? (Folder Name) : ")
                        nodes = currentPath[-1].child.getNode(nameDir)
                        currentPath.append(nodes)
                    elif user==3:
                        currentPath[-1].child.printAsc()
                    elif user==4:
                        currentPath[-1].child.printDesc()
                    elif user==5:
                        currentPath.pop(-1)
                    elif user==0:
                        break
            elif user == "20":
                print("Structure dari ",end="")
                print_path(currentPath)
                print()
                print_structure(tree.getNodeByPath(currentPath))
            else :
                print('input invalid,input lagi!!')