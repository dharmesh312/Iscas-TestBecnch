### IN ADJCACENCY LIST OF THE GRAPH [NODE,NODETYPE,COMPUTATUION TIME,DEALY,WEIGHT OF THE EDGE]
import sys
from sys import argv
import copy
import math
script,filename=argv

Input=[]
Output=[]
INPUT_computation=0
OUTPUT_computation=0
adj_list={}
DFF_list=[]
t_max=1
NOR_computation_time=1
NOT_computation_time=1
AND_computation_time=1
NAND_computation_time=1
OR_computation_time=1
DFF_computation_time=0
keys=[]
keys2=[]
NodeTypes={}
node_computation_time={}

def copyList(adj_list2):
    temp={}
    temp=copy.deepcopy(adj_list2)
    return temp

def adding_weightsDFS(adj_list,entry,i,p):
    tempNode=adj_list[entry][i][0]
    if(adj_list[tempNode][0][1]=='DFF'):
        p=p+1
        return adding_weightsDFS(adj_list,tempNode,i,p)
    else :
         adj_list[tempNode][0][4]=adj_list[tempNode][0][4]+1 +p
         return adj_list[tempNode][0]

def initialize(filename):
    data=open(filename,'r')
    adj_list['GInput']=[]
    adj_list['GOutput']=[]
    node_computation_time['GInput']=0
    node_computation_time['GOutput']=0
    for line in data :
        arr=line.split()
        a=line[line.find("(")+1:line.find(")")]
        if '#' not in line and line!='\n' and 'INPUT' not in line and 'OUTPUT' not in line:
            adj_list[arr[0]]=[]
        if 'INPUT' in line or 'OUTPUT' in line :
            adj_list[a]=[]

def createFirstGraph(filename):
    data=open(filename,'r')
    for line in data :
        temp=[]
        temp2=[]
        arr=line.split()
        if '#' not in line:
            a=line[line.find("(")+1:line.find(")")]
            a1=a.split(',')
            if 'INPUT' in line:
                Input.append(a)
                node_computation_time[a]=INPUT_computation
            elif 'OUTPUT' in line:
                Output.append(a)
                node_computation_time[a]=OUTPUT_computation
            elif 'AND' in line and 'NAND' not in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=AND_computation_time
                    NodeTypes[arr[0]]='AND'
                    adj_list[m[0]].append([arr[0],'AND',AND_computation_time,0,0])
            elif 'OR' in line and 'NOR' not in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=OR_computation_time
                    NodeTypes[arr[0]]='OR'
                    adj_list[m[0]].append([arr[0],'OR',OR_computation_time,0,0])
            elif 'NAND' in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=NAND_computation_time
                    NodeTypes[arr[0]]='NAND'
                    adj_list[m[0]].append([arr[0],'NAND',NAND_computation_time,0,0])
            elif 'NOR' in line :
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=NOR_computation_time
                    NodeTypes[arr[0]]='NOR'
                    adj_list[m[0]].append([arr[0],'NOR',NOR_computation_time,0,0])
            elif 'NOT' in line:
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=NOT_computation_time
                    NodeTypes[arr[0]]='NOT'
                    adj_list[m[0]].append([arr[0],'NOT',NOT_computation_time,0,0])
            elif 'DFF' in line :
                for i in range(0,len(a1)):
                    m=a1[i].split()
                    node_computation_time[arr[0]]=DFF_computation_time
                    DFF_list.append(arr[0])
                    adj_list[m[0]].append([arr[0],'DFF',DFF_computation_time,0,0])

def createWeightedGraph(adj_list):
    for entry in adj_list:
        for i in range(0,len(adj_list[entry])):
            if(adj_list[entry][i][1]=='DFF'):
                tempNode=adding_weightsDFS(adj_list,entry,i,0)
                ###tempNode is the address location of the node
                temp=[tempNode[0],tempNode[1],tempNode[2],tempNode[3],tempNode[4]]
                ####storing in the value not the address of the temp node
                adj_list[entry][i]=temp

def createRetimingModel(adj_list):
    for i in range(0,len(Input)):
        adj_list['GInput'].append([Input[i],'INPUT',0,0,0])

    for i in range(0,len(Output)):
        adj_list[Output[i]].append(['GOutput','OUTPUT',0,0,0])

def generateReweightedGraph(adj_list_reweighted):
    ##find n
    n=0
    for entry in adj_list_reweighted:
        if entry not in DFF_list:
            n=n+1
    M=t_max*n
    for entry in adj_list_reweighted:
        for i in range(0,len(adj_list_reweighted[entry])):
            if(node_computation_time[entry]!=0):
                adj_list_reweighted[entry][i][4]=(M*adj_list_reweighted[entry][i][4] )  -node_computation_time[entry]

