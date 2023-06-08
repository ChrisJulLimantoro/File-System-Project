#Library copy untuk copy file agar reference berbeda
from copy import copy
from collections import OrderedDict
#Leo
class NodeFolder:
    def __init__(self, name):
        self.name= name
        #child disimpan dalam bentuk Double link list
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Folder Name:", self.name)

#CJ
class NodeDrive:
    def __init__(self, name, authName):
        #pengecekan untuk nama drive hanya boleh 1 karakter saja dan antara A-Z
        if (len(name) > 1 or (ord(name[0]) < 65 and ord(name[0]) > 90)):
            print('failed disk name invalid')
            self.status= False
            return
        self.child= DoubleLinkedList()
        self.auth= authName
        self.name= name+":"
        self.next= None
        self.prev= None
        self.status= True
    #Hanya bisa rename nama authornya saja, tidak bisa nama drivenya
    def rename(self, newName):
        self.auth= newName
    
#cj and Leo
class NodeZip:
    def __init__(self, name):
        self.name= name
        self.type= "zip"
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
    #inisialisasi isi dari zip yang sudah dibuat. listOfChild dalam bentuk array
    def addZip(self,listOfChild):
        for i in listOfChild:
            #jika node File maka langsung copy menggunakan library
            if type(i) == NodeFile:
                self.child.addWithSort(copy(i))
            #jika bukan, maka copy menggunakan method copyAll yang dibuat agar anak" dari folder tidak reference copy
            elif type(i) == NodeFolder:
                self.child.addWithSort(copyAll(i,NodeFolder(i.name)))
            else :
                self.child.addWithSort(copyAll(i,NodeZip(i.name)))
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Name:", self.name)
        print("Type:", self.type)
    
#Leo
class NodeFile:
    def __init__(self,name):
        self.name= name
        indexType= searchTypeOfFile(self.name)
        self.type=self.name[indexType:]
        self.next= None
        self.prev= None
    #ketika rename bisa juga tipe file diperbarui juga
    def rename(self, newName):
        self.name=newName
        indexType= searchTypeOfFile(self.name)
        self.type= self.name[indexType:]
    def getDetail(self):
        print("File Name:", self.name)
        print("File Type:", self.type)

class NodeRoot:
    def __init__(self):
        self.name = "My Computer"
        self.dict = dict()
    
    def add(self,node:NodeDrive):
        if node.name in self.dict:
            print('Drive dengan nama '+node.name+' sudah ada!')
            return
        self.dict[node.name] = node
        # pakai library untuk sorting dictionary!
        self.dict = OrderedDict(sorted(self.dict.items()))
    
    def get(self,name):
        return self.dict[name]

