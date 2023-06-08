from copy import copy
from proyek import *

if __name__ == '__main__':
    #input username untuk drive c
    username = input("Input UserName: ")

    #inisiasi array current path untuk menyimpan posisi sekarang
    currentPath = []

    #inisiasi Root bernama My computer
    NodeComputer = NodeFolder("My Computer")
    tree = Tree(NodeComputer)

    #inisiasi drive c kemudian dimasukan ke anaknya my computer
    nodeC = NodeDrive("C", username)
    NodeComputer.child.addWithSort(nodeC)

    #inisiasi folder Users kemudian dimasukan ke anaknya drive C:
    nodeUsers = NodeFolder("Users")
    nodeC.child.addWithSort(nodeUsers)

    # inisiasi folder sesuai input nama dimasukan ke anaknya Users
    nodeChildUsers = NodeFolder(username)
    nodeUsers.child.addWithSort(nodeChildUsers)

    #memasukkan folder-folder ke dalam anaknya nodeChildUsers
    nodeChildUsers.child.addWithSort(NodeFolder("Desktop"))
    nodeChildUsers.child.addWithSort(NodeFolder("Downloads"))
    nodeChildUsers.child.addWithSort(NodeFolder("Documents"))
    nodeChildUsers.child.addWithSort(NodeFolder("Pictures"))
    nodeChildUsers.child.addWithSort(NodeFolder("Music"))
    nodeChildUsers.child.addWithSort(NodeFolder("Video"))

    # inisiasi folder public di dalam anaknya Users
    nodeUsers.child.addWithSort(NodeFolder("Public"))

    # memasukkan folder-folder ke dalam anaknya Public
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Desktop"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Downloads"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Documents"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Pictures"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Music"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Video"))

    #Memasukan node my computer ke dalam curentpath untuk menginisiasi posisi pertama
    currentPath.append(NodeComputer)

