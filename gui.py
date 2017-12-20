import sys,copy
import traceback
import processFile
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QHeaderView,QGraphicsView,QGraphicsScene,QGraphicsWidget
from ImageViewerQt import ImageViewerQt

"""
QtWidgets Window class
"""
class Window(QtWidgets.QWidget):
    """
    constructor for the class
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    """
    initialise GUI, add all GUI elements to the main window.
    Connect buttons to corresponding event handler.
    """
    def init_ui(self):

            self.processedDataCopy = {}
            self.rawTextDataCopy = []
            self.transitionFlag = 0

            # A text field for entering path of data file
            self.dataPathTextBox = QtWidgets.QLineEdit(self)
            self.dataPathTextBox.move(25,14)
            self.dataPathTextBox.resize(284,30)

            # Choose a file by clicking this button
            self.fileButton = QtWidgets.QPushButton(self)
            self.fileButton.setText("Choose")
            self.fileButton.resize(102,30)
            self.fileButton.clicked.connect(self.openFileNameDialog)
            self.fileButton.move(320,14)

            # start button, for applying page rank algorithm
            self.startButton = QtWidgets.QPushButton(self)
            self.startButton.setText('Start')
            self.startButton.resize(102,30)
            self.startButton.move(430,14)
            self.startButton.clicked.connect(self.start)

            # Refresh button, for updating page rank according to deleted nodes and added edges
            self.refreshButton = QtWidgets.QPushButton(self)
            self.refreshButton.setText('Refresh')
            self.refreshButton.resize(102,30)
            self.refreshButton.move(537,14)
            self.refreshButton.clicked.connect(self.refresh)

            # Revert button, to undo all changes in graph.
            self.revertButton = QtWidgets.QPushButton(self)
            self.revertButton.setText('Revert')
            self.revertButton.resize(102,30)
            self.revertButton.move(47,49)
            self.revertButton.clicked.connect(self.revert)

            # Delete nodes in the web graph.
            self.deleteButton = QtWidgets.QPushButton(self)
            self.deleteButton.setText('Delete Node')
            self.deleteButton.resize(102,30)
            self.deleteButton.move(157,49)
            self.deleteButton.clicked.connect(self.deleteNode)

            # Indicate the node to be deleted.
            self.deleteNodeTextBox = QtWidgets.QLineEdit(self)
            self.deleteNodeTextBox.move(264,49)
            self.deleteNodeTextBox.resize(45,30)

            # Button for setting transition gif, which indicates the iteration in the page rank algorithm
            self.transitionButton = QtWidgets.QPushButton(self)
            self.transitionButton.setText('Transition')
            self.transitionButton.resize(102,30)
            self.transitionButton.move(320,49)
            self.transitionButton.clicked.connect(self.transition)

            # Button to add an edge between to nodes, according to input in text box
            self.addEdgeButton = QtWidgets.QPushButton(self)
            self.addEdgeButton.setText('Add Edge')
            self.addEdgeButton.resize(102,30)
            self.addEdgeButton.move(430,49)
            self.addEdgeButton.clicked.connect(self.addEdge)

            # Enter from node in this text field
            self.edgeNode1TextBox = QtWidgets.QLineEdit(self)
            self.edgeNode1TextBox.move(537,49)
            self.edgeNode1TextBox.resize(45,30)

            # Enter to node in this text field
            self.edgeNode2TextBox = QtWidgets.QLineEdit(self)
            self.edgeNode2TextBox.move(584,49)
            self.edgeNode2TextBox.resize(45,30)

            # Label for adding image/transition image
            self.imageLabel = QtWidgets.QLabel(self)
            self.imageLabel.move(25,94)
            self.imageLabel.setFixedSize(656,364)
            self.imageLabel.setStyleSheet("border: 1px solid black")

            # List the page rank value of all nodes in the web graph
            self.rankTable = QtWidgets.QTableWidget(self)
            self.rankTable.move(25,463)
            self.rankTable.setFixedSize(656,130)
            self.rankTable.setStyleSheet("border: 1px solid black")

            # Make window visible
            self.show()

    """
    Open a dialog box, for choosing a data file containing the
    nodes and corresponding connections.
    Set the text of dataPathTextBox to the absolute path of the choosen file.
    """
    def openFileNameDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
                self.dataPathTextBox.clear()
                self.dataPathTextBox.setText(fileName)

    """
    Run the page rank algorithm, input from the choosen file.
    layoutFlag is set to 1, so as to form the process all links and add them to a dictionary.
    Refer to processFile.py for further details.
    """
    def start(self):
        try:
            processFile.layoutFlag=1

            processFile.main(self.dataPathTextBox.displayText(),0,'/home/subhadip/PageRankTester/Images/','/home/subhadip/PageRankTester/Final_images/')
            pixmap_staticImage = QtGui.QPixmap()
            pixmap_staticImage.load('Final_images/g1.png')
            self.createTable()
            self.imageLabel.setPixmap(pixmap_staticImage)
            self.processedDataCopy = copy.deepcopy(processFile.processed_Data_Dictionary)
            self.rawTextDataCopy = copy.deepcopy(processFile.rawTextData)
        except Exception:
            traceback.print_exc()
            print('Error')

    """
    Apply page rank after updating the graph by deleting nodes or adding edges,
    The node dictionary is not created again, since we have updated the node dictionary while deleting nodes/adding edges.
    Next set the new web graph visualisation.
    Add the web graph visualisation and page rank table to the GUI.Update the page rank table.
    """
    def refresh(self):
        processFile.layoutFlag = 0
        processFile.plotNum = 1
        processFile.x = 1
        try:
            processFile.main(self.dataPathTextBox.displayText(),1,'/home/subhadip/PageRankTester/Images/','/home/subhadip/PageRankTester/Final_images/')
            self.imageLabel.clear()
            pixmap_staticImage = QtGui.QPixmap()
            pixmap_staticImage.load('Final_images/g6.png')
            self.imageLabel.setPixmap(pixmap_staticImage)
            self.createTable()
        except Exception:
            traceback.print_exc()
            print('error1')

    """
    Add a new adge in the existing web graph.
    Update processed_Data_Dictionary, by adding the toNode (value), appending the same to the list
    corresponding to the fromNode key.
    """
    def addEdge(self):
        try:
            fromEdge = self.edgeNode1TextBox.displayText()
            toEdge = self.edgeNode2TextBox.displayText()
            if fromEdge !='' and toEdge !='':
                    processFile.processed_Data_Dictionary[fromEdge].append(toEdge)
                    processFile.rawTextData.append([fromEdge,toEdge])
                    print(processFile.processed_Data_Dictionary)
        except Exception:
            traceback.print_exc()
            print('Refresh Error : add edge')

    """
    Remove all instances of the node to be deleted from processed_Data_Dictionary.
    Delete all edges which contain this node.
    """
    def deleteNode(self):
        nodeToBeDeleted = self.deleteNodeTextBox.displayText()
        processFile.deletedNodesList.append(nodeToBeDeleted)
        try:

            #delete from rawdatafile also
            processFile.processed_Data_Dictionary[nodeToBeDeleted] = []
            for node in processFile.processed_Data_Dictionary:
                if nodeToBeDeleted in processFile.processed_Data_Dictionary[node]:
                    processFile.processed_Data_Dictionary[node].remove(nodeToBeDeleted)
            print(processFile.processed_Data_Dictionary)

            #list of edges to be deleted.
            edgesToBeDeleted = []
            for edge in processFile.rawTextData:
                if nodeToBeDeleted in edge:
                    print(edge)
                    edgesToBeDeleted.append(edge)

            #remove edges from rawTextData
            for edge in edgesToBeDeleted:
                processFile.rawTextData.remove(edge)
            print(processFile.rawTextData)
        except Exception:
            traceback.print_exc()

    """
    Add values to the page rank table, containing
    node number, node URL and corresponding page rank.
    """
    def createTable(self):

        #List of nodes in the graph excluding the deleted nodes
        newNodeList = []
        table = {'Node Number':[],'Node Name':[],'Page Rank':[]}

        #Create newNodeList and table[Node Number], value list
        for node in processFile.nodeList:
            if len(processFile.deletedNodesList)==0 or node not in processFile.deletedNodesList:
                newNodeList.append(node)
                table['Node Number'].append(node)

        #List containg the URL of the nodes.
        nodeNameList = []
        nodePageRankValueList = []
        for node in newNodeList:
            table['Node Name'].append(processFile.linkToNum[int(node)])
            table['Page Rank'].append(processFile.rankMatrix[int(node)][0])

        self.rankTable.setRowCount(len(newNodeList))
        self.rankTable.setColumnCount(3)

        horHeaders = []
        #Create the table, also set the column headers
        for n, key in enumerate(['Node Number','Node Name','Page Rank']):
            horHeaders.append(key)
            for m, item in enumerate(table[key]):
                newitem = QtWidgets.QTableWidgetItem(str(item))
                self.rankTable.setItem(m, n, newitem)

        #Add Header
        self.rankTable.setHorizontalHeaderLabels(horHeaders)

        #Adjust size of Table
        self.rankTable.resizeRowsToContents()
        self.rankTable.setColumnWidth(0,200 )
        self.rankTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    """
    Undo all changes in the web graph in terms of edge additions or node deletions.
    Refresh the web graph.
    """
    def revert(self):
        processFile.processed_Data_Dictionary = self.processedDataCopy
        processFile.deletedNodesList = []
        processFile.rawTextData = self.rawTextDataCopy
        self.refresh()

    """
    Display a static visualisation corresponding to the final graph (.png image),
    or visualise the formation of the web graph (changes in page rank of nodes)
    using a gif image.
    """
    def transition(self):
        if self.transitionFlag==0:
            self.imageLabel.clear()
            movie = QtGui.QMovie("movie2.gif")
            self.imageLabel.setMovie(movie)
            movie.start()
            self.transitionFlag = 1
        else:
            self.imageLabel.clear()
            pixmap_staticImage = QtGui.QPixmap()
            pixmap_staticImage.load('Final_images/g6.png')
            pixmap_staticImage = pixmap_staticImage.scaled(656,353)
            self.imageLabel.setPixmap(pixmap_staticImage)
            self.transitionFlag = 0



app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.setWindowTitle('Page Rank Analyser')
a_window.setFixedSize(707,603)
sys.exit(app.exec_())