class DoubleLinkedList:
    def __init__(self):
        self.head= None
        self.tail= None
        self.size=0

    #fungsi untuk mereturn node berdasarkan sebuah nama di parameter
    #jadi dicari node mana yang memiliki nama sesuai parameter
    #ketika ditemukan maka direturn
    def getNode(self, name):
        iter= self.head
        for i in range(self.size):
            if iter.name.lower() == name.lower():
                return iter
            iter= iter.next
        print("Tidak ditemukan")


    #function rename terus disort lagi setelah direname
    def renameThenSort(self, node: NodeFolder or NodeFile or NodeZip, newName):

        #kalau nodeDrive yang direname adalah auth nya
        if type(node)== NodeDrive:
            adaYangSama= False
            iter= self.head
            #dicari apakah newnName ini ada sama apa tidak dengan nama di dalam dir itu
            for i in range(self.size):
                if iter.auth.lower()== newName.lower():
                    adaYangSama= True
                    break
                iter= iter.next
            #jika ada yang sama tidak bisa direname
            if adaYangSama:
                print("Nama yang anda inputkan tidak valid, ada yang sama!")
            else:
                iter= self.head
                for i in range(self.size):
                    if iter.auth.lower()== node.auth.lower():
                        break
                    iter= iter.next
                
                #jadi logikanya, kita hapus terlebih dahulu node yang akan direname dari link list

                #ketika ukuran link list 1
                if self.size==1:
                    self.head= None
                    self.prev= None
                #ketika node yang direname adalah head
                elif iter== self.head:
                    self.head= iter.next
                    self.head.prev= None
                    iter.next= None
                    iter.prev= None
                #ketika node yang direname adalah tail
                elif iter== self.tail:
                    self.tail= iter.prev
                    self.tail.next= None
                    iter.next= None
                    iter.prev= None
                #ketika node yang direname ada di tengah"
                else:
                    iter.prev.next= iter.next
                    iter.next.prev= iter.prev
                    iter.next= None
                    iter.prev= None

                iter.rename(newName)
                self.size-=1
                self.addWithSort(iter)
        
        #kalau node lain yaitu namanya
        #logic sama
        else:
            adaYangSama= False
            iter= self.head
            for i in range(self.size):
                if iter.name.lower()== newName.lower():
                    adaYangSama= True
                    break
                iter= iter.next
            if adaYangSama:
                print("Nama yang anda inputkan tidak valid, ada yang sama!")
            else:
                iter= self.head
                for i in range(self.size):
                    if iter.name.lower()== node.name.lower():
                        break
                    iter= iter.next
                if self.size==1:
                    self.head= None
                    self.prev= None
                elif iter== self.head:
                    self.head= iter.next
                    self.head.prev= None
                    iter.next= None
                    iter.prev= None
                elif iter== self.tail:
                    self.tail= iter.prev
                    self.tail.next= None
                    iter.next= None
                    iter.prev= None
                else:
                    iter.prev.next= iter.next
                    iter.next.prev= iter.prev
                    iter.next= None
                    iter.prev= None

                iter.rename(newName)
                self.size-=1
                self.addWithSort(iter)

     #fungsi add child kemudian langsung disort secara ascending
    def addWithSort(self, node: NodeFolder or NodeFile or NodeZip or NodeDrive):
        iter= self.head
        canAdd= True
         #pengecekan apakah nama dari node yang diinput itu sudah ada atau belum di directory itu
        for i in range(self.size):
            if iter.name.lower()== node.name.lower():
                canAdd= False
                break
            iter= iter.next
        
        #jika tidak ada maka bisa add
        if canAdd:

            #kondisi ketika jumlah datanya masih 0
            if self.size==0:
                self.head= node
                self.tail= node
            
            #kondisi ketika jumlah data 1
            elif self.size==1:
                #ketika data yang sekarang ini lebih besar dari inputan, maka inputan akan jadi head
                if self.head.name.lower() > node.name.lower():
                    node.next = self.head
                    self.head.prev = node
                    self.head = node
                #sebaliknya
                else:
                    node.prev = self.head
                    self.head.next = node
                    self.tail = node
            else:
                iter= self.head
                loop=0
                while loop<self.size:
                    if iter.name.lower() > node.name.lower():
                        break
                    loop+=1
                    iter= iter.next
                
                 #jika node yang diinput lebih kecil daripada head, maka akan jadi head
                if loop==0:
                    node.next= self.head
                    self.head.prev= node
                    self.head= node
                
                 #jika node yang diinput adalah node paling besar, maka akan jadi tail
                elif loop== self.size:
                    node.prev= self.tail
                    self.tail.next= node
                    self.tail= node
                
                #ketika di tengah
                else:
                    iter.prev.next= node
                    node.next= iter
                    node.prev= iter.prev
                    iter.prev = node
            self.size += 1
        else:
            print("Ada data yang sama")
    

    #DELETE
    #fungsi delete berdasarkan name
    def deleteByName(self, name):
        cek = False
        iter = self.head
        if self.size == 0:
            print("kosong")
        else:
            for i in range(self.size):
                if iter.name.lower() == name.lower():
                    cek = True
                    if self.head == self.tail:
                        self.head = self.tail = None
                    elif iter == self.head:
                        self.head = self.head.next
                        self.head.prev = None
                    elif iter == self.tail:
                        self.tail = self.tail.prev
                        self.tail.next = None
                    else:
                        iter.prev = temp
                        temp.next = iter.next
                    self.size -= 1
                temp = iter
                iter = iter.next

            # kondisi ketika tidak ditemukan data
            if not cek and self.size != 0:
                print("Tidak ada data dengan nama", name)


    def printAsc(self):
        iter= self.head
        #tinggal print biasa, karena data sudah disimpan secara ascending
        for i in range(self.size):
            if type(iter)== NodeDrive:
                print(" > "+iter.auth+"("+iter.name+")")
            elif type(iter)== NodeFolder or type(iter)== NodeZip:
                print(" > "+iter.name)
            else :
                print(" - "+iter.name)
            iter= iter.next
    def printDesc(self):
        iter= self.tail
        #print dari tail
        for i in range(self.size):
            if type(iter)== NodeDrive:
                print(" > "+iter.auth+"("+iter.name+")")
            elif type(iter)== NodeFolder or type(iter)== NodeZip:
                print(" > "+iter.name)
            else :
                print(" - "+iter.name)
            iter= iter.prev
    
    #jadi semua ditampilkan tapi disorting berdasarkan typenya
    def sortByType(self):
        arrFolder= []
        arrFile= []
        iter= self.head
        for i in range(self.size):
            #jika folder maka diappend ke arrFolder
            if type(iter) is NodeFolder:
                arrFolder.append(iter)
            #kondisi ketika file
            else:
                #simpan index untuk dimasukkan ke arrFile
                index=0
                for i in range(len(arrFile)):
                    if iter.type < arrFile[i].type:
                        break
                    index+=1
                arrFile.insert(index,iter)
            iter= iter.next
        for i in arrFolder:
            print(i.name)
        for i in arrFile:
            print(i.name)
    
    #untuk view type apa yang mau diview
    def viewByType(self, types):
        print("VIEW", types)
        count=0
        if types=="Folder" or types=="folder":
            iter= self.head
            for i in range(self.size):
                #dicari yang merupakan NodeFolder saja
                if type(iter) is NodeFolder:
                    count+=1
                    print(iter.name)
                iter= iter.next
        else:
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFile or type(iter) is NodeZip:
                    #dicari tipe file yang sesuai parameter
                    if iter.type == types:
                        count+=1
                        print(iter.name)
                iter= iter.next
        #kondisi ketika tidak ada
        if count==0:
            print(types, "tidak ditemukan di folder ini!")

    #menampilkan node zip saja
    def viewOnlyZip(self):
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeZip:
                print(iter.name)
            iter= iter.next
        print()

    #group by View
    def groupBy(self):
        #Folder first
        adaFolder= False
        iter= self.head
        #dicek apakah ada folder atau tidak
        for i in range(self.size):
            if type(iter) is NodeFolder:
                adaFolder= True
                break

        #jika ada tampilkan folder dulu
        if adaFolder:
            print("======== FOLDER ========")
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFolder:
                    print(iter.name)
                iter= iter.next

        #File
        #arr untuk menyimpan type apa saja yang sudah divisit
        visitedType=[]
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFile or type(iter) is NodeZip:
                if iter.type not in visitedType:
                    visitedType.append(iter.type)
                    print("========", iter.type.upper() , "========")
                    iter2= self.head
                    for j in range(self.size):
                        if type(iter2) is NodeFile or type(iter2) is NodeZip:
                            if iter2.type == iter.type:
                                print(iter2.name)
                        iter2= iter2.next
            iter=iter.next




