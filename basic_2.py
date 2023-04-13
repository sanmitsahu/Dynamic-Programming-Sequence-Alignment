import sys
import time
import psutil
gap=30


def read(): #Reading input from "input.txt" file
    
    file = sys.argv[1]  #Reading first argument which is the file "input.txt"
    f = open(file, "r")
    string_list = []    #list of both strings
    pos1 = []   #list of positions for first string
    pos2 = []   #list of positions for second string

    for line in f.readlines():
        line = line.strip()

        if not line.isnumeric():
            string_list.append(line)

        else:
            if len(string_list)<2:      #if secon string is encountered already then add numbers in pos2
                pos1.append(int(line))
            else:
                pos2.append(int(line))

    f.close()
    return string_list, pos1, pos2


def string_generator(string, num):  #generates string from the pos and string
    
    index = 0
    
    while index < len(num):
        string = string[0:num[index]+1] + string + string[num[index]+1 :]
        index += 1
    
    return string


def get_input():    #gets both the generated strings and adds them in a list and returns the list 
    str_list, pos1, pos2 = read() 
    string_list=[]
    string_list.append(string_generator(str_list[0], pos1))
    string_list.append(string_generator(str_list[1], pos2))

    return string_list


def penalty(a1, a2):       #function that holds the penalty mismatch matrix
    str= 'ACGT'
    string1_index= str.find(a1)
    string2_index= str.find(a2)
    penalty_matrix = [[0, 110, 48, 94],
                      [110, 0, 118, 48],
                      [48, 118, 0, 110],
                      [94, 48, 110, 0]]
    return penalty_matrix[string1_index][string2_index]



def sequence_alignment(string1,string2):      #MAIN ALGORITHM THE CALCULATES THE COST AND sequence_alignment
    
    m = len(string1)

    n = len(string2)

    OPT = [[0 for col in range(n + 1)] for row in range(m + 1)]       #Creating dp array

    for i in range(m+1):   #for no sequence_alignment
        OPT[i][0]=gap*i

    for j in range(n+1):   #for no sequence_alignment
        OPT[0][j]=gap*j


    #To calculate the cost of alignment

    for i in range(1,m+1):
        for j in range(1,n+1):
            if string1[i-1]==string2[j-1]:
                min_value=min(OPT[i-1][j-1],
                              OPT[i-1][j]+ gap,
                              OPT[i][j-1]+gap)
                OPT[i][j]=min_value
            else:
                min_value= min(OPT[i - 1][j - 1]+penalty(string1[i-1], string2[j-1]),
                                OPT[i - 1][j] + gap,
                                OPT[i][j - 1] + gap)
                OPT[i][j]=min_value

    #TO calculate the alignment

    i= m
    j= n
    seq=[[0 for col in range(n+1)] for row in range(m+1)]
    seq[i][j]=1
    seq[0][0]=1
    while i!=0 or j!=0:
        if  OPT[i][j]==OPT[i-1][j]+gap:
            seq[i-1][j]=1
            i=i-1
        elif  OPT[i][j]==OPT[i][j-1]+gap:
            seq[i][j-1] = 1
            j=j-1
        else:
            seq[i-1][j - 1] = 1
            i=i-1
            j=j-1

    string1_final=''
    string2_final=''
    i=0
    j=0
    while i!=m and j!=m:
        if i!=m and seq[i+1][j]==1:
            string1_final=string1_final+string1[i]
            string2_final = string2_final + '-'
            i=i+1
        elif j!=n and seq[i][j+1]==1:
            string1_final = string1_final + '-'
            string2_final = string2_final + string2[j]
            j=j+1
        else:
            string1_final = string1_final + string1[i ]
            string2_final = string2_final + string2[j]
            i=i+1
            j=j+1
            
    output=[str(OPT[m][n]), string1_final, string2_final]

    return OPT, output

def time_wrapper(string1,string2):    #calculating time
    start_time = time.time()
    OPT,output = sequence_alignment(string1, string2) #Calling the algorithm
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return OPT,output,time_taken

def process_memory():   #calculating memory
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed


input_string=get_input()
string1 = input_string[0]
string2 = input_string[1]


OPT, output, run_time = time_wrapper(string1,string2) 

memory_consumed = process_memory()
output.append(str(run_time))
output.append(str(memory_consumed))

file = sys.argv[2]
f = open(file, 'wt')
f.write('\n'.join(output))
f.close()