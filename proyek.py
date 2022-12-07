from copy import copy
class NodeFolder:
    def __init__(self, name):
        self.name= name
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Folder Name:", self.name)

class NodeZip:
    def __init__(self, name, listOfChild):
        self.name= name
        self.type= "zip"
        self.child= DoubleLinkedList()
        self.next= None
        self.prev= None
        # listOfChild isinya node
        for i in listOfChild:
            self.child.addWithSort(i)
    def rename(self, newName):
        self.name= newName
    def getDetail(self):
        print("Name:", self.name)
        print("Type:", self.type)
    

class NodeFile:
    def __init__(self,name):
        self.name= name
        indexType= searchTypeOfFile(self.name)
        self.type=self.name[indexType:]
        self.next= None
        self.prev= None
    def rename(self, newName):
        self.name=newName
        indexType= searchTypeOfFile(self.name)
        self.type= self.name[indexType:]
    def getDetail(self):
        print("File Name:", self.name)
        print("File Type:", self.type)


def searchTypeOfFile(fileName):
    indexType=0
    for i in fileName[::-1]:
        if i == ".":
            break
        indexType += 1
    return len(fileName)-indexType

class DoubleLinkedList:
    def __init__(self):
        self.head= None
        self.tail= None
        self.size=0

    def renameThenSort(self, node: NodeFolder or NodeFile or NodeZip, newName):
        iter= self.head
        for i in range(self.size):
            if iter.name== node.name:
                break
            iter= iter.next
        if iter== self.head:
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

    def addWithSort(self, node: NodeFolder or NodeFile or NodeZip):
        iter= self.head
        canAdd= True
        for i in range(self.size):
            if iter.name.lower()== node.name.lower():
                canAdd= False
                break

        if canAdd:
            if self.size==0:
                self.head= node
                self.tail= node
            elif self.size==1:
                if self.head.name.lower() > node.name.lower():
                    node.next = self.head
                    self.head.prev = node
                    self.head = node
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
                if loop==0:
                    node.next= self.head
                    self.head.prev= node
                    self.head= node
                elif loop== self.size:
                    node.prev= self.tail
                    self.tail.next= node
                    self.tail= node
                else:
                    iter.prev.next= node
                    node.next= iter
                    node.prev= iter.prev
                    iter.prev = node
            self.size += 1
        else:
            print("Ada data yang sama")

    def deleteByName(self, name):
        iter = self.head
        if self.size == 0:
            print("kosong")
        else:
            for i in range(self.size):
                if iter.name.lower() == name.lower():
                    if self.head == self.tail:
                        self.head = self.tail = None
                    elif iter == self.head:
                        self.head = self.head.next
                        self.head.prev = None
                    elif iter == self.tail:
                        self.tail= self.tail.prev
                        self.tail.next = None
                    else:
                        iter.prev = temp
                        temp.next = iter.next
                    self.size-=1
                temp = iter
                iter = iter.next

    def printAsc(self):
        iter= self.head
        for i in range(self.size):
            print(iter.name)
            iter= iter.next
    def printDesc(self):
        iter= self.tail
        for i in range(self.size):
            print(iter.name)
            iter= iter.prev
    def sortByType(self):
        arrFolder= []
        arrFile= []
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFolder:
                arrFolder.append(iter)
            else:
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

    def viewByType(self, types):
        print("VIEW", types)
        if types=="Folder" or types=="folder":
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFolder:
                    print(iter.name)
                iter= iter.next
        else:
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFile:
                    if iter.type == types:
                        print(iter.name)
                iter= iter.next

    def groupBy(self):
        #Folder first
        adaFolder= False
        iter= self.head
        for i in range(self.size):
            if type(iter) is NodeFolder:
                adaFolder= True
                break

        if adaFolder:
            print("======== FOLDER ========")
            iter= self.head
            for i in range(self.size):
                if type(iter) is NodeFolder:
                    print(iter.name)
                iter= iter.next
        #File
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
    def __init__(self,root = NodeFolder("PC")):
        self.root = root
    
    def findAll(self,node,name):
        path = self.getPath(node)
        self.findAllUtil(name,node,path)
    
    def findAllUtil(self,name,node : NodeFolder,path):
        queue = []
        temp = node.child.head
        while temp is not None:
            queue.append(temp)
            temp = temp.next
        while len(queue) > 0:
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                continue
            elif type(akses) == NodeFolder:
                if akses.name.__contains__(name):
                    for i in path :
                        print(i,end="\\")
                    print(akses.name)
                    path.append(akses.name)
                self.findAllUtil(name,akses,path)
        path.pop(len(path)-1)

    def getPath(self,node:NodeFolder or NodeFile or NodeZip):
        return self.getPathUtil(self.root,node,[])
    
    def getDetail(self, node: NodeFolder or NodeFile or NodeZip):
        node.getDetail()
        print("Path: ", end="")
        self.printPath(node)

    def printPath(self,node:NodeFolder or NodeFile or NodeZip):
        for i in self.getPath(node):
            print(i,end="\\")

    def getPathUtil(self,node,search,path):
        path.append(node.name)
        queue = []
        temp = node.child.head
        while temp is not None:
            queue.append(temp)
            temp = temp.next
        while len(queue) > 0:
            akses = queue.pop(0)
            if type(akses) == NodeFile:
                if akses == search:
                    path.append(akses.name)
                    return path
                
            if type(akses) == NodeFolder:
                if akses == search:
                    path.append(akses.name)
                    return path
                else:
                    hasil = self.getPathUtil(akses,search,path)
                    if(type(hasil) == []):
                        return hasil
        path.pop(len(path)-1)
        return

    def move(self,nodeParent: NodeFolder,nodePindah: NodeFolder or NodeFile or NodeZip, nodeParentTujuan: NodeFolder):
        temp= nodePindah
        nodeParent.child.deleteByName(nodePindah.name)
        nodeParentTujuan.child.addWithSort(temp)
    
    def copypaste(self, nodeCopy: NodeFolder or NodeFile or NodeZip, nodeParentDest: NodeFolder):
        newNode= copy(nodeCopy)
        nodeParentDest.child.addWithSort(newNode)

        