def createAdjacencyMatrix(adj_list):
    mat=[[float('inf') for x in range(len(adj_list)-len(DFF_list))] for y in range(len(adj_list)-len(DFF_list))]

    for i in range(len(mat[0])):
        mat[i][i]=0
    for entry in adj_list :
        if entry not in DFF_list:
            keys.append(entry)
    for entry in adj_list:
        if entry not in DFF_list:
            l=keys.index(entry)
            for i in range(len(adj_list[entry])):
                entry2=adj_list[entry][i][0]
                if entry2 not in DFF_list:
                    m=keys.index(entry2)
                    mat[l][m]=adj_list[entry][i][4]
    return mat

def floydWarshall(mat):
    n=len(mat[0])
    D=[None for x in range(0,n)]
    D[0]=mat
    for k in range(1,n):
        D[k]=[[None for x in range(0,n)]for y in range(0,n)]
        for i in range(0,n):
            for j in range(0,n):
                D[k][i][j]=min(D[k-1][i][j],D[k-1][i][k]+D[k-1][k][j])

    return D[n-1]

def findWmatrix(mat):
    n=len(mat[0])
    M=t_max*n
    W_mat=[[0 for x in range(0,n)]for y in range(0,n)]
    for i in range(0,n):
        for j in range(0,n):
            W_mat[i][j]=math.ceil(mat[i][j]/M)

    return W_mat

def findDmatrix(mat,W_mat,adj_list):
    n=len(mat[0])
    M=t_max*n
    D_mat=[[0 for x in range(0,n)]for y in range(0,n)]
    for i in range(0,n):
        for j in range(0,n):

            if(i==j):
                    D_mat[i][j]=node_computation_time[keys[i]]
            else :
                    D_mat[i][j]=W_mat[i][j]*M-mat[i][j]+node_computation_time[keys[j]]
    return D_mat

def feasibilityConstraints(W_mat,D_mat,mat,adjList,keys,c):
    inequalityDict={}
    for i in range(0,len(keys)):
        inequalityDict[keys[i]]=[]

    for i in range(0,len(mat[0])):
        for j in range(0,len(mat[0])):
            u=keys[i]
            v=keys[j]
            for k in range(0,len(adjList[keys[i]])):
                if(adjList[keys[i]][k][0]==keys[j]):
                    inequalityDict[v].append( [ u,adjList[keys[i]][k][4] ] )

    for i in range(0,len(mat[0])):
        for j in range(0,len(mat[0])):
            u=keys[i]
            v=keys[j]
            if(D_mat[i][j]>c):
                flag=0
                weight=W_mat[i][j]-1
                if(inequalityDict[v]==[]):
                    inequalityDict[v].append([  u,weight ])
                else:
                    for k in range(0,len(inequalityDict[v])):
                        if(inequalityDict[v][k][0]==u):
                            flag=1
                            if(inequalityDict[v][k][1]>weight):

                                inequalityDict[v][k][1]=weight

                    if(flag==0):
                        inequalityDict[v].append([ u, weight])

    for key, item in inequalityDict.items():
        if item == []:
            del inequalityDict[key]

    for entry in inequalityDict:
        if(entry not in keys2):
            keys2.append(entry)
        for j in range(0,len(inequalityDict[entry])):
            if(inequalityDict[entry][j][0] not in keys2 ):
                keys2.append(inequalityDict[entry][j][0])

    mat2=[[ float('inf') for x in range(0,len(keys2)+1)] for y in range(0,len(keys2)+1) ]

    for entry in inequalityDict:
        for k in range(0,len(inequalityDict[entry])):
            i=keys2.index(entry)
            j=keys2.index(inequalityDict[entry][k][0])
            mat2[i][j]=inequalityDict[entry][k][1]

    ###the last element of the matrix is used as a source that is connected to every nnode by weight 1
    for j in range(len(mat2[0])):
        mat2[len(keys2)][j]=0
    return  mat2

def BellmanFord(mat,s):
    d=[float('inf') for x in range(len(mat[0]))]
    d[len(mat[0])-1]=0

    for i in range(0,len(mat[0])):
        for j in range(0,len(mat[0])):
            if(mat[i][j]!=float('inf')):
                if(d[j]>d[i]+mat[i][j]):
                    d[j]=d[i]+mat[i][j]             ####relasing the edges by bellman ford no need to find parent component

    for i in range(0,len(mat[0])):
        for j in range(0,len(mat[0])):
            if(mat[i][j]!=float('inf')):
                if(d[j]>d[i]+mat[i][j]):
                    return False

    return d

def FinalGraph(arr,adj_list):
    adjFinal=copyList(adj_list)
    for key, item in adjFinal.items():
        if key not in keys:
            del adjFinal[key]

    for entry in adjFinal:
        for i in range(0,len(adjFinal[entry])):
            adjFinal[entry][i][4]=adjFinal[entry][i][4]+arr[keys2.index(adjFinal[entry][i][0])]-arr[keys2.index(entry)]

    return  adjFinal