class Tree:
    def __init__(self):
        self.root = NodeRoot()

    def add(self,node:NodeDrive):
        self.root.add(node)

    #CJ
    def findAll(self,node,name):
        #path dalam bentuk array string
        path = self.getPath(node)
        self.findAllUtil(name,node,path)
    
    #CJ
    def findAllUtil(self,name,node : NodeFolder,path):
        queue = []
        if node == self.root:
            # khusus untuk anak dari My Computer merupakan sebuah tree yang menyimpan anaknya di dictionary
            for i in node.dict:
                queue.append(node.dict[i])
        else:
            temp = node.child.head
            #Anak dari node dimasukkan semua ke queue
            while temp is not None:
                queue.append(temp)
                temp = temp.next
        while len(queue) > 0:
            #dicek dari awal
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                continue
            elif type(akses) == NodeFolder or type(akses) == NodeZip or type(akses) == NodeDrive:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                path.append(akses.name)
                #jika folder/ zip/ drive, kita rekursif lagi untuk dicek anak"nya. Jika file tidak usah rekursif
                self.findAllUtil(name,akses,path)
        #untuk mundur
        path.pop(-1)

    #LELE
    def getPath(self,node:NodeFolder or NodeFile or NodeZip or NodeDrive or NodeRoot):
        if type(node) == NodeRoot:
            return [node.name]
        return self.getPathUtil(self.root,node,[])
    
    #CJ
    def getDetail(self, node: NodeFolder or NodeFile or NodeZip or NodeDrive):
        node.getDetail()
        print("Path: ", end="")
        self.printPath(node)
        print()

    #LELE
    def printPath(self,node:NodeFolder or NodeFile or NodeZip or NodeDrive or NodeRoot):
        if type(node) == NodeRoot:
            print(node.name,end="\\")
        else:
            for i in self.getPath(node):
                print(i,end="\\")

    #LELE
    #RETURN PATH DALAM BENTUK ARRAY STRING
    def getPathUtil(self,node,search,path):
        #jika yang disearch adalah root, maka lgsg return
        if search == self.root:
            return [self.root.name]
        path.append(node.name)
        queue = []
        if node == self.root:
            # khusus untuk anak dari My Computer merupakan sebuah tree yang menyimpan anaknya di dictionary
            for i in node.dict:
                queue.append(node.dict[i])
        else:
            temp = node.child.head
            #Anak dari node dimasukkan semua ke queue
            while temp is not None:
                queue.append(temp)
                temp = temp.next
        while len(queue) > 0:
            #dipop dari awal untuk dicek anaknya
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses == search:
                    path.append(akses.name)
                    return path
                
            if type(akses) == NodeFolder or type(akses) == NodeDrive or type(akses) == NodeZip:
                if akses == search:
                    path.append(akses.name)
                    return path
                else:
                    #jika bukan, kita rekursif lagi untuk dicek anaknya lagi
                    hasil = self.getPathUtil(akses,search,path)
                    if(type(hasil) == list):
                        return hasil
        #jika buntu, maka mundur
        path.pop(len(path)-1)
        return

    #CJ
    def getNodeByPath(self, path):
        nodeHasil= self.root
        for i in path[1:]:
            if i.__len__() == 2 and i[1] == ':':
                nodeHasil = nodeHasil.dict[i]
            else:
                if nodeHasil == None:
                    print('tidak ada folder tersebut!')
                    break
                nodeHasil= nodeHasil.child.getNode(i)
        return nodeHasil




