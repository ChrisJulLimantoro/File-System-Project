from copy import copy
from proyekRev import *

if __name__ == '__main__':
    username= input("Input UserName: ")
    currentPath = []
    tree = Tree()
    nodeC= NodeDrive("C", username)
    tree.root.add(nodeC)
    nodeUsers= NodeFolder("Users")
    nodeC.child.addWithSort(nodeUsers)
    nodeChildUsers= NodeFolder(username)
    nodeUsers.child.addWithSort(nodeChildUsers)
    nodeChildUsers.child.addWithSort(NodeFolder("Desktop"))
    nodeChildUsers.child.addWithSort(NodeFolder("Downloads"))
    nodeChildUsers.child.addWithSort(NodeFolder("Documents"))
    nodeChildUsers.child.addWithSort(NodeFolder("Pictures"))
    nodeChildUsers.child.addWithSort(NodeFolder("Music"))
    nodeChildUsers.child.addWithSort(NodeFolder("Video"))
    nodeUsers.child.addWithSort(NodeFolder("Public"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Desktop"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Downloads"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Documents"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Pictures"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Music"))
    nodeUsers.child.head.next.child.addWithSort(NodeFolder("Public Video"))
    currentPath.append(tree.root)

while True:
    print()
    print_path(currentPath)
    key = input().strip()
    cmd = key.split(" ",1)
    if cmd[0].strip().lower() == 'out':
        # function quit
        break
    elif cmd[0].strip().lower() == 'help':
        # function menampilakn list of command
        print('=============== List of Command ===============')
        print('cd [NAMA_DIR] -- untuk change directory')
        print('find [REGEX] -- unutk menampilkan semua path dengan file/folder yang mengandung regex yg dicari')
        print('ls -- print seluruh children di folder tersebut secara ascending')
        print('ls -r -- print seluruh children di folder tersebut secara descending')
        print('ls -file -- print seluruh children dengan tipe file di folder tersebut')
        print('ls -folder -- print seluruh children dengan tipe folder di folder tersebut')
        print('ls -type -- print seluruh children sort berdasarkan type')
        print('ls -group --print seluruh children dengan group sesuai type')
        print('ls -structure --print sesuai structure tree')
        print('mkdir [NAMA_DIR] --Menambahkan folder ke dalam current path/node')
        print('mkdrive [NAMA_DRIVE(1 huruf)]|[NAMA_AUTHOR] --Membuat drive di My Computer')
        print('touch [NAMA_FILE] --membuat file baru kedalam folder')
        print('mv [NAMA_FILE/DIR/ZIP] [NAMA_PATH] --memindahkan file/folder/zip ke folder di path')
        print('cp [NAMA_FILE/DIR/ZIP] [NAMA_PATH] --mengcopy file/folder/zip ke folder di path')
        print('rename [NAMA_LAMA]:[NAMA_BARU] --rename file/folder/zip')
        print('zip [NAMA_FILE],[NAMA_FILE2],...:[NAMA_ZIP] --zip file yang dipilih ')
        print('unzip [NAMA_ZIP] [NAMA_PATH] --melakukan unzip')
        print('del [NAMA_FILE/DIR/ZIP] --delete (khusus folder hanya delete foldernya namun anaknya akan naik ke atasnya)')
        print('delall [NAMA_FILE/DIR/ZIP] --delete all(khusus folder bakalan hapus semuane sama isinya)')
        print('vp [NAMA_FILE/DIR/ZIP] --view path')
        print('vd [NAMA_FILE/ZIP/DIR] --view detail')
        print('vt [TYPE] --view berdasarkan type')
        print('out -- untuk exit/end CLI')

    elif cmd[0].strip().lower() == 'cd':
        # function untuk change directory 
        if cmd.__len__() > 1:
            if cmd[1].strip() == "..":
                # (.. -> mundur)
                if currentPath.__len__() > 1:
                    currentPath.pop(-1)
                else :
                    print('My Computer merupakan root!')
            else:
                # nama dir/zip
                if currentPath[-1] == tree.root:
                    node = currentPath[-1].dict[cmd[1].strip().upper()]
                else:
                    node = currentPath[-1].child.getNode(cmd[1].strip())
                if type(node) == NodeFile:
                    print('Can\'t change dir to file')
                else:
                    if node is not None:
                        currentPath.append(node)
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'find':
        # function untuk find all 
        if cmd.__len__() > 1:
            print('All List of Possible finding in this Folder : ')
            tree.findAll(currentPath[-1],cmd[1].strip())
        else:
            print('Invalid Syntax!')

    elif cmd[0].strip().lower() == 'mkdir':
        # function untuk create new directory menerima nama directory baru
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Can\'t add Folder in My Computer')
            else:
                currentPath[-1].child.addWithSort(NodeFolder(cmd[1].strip()))
        else :
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'mkdrive':
        # function untuk create drive baru menerima nama drive yang pasti di upper dan author
        if cmd.__len__() > 1:
            temp = cmd[1].strip().split("|")
            if temp.__len__() > 1:
                if currentPath[-1] == tree.root:
                    currentPath[-1].add(NodeDrive(temp[0].strip().upper(),temp[1].strip()))
                else :
                    print('Drive can only be added in My Computer')
            else:
                print('Invalid Syntax!')
        else:
            print('Invalid Syntax!')

    elif cmd[0].strip().lower() == 'touch':
        # function untuk create file baru
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Can\'t add File in My Computer')
            else:
                if "." not in cmd[1].strip().lower():
                    name = cmd[1].strip().lower()+".txt"
                else :
                    name = cmd[1].strip().lower()
                currentPath[-1].child.addWithSort(NodeFile(name))
        else:
            print('Invalid Syntax!')

    elif cmd[0].strip().lower() == 'ls':
        # funtion untuk print semua item di dalam directory
        if cmd.__len__() == 1:
            # print all ascending
            print_children(currentPath[-1])
        else:
            if cmd[1].strip().split(" ")[0] == '-r':
                # print all descending
                print_children(currentPath[-1],0,1)
            elif cmd[1].strip().split(" ")[0] == '-file':
                # print file type only
                if cmd[1].strip().split(" ").__len__() > 1 and cmd[1].strip().split()[1].strip() == '-r':
                    # descending
                    print_children(currentPath[-1],2,1)
                else:
                    # ascending
                    print_children(currentPath[-1],2,0)
            elif cmd[1].strip().split(" ")[0] == '-folder':
                # print folder type only
                if cmd[1].strip().split().__len__() > 1 and cmd[1].strip().split()[1].strip() == '-r':
                    # descending
                    print_children(currentPath[-1],1,1)
                else:
                    # ascending
                    print_children(currentPath[-1],1,0)
            elif cmd[1].strip().split(" ")[0] == '-structure':
                # print secara structure tree logic di proyek.py
                print_structure(currentPath[-1])
            elif cmd[1].strip().split(" ")[0] == '-type':
                # print secara sort by type
                currentPath[-1].child.sortByType()
            elif cmd[1].strip().split(" ")[0] == '-group':
                # print secara sort by group
                currentPath[-1].child.groupBy()
            else : 
                print('salah syntax ls')

    elif cmd[0].strip().lower() == 'mv':
        # function untuk move menerima nama file/folder/zip dan path lokasi yg dituju
        # pertama akan mengubah string dari lokasi yang dituju menjadi sebuah list/path 
        # lalu mendapatkan node melalui nama dari children
        # melakukan pengecekkan apakah valid/tidak lalu apakah syntax benar tidak?
        # lalu menggunakan function move di proyek.py
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Cannot Move Drive!!')
            if cmd[1].strip().split(" ").__len__() == 1:
                print('syntax tidak valid')
            else:
                temp = cmd[1].strip().split(" My Computer\\")
                if temp.__len__() == 1:
                    print('invalid path name(use path from My Computer)')
                    continue
                arr = ['My Computer']
                arrTemp = temp[1].strip().split("\\")
                nodes = currentPath[-1].child.getNode(temp[0].strip())
                if nodes == None:
                    print('File/folder tidak ada!')
                    continue
                for i in arrTemp:
                    arr.append(i.strip().upper())
                tujuan = tree.getNodeByPath(arr)
                if tujuan == None:
                    print('Folder tujuan tidak ada!')
                elif type(tujuan) == NodeFile:
                    print('Tidak bisa masuk ke File!')
                elif type(tujuan) == NodeZip:
                    print('Tidak bisa masuk ke Zip!')
                else:
                    move(currentPath[-1],nodes,tujuan)
        else:
            print('invalid syntax')

    elif cmd[0].strip().lower() == 'cp':
        # function untuk copy menerima nama file/folder/zip dan path lokasi yg dituju
        # pertama akan mengubah string dari lokasi yang dituju menjadi sebuah list/path 
        # lalu mendapatkan node melalui nama dari children
        # melakukan pengecekkan apakah valid/tidak lalu apakah syntax benar tidak?
        # lalu menggunakan function copy di proyek.py
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Cannot copy Drive!!')
            if cmd[1].strip().split(" ").__len__() == 1:
                print('syntax tidak valid')
            else:
                temp = cmd[1].strip().split(" My Computer\\")
                if temp.__len__() == 1:
                    print('invalid path name(use path from My Computer)')
                    continue
                arr = ['My Computer']
                arrTemp = temp[1].strip().split("\\")
                nodes = currentPath[-1].child.getNode(temp[0].strip())
                if nodes == None:
                    print('File/folder tidak ada!')
                    continue
                for i in arrTemp:
                    arr.append(i.strip().upper())
                tujuan = tree.getNodeByPath(arr)
                if tujuan == None:
                    print('Folder tujuan tidak ada!')
                elif type(tujuan) == NodeFile:
                    print('Tidak bisa masuk ke File!')
                elif type(tujuan) == NodeZip:
                    print('Tidak bisa masuk ke Zip!')
                else:
                    if tujuan == currentPath[-1]:
                        copypaste(copy(nodes), tujuan,nodes.name+"-copy")
                    else:
                        copypaste(copy(nodes), tujuan,nodes.name)
        else:
            print('Invalid Syntax!')
    
    elif cmd[0].strip().lower() == 'rename':
        # function untuk rename menerima nama lama dan nama baru
        # memanggil function pada proyek.py untuk merename lalu di sort di dll(child)
        if cmd.__len__() > 1:
            temp = cmd[1].strip().split(":")
            nodeRename = currentPath[-1].child.getNode(temp[0].strip())
            currentPath[-1].child.renameThenSort(nodeRename, temp[1].strip())
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'zip':
        # function zip menerima beberapa folder/file yang mau di zip lalu nama hasil zipnya
        # beberapa file yg mau dizip di gabung / masukkan ke list
        # lalu memanggil constructor object NodeZip dari proyek.py
        # lalu memasukkan semua file dalma list ke nodeZip tersebut
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Can\'t Zip drive')
            else:
                temp = cmd[1].strip().split(":")
                if temp.__len__() == 1:
                    print('syntax zip salah, liat help untuk pembantu!')
                    continue
                zipped = temp[0].strip().split(",")
                listOfZip =[]
                for i in zipped:
                    getNode = currentPath[-1].child.getNode(i.strip())
                    if getNode not in listOfZip and getNode is not None:
                        listOfZip.append(getNode)
                node = NodeZip(temp[1].strip())
                node.addZip(listOfZip)
                currentPath[-1].child.addWithSort(node)
        else:
            print('Invalid Syntax')
    
    elif cmd[0].strip().lower() == 'unzip':
        # function unzip logic menerima file zip dan  fixed path (tempat unzipnya)
        # lalu memmanggil function unzip yang sudah dibuat di proyek.py
        if cmd.__len__() > 1:
            temp = cmd[1].strip().split(" My Computer\\")
            if temp.__len__() == 1:
                print('invalid path name(use path from My Computer)')
                continue
            arr = ['My Computer']
            arrTemp = temp[1].strip().split("\\")
            nodes = currentPath[-1].child.getNode(temp[0].strip())
            if nodes == None:
                print('File/folder tidak ada!')
                continue
            for i in arrTemp:
                arr.append(i.strip().upper())
            tujuan = tree.getNodeByPath(arr)
            if tujuan == None:
                print('Folder tujuan tidak ada!')
            elif type(tujuan) == NodeFile:
                print('Tidak bisa masuk ke File!')
            elif type(tujuan) == NodeZip:
                print('Tidak bisa masuk ke Zip!')
            elif type(tujuan) == NodeRoot:
                print('Tidak bisa masuk ke My Computer')
            else:
                unzip(nodes,tujuan)
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'del':
        # function untuk delete (folder cmn buang folder aja)
        # logic mengambil node berdasarkan name lalu menggunakan function delete pada proyek.py
        if cmd.__len__() > 1:
            node = currentPath[-1].child.getNode(cmd[1].strip())
            if node is None:
                print('tidak ada File/Folder')
            elif type(node) == NodeFile or type(node) == NodeZip:
                currentPath[-1].child.deleteByName(cmd[1].strip())
            elif type(node) == NodeFolder:
                deleteFolderOnly(currentPath[-1],node)
            else:
                print('Drive tak bisa dihapus')
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'delall':
        # function untuk delete all (folder dihapus sama isinya)
        # logic mengambil node berdasarkan name lalu menggunakan function delete pada proyek.py
        if cmd.__len__() > 1:
            node = currentPath[-1].child.getNode(cmd[1].strip())
            if node is None:
                print('tidak ada File/Folder')
            elif type(node) == NodeFile or type(node) == NodeZip:
                currentPath[-1].child.deleteByName(cmd[1].strip())
            elif type(node) == NodeFolder:
                deleteFolderAll(currentPath[-1],node)
            else:
                print('Drive tak bisa dihapus')
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'vp':
        # function buat view path
        # logic get node lalu gunakan function di tree dari proyek.py
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                node = currentPath[-1].dict[cmd[1].strip()]
            else:
                node = currentPath[-1].child.getNode(cmd[1].strip())
            if node is not None:
                tree.printPath(node)
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'vd':
        # function buat view data
        # logic get node lalu gunakan function di tree dari proyek.py
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                node = currentPath[-1].dict[cmd[1].strip()]
            else:
                node = currentPath[-1].child.getNode(cmd[1].strip())
            if node is not None:
                tree.getDetail(node)
        else:
            print('Invalid Syntax')

    elif cmd[0].strip().lower() == 'vt':
        if cmd.__len__() > 1:
            if currentPath[-1] == tree.root:
                print('Can\'t view type in My Computer')
            else:
                vt = cmd[1].strip()
                currentPath[-1].child.viewByType(vt)
        else:
            print('Invalid Syntax')

    else:
        print('\''+cmd[0].strip()+'\' is not a recognizable command!')
