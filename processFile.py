import os
import shutil
import sys
import numpy
import math
import random
import igraph
from scipy import sparse
from igraph import *


#store text file in a list
global rawTextData, rawTextDataCopy
rawTextData = []
rawTextDataCopy = []
global nodeList
nodeList = []
global deletedNodesList
deletedNodesList = []
global linkToNum
linkToNum = []
global processed_Data_Dictionary #,processed_Data_Dictionary_Copy
processed_Data_Dictionary = {}
processed_Data_Dictionary_Copy = {}
global rankedLinksList
rankedLinksList = []
plotNum = 1
layoutFlag = 1
layout = []
x=1
rankMatrix = []

'''
Check whether sum of column values of difference matrix, formed by subtracting
old rank matrix and new new rank matrix, is less than some threshold value.
'''
def checkConvergence(rankMatrix_old, rankMatrix_new):
    subMatrix = rankMatrix_old - rankMatrix_new
    sum = 0
    for rankDif in subMatrix:
        sum = sum + abs(rankDif[0])
    if sum<0.001:
        return False
    else:
        return True

'''
Read the nodes and their corresponding links from the data file.
Assign every node(URL) a unique integer.
Write the links (FromNode : ToNode in numeric format) to a separate file 'processedLinksData'
'''
def createNodeToNum(stringData):

    with open(stringData) as fread:
        linkNum=0
        lineList = []
        for line in fread:
            lineList = line.split(' ')
            lineList[1] = lineList[1].strip('\n')
            if lineList[0] not in linkToNum:
                linkToNum.append(lineList[0])
            if lineList[1] not in linkToNum:
                linkToNum.append(lineList[1])
            with open('processedLinksData','a') as fwrite:
                fwrite.write(str(linkToNum.index(lineList[0])) + ' ' + str(linkToNum.index(lineList[1])) + '\n')


#read the file line by line, and create rawTextdata 2D list
def createRawTextData():
    with open('processedLinksData') as f:
        lineList = []
        for line in f:
            lineList = line.split(' ')
            lineList[1] = lineList[1].strip('\n')
            rawTextData.append(lineList);
    global rawTextDataCopy
    rawTextDataCopy = rawTextData


#create processeddataDictionary, key: link, value: list of tolinks
def createProcessed_Data_dictionary():
    tempList = []
    global processed_Data_Dictionary_Copy
    for tempList in rawTextData:
        if tempList[0] not in processed_Data_Dictionary:
            processed_Data_Dictionary[tempList[0]] = [tempList[1]]
        else:
            processed_Data_Dictionary[tempList[0]].append(tempList[1])

        if tempList[0] not in nodeList:
            nodeList.append(tempList[0])
        if tempList[1] not in nodeList:
            nodeList.append(tempList[1])
    processed_Data_Dictionary_Copy = processed_Data_Dictionary


#process those nodes who have no toLinks
def handleLinks_with_No_ToNodes():
    for node in nodeList:
        if node not in processed_Data_Dictionary:
            processed_Data_Dictionary[node] = []


#create the link matrix
def createLinkMatrix(matrixM):
    for node in processed_Data_Dictionary:
        numOfToLinks = len(processed_Data_Dictionary[node])
        for toLink in processed_Data_Dictionary[node]:
            matrixM[int(toLink)][int(node)] = 1/numOfToLinks
    return matrixM


def performPowerIteration(matrixM,oldRankMatrix,newRankMatrix,teleportMatrix):
    while checkConvergence(numpy.asarray(newRankMatrix.todense()),numpy.asarray(oldRankMatrix.todense())):
        oldRankMatrix = newRankMatrix
        newRankMatrix = (matrixM*oldRankMatrix) + teleportMatrix
        visualisePageRank(numpy.asarray(newRankMatrix.todense()))
        print(newRankMatrix)
    return numpy.asarray(newRankMatrix.todense())