#MAIN FUNCTION

#LEO
#fungsi untuk mencari posisi titik paling akhir untuk mendetect posisi tipe file
def searchTypeOfFile(fileName):
    indexType=0
    for i in fileName[::-1]:
        if i == ".":
            break
        indexType += 1
    return len(fileName)-indexType


#CJ
def print_structure(node:NodeFolder or NodeDrive or NodeZip or NodeRoot,lvl = 1):
    #kondisi ketika node yang dicek adalah folder atau zip
    if type(node) == NodeFolder or NodeZip:
        print('> '+node.name)
    #kondisi ketika node yang dicek adalah drive
    elif type(node) == NodeDrive:
        print('> '+node.auth+' ('+node.name+')')
    #pengecekan anak" dari node parameter
    if type(node) == NodeRoot:
        for i in node.dict:
            for j in range(lvl):
                print('    ',end="")
            print_structure(node.dict[i],lvl+1)
    else:
        temp = node.child.head
        if temp != None:
            while temp != None:
                #untuk spacing levelnya
                for i in range(lvl):
                    print('    ',end="")
                #jika node file
                if type(temp) == NodeFile:
                    print('- '+temp.name)
                #jika folder atau drive atau zip, direkursif masuk lagi kemudian levelnya ditambah 1
                else:
                    print_structure(temp,lvl+1)
                temp = temp.next

