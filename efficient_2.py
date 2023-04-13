import time
import sys
import psutil
gap = 30        #Defining Gap Penalty



def penalty(a1, a2):       #function that holds the penalty mismatch matrix
    str= 'ACGT'
    string1_index= str.find(a1)
    string2_index= str.find(a2)
    penalty_matrix = [[0, 110, 48, 94],
                      [110, 0, 118, 48],
                      [48, 118, 0, 110],
                      [94, 48, 110, 0]]
    return penalty_matrix[string1_index][string2_index]


def align(string1, string2):

    OPT = [[0 for _ in range(len(string2) + 1)] for _ in range(len(string1) + 1)]
    #Creating a temperary OPT

    #Initial values of the OPT Array
    for i in range(len(string1) + 1):
        OPT[i][0] = i * gap
    for i in range(len(string2) + 1):
        OPT[0][i] = i * gap


    for i in range(1, len(string1) + 1):
        for j in range(1, len(string2) + 1):
            OPT[i][j] = min(
                OPT[i - 1][j - 1] + penalty(string1[i - 1],string2[j - 1]),
                OPT[i - 1][j] + gap,
                OPT[i][j - 1] + gap,
            )

    string1_aligned = []
    string2_aligned = []
    m = len(string1)
    n = len(string2)

    while m > 0 and n > 0:
        if OPT[m][n] == OPT[m - 1][n - 1] + penalty(string1[m - 1],string2[n - 1]):
            string1_aligned.append(string1[m - 1])
            string2_aligned.append(string2[n - 1])
            m -= 1
            n -= 1
        elif OPT[m][n] == OPT[m - 1][n] + gap:
            string1_aligned.append(string1[m - 1])
            string2_aligned.append("-")
            m -= 1
        else:
            string1_aligned.append("-")
            string2_aligned.append(string2[n - 1])
            n -= 1

    if m:
        for i in range(m, 0, -1):
            string1_aligned.append(string1[i - 1])
            string2_aligned.append("-")
    elif n:
        for i in range(n, 0, -1):
            string1_aligned.append("-")
            string2_aligned.append(string2[i - 1])

    string1_aligned.reverse()
    string2_aligned.reverse()

    return "".join(string1_aligned), "".join(string2_aligned)


def forward_alignment(string1, string2):
    OPT = [[0, 0] for _ in range(len(string1) + 1)]
    #OPT array initialized with the product of gap and the row index
    for i in range(len(string1) + 1):
        #Base
        OPT[i][0] = i * gap

    for j in range(1, len(string2) + 1):
        OPT[0][1] = j * gap
        for i in range(1, len(string1) + 1):
            #Findng OPT array
            OPT[i][1] = min(
                OPT[i - 1][0] + penalty(string1[i - 1],string2[j - 1]),
                OPT[i - 1][1] + gap,
                OPT[i][0] + gap,
            )

        for k in range(len(string1) + 1):
            OPT[k][0] = OPT[k][1]

    return OPT[: len(string1) + 1]


def backward_alignment(string1, string2):
    OPT = [[0, 0] for _ in range(len(string1) + 1)]
    #OPT array initialized with the product of gap and the row index
    for i in range(0,len(string1) + 1):
        OPT[i][0] = (len(string1) - i) * gap

    for j in range(len(string2) - 1, -1, -1):
        OPT[len(string1)][1] = (len(string2) - j) * gap
        #Base
        for i in range(len(string1) - 1, -1, -1):
            #Updating OPT array
            OPT[i][1] = min(
                OPT[i + 1][0] + penalty(string1[i],string2[j]),
                OPT[i + 1][1] + gap,
                OPT[i][0] + gap,
            )

        for k in range(0,len(string1) + 1):
            OPT[k][0] = OPT[k][1]
    return OPT[: len(string1) + 1]


temporary_list = []


def Algorithm(string1, string2):
    if len(string1) <= 2 or len(string2) <= 2:
        temporary_list.append(align(string1, string2))
        return
    #Initially considering array is split in the middle
    division_point = len(string2) // 2
    #Finding split point
    f = forward_alignment(string1, string2[:division_point])
    b = backward_alignment(string1, string2[division_point:])

    min_list = f[0][1] + b[0][1]
    x = 0
    for i in range(len(string1) + 1):
        temp = f[i][1] + b[i][1]
        if temp < min_list:
            #Finding minimum split point
            min_list = temp
            x = i
    #Recursively calling the function
    Algorithm(string1[:x], string2[:division_point])
    Algorithm(string1[x:], string2[division_point:])



def time_wrapper(string1,string2,OPT):    #calculating time
    start_time = time.time()

    Algorithm(string1, string2)
    output_string1 = "".join([x[0] for x in temporary_list])
    output_string2 = "".join([x[1] for x in temporary_list])

    solution_cost = 0
    for i in range(len(output_string1)):
        if output_string1[i] != "-" and output_string2[i] != "-":
            #In case of mismatch Update alignment cost by adding mismatch cost
            solution_cost += penalty(output_string1[i],output_string2[i])
        else:
            #In case of gap update alignment cost by adding gap cost
            solution_cost += gap

    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return solution_cost, time_taken, output_string1, output_string2

def process_memory():   #calculating memory
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def read(): #Reading input from "input.txt" file
    
    file = sys.argv[1]  #Reading first argument which is the file "input.txt"
    f = open(file, "r")
    string_list = []    #list of both strings
    postring1 = []   #list of positions for first string
    postring2 = []   #list of positions for second string

    for line in f.readlines():
        line = line.strip()

        if not line.isnumeric():
            string_list.append(line)

        else:
            if len(string_list)<2:      #if second string is encountered already then add numbers in postring2
                postring1.append(int(line))
            else:
                postring2.append(int(line))

    f.close()
    return string_list, postring1, postring2


def string_generator(string, num):  #generates string from the pos and string
    
    index = 0
    
    while index < len(num):
        string = string[0:num[index]+1] + string + string[num[index]+1 :]
        index += 1
    
    return string


def get_input():    #gets both the generated strings and adds them in a list and returns the list 
    str_list, postring1, postring2 = read() 
    string_list=[]
    string_list.append(string_generator(str_list[0], postring1))
    string_list.append(string_generator(str_list[1], postring2))

    return string_list


stringlist=[]
stringlist=get_input()
string1 = stringlist[0]
string2 = stringlist[1]



OPT = [[0, 0] for _ in range(len(string1) + 1)]
#Calculating time and memory
solution_cost, time_taken, output_string1, output_string2 = time_wrapper(string1, string2,OPT)
memory_used = process_memory()
#Write output to file
output=[str(solution_cost), output_string1, output_string2, str(time_taken), str(memory_used)]

file = sys.argv[2]
f = open(file, 'wt')
f.write('\n'.join(output))
f.close()