# if __name__ == '__main__':
    ll= DoubleLinkedList()
    node1= NodeFile("file1.docs")
    ll.addWithSort(node1)
    ll.addWithSort(NodeFolder("blabla"))
    ll.addWithSort(NodeFile("cicak.pdf"))
    ll.addWithSort(NodeFile("cicak.txt"))
    ll.addWithSort(NodeFile("blabla.xlsx"))
    ll.addWithSort(NodeFolder("babi"))
    ll.addWithSort(NodeFolder("Barbar"))
    ll.addWithSort(NodeFile("gas.pdf"))
    ll.addWithSort(NodeFile("babi.txt"))
    ll.addWithSort(NodeFile("zebra.txt"))
    ll.addWithSort(NodeZip("ok.zip",listOfChild=[NodeFile("blabla.pdf"), NodeFile("yyy.docs")]))

    # ll.deleteByName("file1.docs")

    ll.printAsc()
    print()
    # ll.printDesc()
    # print()
    # ll.sortByType()
    # print()
    ll.viewByType("xlsx")

    print()

    ll.groupBy()

# s = [5,4,3]
# print(s.pop(len(s)-1))
# t = Tree()
# file1= NodeFile("testing.pdf")
# t.root.child.addWithSort(file1)
# t.root.child.addWithSort(NodeFolder("Ayam Bakar"))
# t.root.child.addWithSort(NodeFolder("Ayam rujak"))
# t.root.child.addWithSort(NodeFolder("Ayam geprek"))
# t.root.child.head.child.addWithSort(NodeFolder("Ayam Bakar"))
# t.root.child.head.next.child.addWithSort(NodeFolder("Ayam Bakar"))
# # t.findAll(t.root.child.head,"Ayam")
# t.getDetail(file1)