#FUNCTION PRINT_PATH
#CJ
def print_path(path):
    for i in range(len(path)):
        if i == len(path)-1:
            print(path[i].name, end="> ")
        else:
            print(path[i].name, end="\\")

#CJ
def print_children(node:NodeFolder or NodeDrive or NodeRoot,tipe = 0,status=0):
    # print khusus root
    if type(node) == NodeRoot:
        # gausa liak tipe karena di root hanya ada drive
        if node.dict.__len__() == 0:
            print('Masih Kosong!')
        elif tipe == 1 or tipe == 2:
            print('tidak ada file/folder')
        else:
            if status == 0:
                for i in node.dict:
                    print(" - "+node.dict[i].auth + "("+node.dict[i].name+")")
            else:
                for i in reversed(node.dict):
                    print(" - "+node.dict[i].auth + "("+node.dict[i].name+")")
    else:
        # print untuk selain root
        #STATUS 0 -> ASCENDING
        if status == 0:
            temp = node.child.head
        #STATUS 1 -> DESCENDING
        else :
            temp = node.child.tail
        if temp == None:
            print('Folder masih kosong!')
        else:
            while temp != None:
                #TIPE 0 -> PRINT SEMUA
                if tipe == 0:
                    if type(temp) == NodeDrive:
                        print(" - "+temp.auth+"("+temp.name+")")
                    else:
                        print(" - "+temp.name)
                elif tipe == 1:
                    #PRINT FOLDER, DRIVE, DAN ZIP
                    if type(temp) == NodeFolder or type(temp) == NodeDrive or type(temp) == NodeZip:
                        if type(temp) == NodeDrive:
                            print(" - "+temp.auth+"("+temp.name+")")
                        else:
                            print(" - "+temp.name)

                #FILE SAJA
                elif tipe == 2:
                    if type(temp) == NodeFile:
                        print(" - "+temp.name)
                if status == 0:
                    temp = temp.next
                else : 
                    temp = temp.prev
                
#LEO
#fungsi untuk move folder, file, atau zip
#nodeparent: nodeparent dari node yang dimove
#nodePindah: node yang akan dipindah
#nodeParentTujuan: tempat node akan dipindah
def move(nodeParent: NodeFolder,nodePindah: NodeFolder or NodeFile or NodeZip, nodeParentTujuan: NodeFolder):
    if type(nodePindah) == NodeFile:
        temp= copyAll(nodePindah,NodeFile(nodePindah.name))
    elif type(nodePindah) == NodeFolder:
        temp= copyAll(nodePindah,NodeFolder(nodePindah.name))
    elif type(nodePindah) == NodeZip:
        temp= copyAll(nodePindah,NodeZip(nodePindah.name))
    nodeParent.child.deleteByName(nodePindah.name)
    nodeParentTujuan.child.addWithSort(temp)


#LEO
#fungsi untuk melakukan copy paste
# nodeCopy: node yang akan dicopy
# nodeParentDest: node Parent tempat dipaste      
def copypaste(nodeCopy: NodeFolder or NodeFile or NodeZip, nodeParentDest: NodeFolder,name):
    #jika file kita langsung gunakan library copy
    if type(nodeCopy) == NodeFile:
        newNode = NodeFile(name)
        nodeParentDest.child.addWithSort(newNode)
        return
    
    #jika folder kita gunakan CopyAll
    elif type(nodeCopy) == NodeFolder:
        newNode= copyAll(nodeCopy,NodeFolder(name))
        nodeParentDest.child.addWithSort(newNode)
        return
    
     #Zip copy all juga
    else :
        newNode= copyAll(nodeCopy,NodeZip(name))
        nodeParentDest.child.addWithSort(newNode)
        return