while True:
    print()
    #Jika posisi Sekarang berada di My computer maka muncul menu khusus drive, jika tidak masuk ke menu folder
    if currentPath[-1] == NodeComputer:
        print("===================MENU MY COMPUTER===================")
        print("1. Add Drive")
        print("2. Change Directory")
        print("3. dir Ascending")
        print("4. dir Descending")
        print("5. Rename")
        print("6. Print Structure Current")
        print("7. Searching")
        print_path(currentPath)
        user = input("Input menu: ")
        if user == "1":
            #inisiasi drive
            diskName = input("New Drive Disk Name (Contoh D): ")
            diskName = diskName.upper()

            #inisiasi nama drive nya
            authName = input("Input Author Name: ")
            newDrive = NodeDrive(diskName, authName)

            #Di cek apakah nama drivenya sesuai dengan syarat di dalam fungsinya
            if newDrive.status == True:
                currentPath[-1].child.addWithSort(newDrive)

        elif user == "2":

            print("list of available directory : ")
            print_children(currentPath[-1])
            print()
            nameDir = input("Change dir to? (Folder Name) : ")
            node = currentPath[-1].child.getNode(nameDir)
            #dicek apakah input nama dir nya ada tidak
            if node is not None:
                currentPath.append(node)

        elif user == "3":
            #print list drive secara asc
            currentPath[-1].child.printAsc()
        elif user == "4":
            # print list drive secara dsc
            currentPath[-1].child.printDesc()
        elif user == "5":
            #input nama author drive yang ingin diubah
            willRename = input("Input Nama Drive yang akan direname (Contoh: C:): ")
            nodeRename = currentPath[-1].child.getNode(willRename)
            #dicek apakah input namanya ada tidak
            if nodeRename is not None:
                newName = input("New Name: ")
                currentPath[-1].child.renameThenSort(nodeRename, newName)
        elif user == "6":
            print("Structure dari ", end="")
            print_path(currentPath)
            print()
            print_structure(currentPath[-1])
        elif user == "7":
            name = input("Input nama yang akan dicari: ")
            tree.findAll(tree.root, name)
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
        print("21. Searching")
        print_path(currentPath)
        print()
        user = input("Pilihan anda: ")
        if user == "1":
            #Memasukkan Folder ke dalam anak terakhir dari currentpath
            folderName = input("New Folder Name: ")
            newFolder = NodeFolder(folderName)
            currentPath[-1].child.addWithSort(newFolder)
        elif user == "2":
            fileName = input("New File Name and with file type (Example: File1.txt): ")
            #di cek apakah file name terdapat . kalau tidak ada dipaksa .txt
            cek = False
            for i in fileName:
                if i == '.':
                    cek = True
            if not cek:
                fileName = fileName + '.txt'
            newFile = NodeFile(fileName)
            currentPath[-1].child.addWithSort(newFile)



        elif user == "3":
            print("list of available directory : ")
            #print list nya dengan tipe 1 sesuai dengan syarat print_childern (utk folder, drive, zip)
            print_children(currentPath[-1], 1)
            nameDir = input("Change dir to? (Folder Name) : ")
            node = currentPath[-1].child.getNode(nameDir)
            #dicek apakah node yang dituju merupakan file, kalo iya tidak bisa
            if type(node) == NodeFile:
                print('Can\'t change dir to file')
            else:
                # dicek apakah input namanya ada tidak
                if node is not None:
                    currentPath.append(node)
        elif user == "4":
            currentPath[-1].child.printAsc()
        elif user == "5":
            currentPath[-1].child.printDesc()

        elif user == "6":
            currentPath.pop(-1)

        elif user == "7":
            print("List of Folder and File in this folder")
            #print semua listnya
            print_children(currentPath[-1])
            willRename = input("Input Nama Folder/ File yang akan direname: ")
            nodeRename = currentPath[-1].child.getNode(willRename)
            # dicek apakah input namanya ada tidak
            if nodeRename is not None:
                newName = input("New Name: ")
                currentPath[-1].child.renameThenSort(nodeRename, newName)

        elif user == "8":
            print("List of File in this folder")
            # print list nya dengan tipe 2 sesuai dengan syarat print_childern (utk file)
            print_children(currentPath[-1], 2)
            willDelete = input("Input File yang akan didelete: ")
            cek = False
            #cek type yang di input apakah file / tidak
            if type(currentPath[-1].child.getNode(willDelete)) == NodeFile:
                cek = True


            if cek:
                currentPath[-1].child.deleteByName(willDelete)
            else:
                print("masukkan data yang benar")


        elif user == "9":
            foldername = input("Input nama Folder yang akan dihapus: ")
            cek = False
            # cek type yang di input apakah folder / tidak
            if type(currentPath[-1].child.getNode(foldername)) == NodeFolder:
                cek = True

            if cek:
                node = currentPath[-1].child.getNode(foldername)
                # dicek apakah input namanya ada tidak
                if node is not None:
                    nodeParent = currentPath[-1]
                    deleteFolderAll(nodeParent, node)
            else:
                print("masukkan data yang benar")


        elif user == "10":
            foldername = input("Input nama Folder yang akan dihapus: ")
            cek = False
            # cek type yang di input apakah folder / tidak
            if type(currentPath[-1].child.getNode(foldername)) == NodeFolder:
                cek = True

            if cek:
                node = currentPath[-1].child.getNode(foldername)
                # dicek apakah input namanya ada tidak
                if node is not None:
                    nodeParent = currentPath[-1]
                    deleteFolderOnly(nodeParent, node)
            else:
                print("masukkan data yang benar")


        elif user == "11":
            name = input("Input nama Folder/ File yang akan ditampilkan pathnya: ")
            node = currentPath[-1].child.getNode(name)
            # dicek apakah input namanya ada tidak
            if node is not None:
                tree.printPath(node)

        elif user == "12":
            currentPath[-1].child.sortByType()
        elif user == "13":
            types = input("Input Type: ")
            currentPath[-1].child.viewByType(types)
        elif user == "14":
            currentPath[-1].child.groupBy()

        elif user == "15":
            name = input("Input name of folder/file: ")
            node = currentPath[-1].child.getNode(name)
            # dicek apakah input namanya ada tidak
            if node is not None:
                tree.getDetail(node)

        elif user == "16":
            print_children(currentPath[-1])
            name = input("Input name of folder/file: ")
            nodes = currentPath[-1].child.getNode(name)
            parent = currentPath[-1]

            # dicek apakah input namanya ada tidak
            if nodes is not None:
                while True:
                    print_path(currentPath)
                    print()
                    print_children(currentPath[-1])
                    print()
                    print("===================MENU COPY PASTE===================")
                    print("1. Paste here")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user = input("Input menu: ")
                    if user == "1":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa paste ke situ
                        if currentPath[-1] == NodeComputer:
                            print("Can't Paste in My Computer")
                            continue
                        # dicek apakah parent ditempat yang sama, kalo iya nama file ditampah -copy
                        if currentPath[-1] == parent:
                            copypaste(copy(nodes), currentPath[-1], nodes.name + "-copy")
                        else:
                            copypaste(copy(nodes), currentPath[-1], nodes.name)
                        break
                    elif user == "2":
                        nameDir = input("Change dir to? (Folder Name) : ")
                        node = currentPath[-1].child.getNode(nameDir)
                        # dicek apakah nama dir ada tidak
                        if node is not None:
                            # dicek apabila ingin masuk ke childnya, keluar perintah tidak bisa
                            if node == nodes:
                                print("The Destination Folder is a subfolder of the source folder")
                            else:
                                currentPath.append(node)
                    elif user == "3":
                        currentPath[-1].child.printAsc()
                    elif user == "4":
                        currentPath[-1].child.printDesc()
                    elif user == "5":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa ke prev path
                        if currentPath[-1] == NodeComputer:
                            print("Sudah Root!")
                            continue
                        currentPath.pop(-1)
                    elif user == "0":
                        break
                    else:
                        print('Input Invalid input ulang yee...')

        elif user == "17":
            print_children(currentPath[-1])
            name = input("Input nama folder/file yang akan dipindah: ")
            nodes = currentPath[-1].child.getNode(name)
            # dicek apakah input namanya ada tidak
            if nodes is not None:
                nodeParent = currentPath[-1]
                while True:
                    print_path(currentPath)
                    print()
                    print_children(currentPath[-1], 1)
                    print("===================MENU MOVE===================")
                    print("1. Move here")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user = input("Input menu: ")
                    if user == "1":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa move ke situ
                        if currentPath[-1] == NodeComputer:
                            print("Can't move in My Computer")
                            continue
                        move(nodeParent, nodes, currentPath[-1])
                        break
                    elif user == "2":
                        nameDir = input("Change dir to? (Folder Name) : ")
                        node = currentPath[-1].child.getNode(nameDir)
                        # dicek apakah nama dir ada tidak
                        if node is not None:
                            # dicek apabila ingin masuk ke childnya, keluar perintah tidak bisa
                            if node == nodes:

                                print("The Destination Folder is a subfolder of the source folder")
                            else:
                                currentPath.append(node)
                    elif user == "3":
                        currentPath[-1].child.printAsc()
                    elif user == "4":
                        currentPath[-1].child.printDesc()
                    elif user == "5":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa ke prev path
                        if currentPath[-1] == NodeComputer:
                            print("Sudah Root!")
                            continue
                        currentPath.pop(-1)
                    elif user == "0":
                        break
                    else:
                        print('Input Invalid!')
        elif user == "18":
            #inisiasi array untuk mentimpan file zip
            listOfFileZip = []
            while True:
                print("Daftar Folder/file")
                print_children(currentPath[-1])
                print("===================MENU ZIP===================")
                print("1. Pilih File/Folder yang akan dizip")
                print("2. ZIP NOW!")
                print("3. dir Ascending")
                print("4. dir Descending")
                print("0. Cancel")
                user = input("Input User: ")
                if user == "1":
                    inputName = input("Input nama File/Folder yang akan dizip: ")
                    getNode = currentPath[-1].child.getNode(inputName)
                    # di cek di dalam listOfFileZip ada tidak
                    if getNode not in listOfFileZip:
                        # ditambahkan dalam penyimpanan list array
                        listOfFileZip.append(getNode)
                    else:
                        print('File/Folder sudah termasuk dalam zip')
                elif user == "2":
                    name = input("Input name of zip file: ") + ".zip"
                    #ditambahkan ke dalam node zip
                    Node = NodeZip(name)
                    Node.addZip(listOfFileZip)
                    #diatmbahkan ke childnya
                    currentPath[-1].child.addWithSort(Node)
                    break
                elif user == "3":
                    currentPath[-1].child.printAsc()
                elif user == "4":
                    currentPath[-1].child.printDesc()
                elif user == "0":
                    break
                else:
                    print('Input Invalid')


        elif user == "19":
            currentPath[-1].child.viewOnlyZip()
            name = input("Input nama file zip (Example: file.zip): ")
            node = currentPath[-1].child.getNode(name)
            #dicek apakah input namanya ada tidak dan tipe nya zip
            if node is not None and type(node) == NodeZip:
                while True:
                    print_path(currentPath)
                    print()
                    print_children(currentPath[-1])
                    print("===================MENU UNZIP===================")
                    print("1. UNZIP HERE")
                    print("2. Change directory")
                    print("3. dir Ascending")
                    print("4. dir Descending")
                    print("5. Prev Dir")
                    print("0. Cancel")
                    user = input("Input menu: ")
                    if user == "1":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa unzip ke situ
                        if currentPath[-1] == NodeComputer:
                            print("Can't unzip in My Computer")
                            continue
                        unzip(node, currentPath[-1])
                        break
                    elif user == "2":
                        nameDir = input("Change dir to? (Folder Name) : ")
                        nodes = currentPath[-1].child.getNode(nameDir)
                        # dicek apakah input namanya
                        if nodes is not None:
                            currentPath.append(nodes)
                    elif user == "3":
                        currentPath[-1].child.printAsc()
                    elif user == "4":
                        currentPath[-1].child.printDesc()
                    elif user == "5":
                        # dicek apakah path sampai My computer, kalo iya tidak bisa ke prev path
                        if currentPath[-1] == NodeComputer:
                            print("Sudah Root!")
                            continue
                        currentPath.pop(-1)
                    elif user == "0":
                        break
                    else:
                        print('Input invalid!')
        elif user == "20":
            print("Structure dari ", end="")
            print_path(currentPath)
            print()
            print_structure(tree.getNodeByPath(tree.getPath(currentPath[-1])))
        elif user == "21":
            name = input("Input nama yang akan dicari: ")
            tree.findAll(tree.root, name)
        else:
            print('input invalid,input lagi!!')