# def maxDFS(adj_list,color,src,cmp,arrCMP,tempKeys):
#     index=tempKeys.index(src)
#     color[index]=1
#     cmp=cmp+node_computation_time[src]
#     if src in DFF_list or src =='GOutput':
#         arrCMP.append([cmp,src])
#     else :
#         for i in range(0,len(adj_list[src])):
#             index2=tempKeys.index(adj_list[src][i][0])
#             if(color[index2]==0):
#                 maxDFS(adj_list,color,adj_list[src][i][0],cmp,arrCMP,tempKeys)
#
# def maxMatrix(adj_list):
#     cmp=0
#     tempKeys=[]
#     for entry in adj_list:
#         tempKeys.append(entry)
#     color=[0 for x in range(len(tempKeys))]
#     arrCMP=[]
#     maxDFS(adj_list,color,'GInput',cmp,arrCMP,tempKeys)
#     #print arrCMP

def WriteToFile(INPUTS,OUTPUTS,dffs,GateList):
    FileP=open('output.txt','w')

    ###writing all thte INPUTS
    for i in range(0,len(INPUTS)):
        FileP.write('INPUT'+'('+INPUTS[i]+')'+'\n')
    FileP.write('\n')

    ###writing all thte OUTPUTs
    for i in range(0,len(OUTPUTS)):
        FileP.write('OUTPUT'+'('+OUTPUTS[i]+')'+'\n')
    FileP.write('\n')

    ###writting the dffs
    for entry in dffs:
        previous=entry
        for j in range(0,dffs[entry][1]):
            new='DFF' + '_' + entry + '_'+ str(j)
            FileP.write(new + ' = '+'DFF'+'('+previous+')'+'\n')
            previous=new

    FileP.write('\n')
    for entry in GateList:
        temp_str=''
        for j in range(1,len(GateList[entry])-1):
            temp_str=temp_str+GateList[entry][j]+','
        temp_str=temp_str+GateList[entry][len(GateList[entry])-1]
        FileP.write(entry +' = ' + GateList[entry][0] + '('+temp_str+')'+'\n')


def writeBack(adjFinal):
    dffs={}
    INPUTS=[]
    OUTPUTS=[]
    GateList={}
    for entry in adjFinal:
        if(entry!='GInput' and entry!='GOutput' and entry not in Input):
            GateList[entry]=[NodeTypes[entry]]


    for i in range(0,len(adjFinal['GInput'])):
        INPUTS.append(adjFinal['GInput'][i][0])
    for i in range(0,len(Output)):
        OUTPUTS.append(Output[i])

    for entry in adjFinal:
        if(entry!='GInput' and entry!='GOutput'  ):
            for i in range(0,len(adjFinal[entry])):
                if(adjFinal[entry][i][4]==0 and adjFinal[entry][i][0]!='GOutput'):
                    head=adjFinal[entry][i][0]
                    GateList[head].append(entry)
                elif(adjFinal[entry][i][4]!=0):
                    head=adjFinal[entry][i][0]
                    GateList[head].append('DFF'+'_'+entry+'_'+str(adjFinal[entry][i][4]-1))
                    dffs[entry]=[head,adjFinal[entry][i][4]]

    WriteToFile(INPUTS,OUTPUTS,dffs,GateList)

##################################   MAIN   ########################################
initialize(filename)
createFirstGraph(filename)
c=int(raw_input('Please Enter the value of the c(critical time for the computation of W matrix and D matrix):'))

####storing the unweighted adjacency list in an another tuple
createRetimingModel(adj_list)
adjListInitial=copyList(adj_list)


####create retiming model
createWeightedGraph(adj_list)


####All pairs shortest path find
adjList=copyList(adj_list)
generateReweightedGraph(adj_list)
mat=createAdjacencyMatrix(adj_list)
all_pair_shortest_path_mat=floydWarshall(mat)

#####finding D and W matrix
W_matrix=findWmatrix(all_pair_shortest_path_mat)
D_matrix=findDmatrix(all_pair_shortest_path_mat,W_matrix,adj_list)

###finding the graph by inequality
InequalityMatrix=feasibilityConstraints(W_matrix,D_matrix,mat,adjList,keys,c)
newTimeArray=BellmanFord(InequalityMatrix,len(InequalityMatrix)-1)   ##the last element of the matrix is the source of the BellmanFord
adjFinal=FinalGraph(newTimeArray,adjList)

###finding max COMPUTATUION time
# maxMatrix(adjListInitial)
writeBack(adjFinal)

for entry in adjList:
     print entry       ,         adjList[entry]