#CJ
#FUNCTION COPY UNTUK MEMBEDAKA REFERENCE AWAL DENGAN REFERENCE HASIL  
def copyAll(node:NodeFolder or NodeZip,hasil:NodeFolder or NodeZip):
    queue = []
    if type(node) == NodeDrive or type(node) == NodeRoot:
        print('Can\'t copy Drive or My Computer')
    temp = node.child.head
    #DIAMBIL ANAKNYA SEMUA
    while temp is not None:
        queue.append(temp)
        temp = temp.next
    

    while queue.__len__() > 0:
        now = queue.pop(0)
        #JIKA NODE FILE
        if type(now) == NodeFile:
            hasil.child.addWithSort(NodeFile(now.name))
        #JIKA NODE FOLDER
        elif type(now) == NodeFolder:
            newFolder = NodeFolder(now.name)
            #TIAP ANAKNYA DIREKURSIF LAGI AGAR REFERENCE BERBEDA
            newFolder = copyAll(now,newFolder)
            hasil.child.addWithSort(newFolder)
        else :
            newZip = NodeZip(now.name)
            #TIAP ANAKNYA DIREKURSIF LAGI AGAR REFERENCE BERBEDA
            newZip = copyAll(now,newZip)
            hasil.child.addWithSort(newZip)
    #return NODE
    return hasil

#LEO
#fungsi delete Folder only
#nodeParentOfFoler: node Parent dari folder yang didelete
#nodeDeleted: node Folder yang mau dihapus
def deleteFolderOnly(nodeParentOfFolder: NodeFolder, nodeDeleted: NodeFolder):
    llDelete= nodeDeleted.child
    nodeParentOfFolder.child.deleteByName(nodeDeleted.name)
    iter= llDelete.head
    for i in range(llDelete.size):
        nodeParentOfFolder.child.addWithSort(iter)
        iter= iter.next

#LEO
def deleteFolderAll(nodeParent: NodeFolder, nodeDelete: NodeFolder):
    nodeParent.child.deleteByName(nodeDelete.name)
    

#CJ
def unzip(zipInput: NodeZip, NodeTujuan: NodeFolder or NodeDrive):
    iter= zipInput.child.head
    folder = NodeFolder(zipInput.name[0:-4])
    for i in range(zipInput.child.size):
        if type(iter) == NodeFile:
            hasil = NodeFile(iter.name)
        elif type(iter) == NodeFolder:
            hasil = NodeFolder(iter.name)
        elif type(iter) == NodeZip(iter.name):
            hasil = NodeZip(iter.name)
        folder.child.addWithSort(copyAll(iter,hasil))
        iter= iter.next
    NodeTujuan.child.addWithSort(folder)


# t = Tree()
# t.add(NodeDrive('E','New Volume'))
# t.add(NodeDrive('D','Data'))
# t.add(NodeDrive('C','Chris'))
# t.root.dict['C:'].child.addWithSort(NodeFolder('hi'))
# t.root.dict['D:'].child.addWithSort(NodeFolder('hello'))
# t.root.dict['D:'].child.head.child.addWithSort(NodeFile('hihihi.py'))
# t.root.dict['D:'].child.head.child.addWithSort(NodeFolder('hiha'))
# t.root.dict['D:'].child.head.child.addWithSort(NodeFile('hihihi.pdf'))
# t.root.dict['D:'].child.addWithSort(NodeFile('hi say.txt'))
# t.root.dict['E:'].child.addWithSort(NodeFile('hi mas.py'))
# path = ['My Computer','D:','hello']
# print_structure(t.getNodeByPath(path))
# print(t.getPath(t.root.dict['D:'].child.head.next))
# t.findAll(t.root,'hi')