def visualisePageRank(newRankMatrix):
    print(newRankMatrix)
    g = Graph(directed=True)
    global plotNum,deletedNodesList
    nodeList.sort()

    #create a color pallet
    num_colors = 100
    palette = RainbowPalette(n=num_colors)
    color_list = []
    for i in range(num_colors):
        color_list.append(palette.get(i))

    #Add node to plot
    for node in nodeList:
        if len(deletedNodesList)==0:
            size = 10*60*newRankMatrix[int(node)][0]
            g.add_vertex(name = node,color = color_list[int(size%98)],label = node, size = 10*60*newRankMatrix[int(node)][0])
        elif node not in deletedNodesList:
            size = 10*60*newRankMatrix[int(node)][0]
            g.add_vertex(name = node,color = color_list[int(size%98)],label = node, size = 10*60*newRankMatrix[int(node)][0])

    global layoutFlag
    global layout
    if layoutFlag==1:
        layout = g.layout_lgl()
        for l in layout:
            print(l)
            l[0] = l[0]/2
            l[1] = l[1]/2
        layout[0][0] = 0
        layout[0][1] = 0
        layoutFlag = 0

    #add edges to plot
    global x
    for edge in rawTextData:
        if len(deletedNodesList)==0 or edge[0] not in deletedNodesList and edge[1] not in deletedNodesList  :
            print(edge[0] + " " + edge[1])
            g.add_edge(edge[0],edge[1])
            plot(g,'Images/g'+str(x)+'.png',layout = layout,bbox =(656,364))
            x = x + 1

    plot(g,'Final_images/g'+str(plotNum)+'.png',layout = layout,bbox =(656,364))
    plotNum = plotNum + 1


def rankVertices(newRankMatrix):
    for linkVal in newRankMatrix:
        i=0
        maxVal=0
        maxLinkNum=0
        for linkVal in newRankMatrix:
            if linkVal[0]>maxVal and linkToNum[i] not in rankedLinksList:
                maxVal = linkVal[0]
                maxLinkNum = i
            i+=1
        rankedLinksList.append(linkToNum[maxLinkNum])

def createGif(imageFolder,gifName):

    image_files = os.listdir(imageFolder)
    for i in range(0,len(image_files)):
        image_files[i] = os.path.join(imageFolder,image_files[i])
    image_files.sort()
    import imageio
    images = []
    for filename in image_files:
        images.append(imageio.imread(filename))
    imageio.mimsave(gifName, images,duration=0.7)

def main(stringDataFile, newEdgeFlag, imageFolder1, imageFolder2):
    global plotNum,layoutFlag,rankMatrix,processed_Data_Dictionary,rawTextData,rankedLinksList,nodeList,linkToNum

    filelist = [ f for f in os.listdir('/home/subhadip/PageRankTester/Images/')]
    for f in filelist:
        os.remove(os.path.join('/home/subhadip/PageRankTester/Images/', f))

    filelist = [ f for f in os.listdir('/home/subhadip/PageRankTester/Final_images/')]
    for f in filelist:
        os.remove(os.path.join('/home/subhadip/PageRankTester/Final_images/', f))

    plotNum = 1

    if newEdgeFlag == 0:
        open('processedLinksData','w').close()
        processed_Data_Dictionary = {}
        rawTextData = []
        linkToNum = []
        rawTextData = []
        nodeList = []

        createNodeToNum(stringDataFile)
        createRawTextData()
        createProcessed_Data_dictionary()
        handleLinks_with_No_ToNodes()
        print(nodeList)
        print(processed_Data_Dictionary)

    rankedLinksList = []
    ini_rank = 1/int(len(nodeList))
    matrixM = numpy.zeros((int(len(nodeList)),int(len(nodeList))))
    matrixM = createLinkMatrix(matrixM)
    matrixM = 0.80*matrixM
    matrixM = sparse.csr_matrix(matrixM)

    #create rank vector
    oldRankMatrix = numpy.zeros((int(len(nodeList)),1))
    for r in oldRankMatrix:
        r[0] = ini_rank
    oldRankMatrix = sparse.csr_matrix(oldRankMatrix)

    #create teleport matrix
    teleportMatrix = numpy.zeros((int(len(nodeList)),1))
    for t in teleportMatrix:
        t[0] = 0.20*ini_rank
    teleportMatrix = sparse.csr_matrix(teleportMatrix)

    newRankMatrix = (matrixM*oldRankMatrix) + teleportMatrix
    visualisePageRank(numpy.asarray(newRankMatrix.todense()))

    newRankMatrix = performPowerIteration(matrixM,oldRankMatrix,newRankMatrix,teleportMatrix)

    rankMatrix = newRankMatrix
    visualisePageRank(newRankMatrix)

    rankVertices(newRankMatrix)
    #createGif(imageFolder1,'movie1.gif')
    createGif(imageFolder2,'movie2.gif')



open('processedLinksData','w').close()
#main('stringData.txt',0,'/home/subhadip/PageRankTester/Images/','/home/subhadip/PageRankTester/Final_images/')
