import random
import copy
import math

def fillIn(array, currDim): #fills the board array with all of the numbers on your bingo board
    if currDim == dimensions: #checks to see if it's in the innermost layer
        for i in range(5): #fills in the layer with 5 new random numbers
            while True:
                p = random.randrange(1, 3 * 5 ** dimensions)

                if not(p in usedNums):
                    usedNums.append(p)
                    array.append(p)
                    break
    else: #if there are more arrays within
        if array != []: #catch, because the way I have this structured, it will keep generating and replacing the board quite a few times, this will kill it outright
            board = copy.deepcopy(array)
        else: #otherwise, it makes more lists to fill into
            for j in range(5):
                array.append([])
                
            for k in array:
                fillIn(k, currDim + 1)

def generateBingo(sample): #this generates all of the possible bingos you can have + 1
    #the bingos form lists, such as [0, 1, 1] or [-1. 1. 0], which dictate the nature of the bingo. Each number corresponds to a dimension, and 0 means to not change, 1 iterates forward, and -1 iterates backward
    negative = [] #I have to generate the negative, because it checks the exact same thing as the positive, but it looks different. [0, 1, 1] is the same as [0, -1, -1]
    
    if len(sample) >= dimensions:
        for i in sample:
            negative.append(i * -1)
            
        if not(sample in bingos) and not(negative in bingos):
            bingos.append(sample)
    else:
        for i in [0, 1, -1]:
            t = copy.deepcopy(sample)
            t.append(i)
            generateBingo(t)

def checkBingo(pos): #this checks if a given position completes a bingo
    for p in bingos:
        ones = [] #one weird thing I have to keep track of is the position per bingo. Because all of them check in mod 5, it loops back if it goes over. so I need to make sure that its actually along the diagonal that its checking
        negones = []

        i = copy.deepcopy(p)
        
        for j in range(len(i)):
            if i[j] == 1:
                ones.append(j)
            elif i[j] == -1:
                negones.append(j)

        if len(ones) >= 2: #this checks if it's in the correct position (see above), and if it isn't, it just skips the rest and checks the next bingo
            bar = pos[ones[0]]

            for h in ones:
                if pos[h] != bar:
                    continue
        if len(negones) >= 2:
            bar = pos[negones[0]]

            for h in negones:
                if pos[h] != bar:
                    continue
        if len(ones) >= 1 and len(negones) >= 1:
            if pos[ones[0]] + pos[negones[0]] != 4:
                continue

        for k in range(4): #now that it's in the right spot, this checks if it actually is 5 in a row
            check = []
            for j in range(len(pos)):
                check.append((pos[j] + i[j]) % 5)

            if check in filled:
                for h in range(len(i)):
                    if i[h] > 0:
                        i[h] += 1
                    elif i[h] < 0:
                        i[h] -= 1
            else: #if any of the projected row values aren't filled in it spits it out later
                continue

        return True #if any make it all of the way through, there is a bingo

    return False #otherwise, no bingos

def largestLog(num): #this just returns how many times 5 divides a number evenly (for 1 super specific purpose)
    log = 0
    while True:
        if int(num / 5) == num / 5 and num > 0:
            log += 1
            num /= 5
        else:
            return log

def printBoard(array, currDim): #misnomer name, this actually just sends all of the formatted lines into another list, strings
    global filled
    global strings
    global counter
    global numsInString
    global position
    
    if currDim == 1: #if we are at the smallest dimension (the one that actually contains numbers instead of more lists)
        for i in array: #for every number
            substring = "" #this is the _ before each number
            substring2 = " " #this is the spaces after each number
            for j in range(len(str(3 * 5 ** dimensions)) - len(str(i))): #generates _ to place before the number so that all numbers take up the same space
                substring += "_"

            if numsInString[counter % len(strings)] % 5 == 4: #checks to see if it has printed a multiple of 5 numbers
                if counter < len(strings): #weird case, logic wouldnt work if counter was less than the length of strings for some reason
                    substring2 += " "
                if numsInString[counter % len(strings)] != 0: #we don't want it to run right away for the first number
                    for h in range(largestLog(numsInString[counter % len(strings)] - 4)): #adds spaces equal to the number of dimensions it's seperating. For example, if it's seperating two 3D boards in the 4th dimension, one extra space
                        substring2 += " "
                else:
                    substring2 += " "

            posOfNum(board, 0, i) #to find the position of the number we are checking

            if position in filled: #if we have found the number, print it
                strings[counter % len(strings)] += substring + str(i) + substring2
            else: #if we haven't, just print the ___
                substring = ""
                for g in range(len(str(3 * 5 ** dimensions))):
                    substring += "_"

                strings[counter % len(strings)] += substring + substring2

            numsInString[counter % len(strings)] += 1

        counter += 1 #we need this to see when we are running this function on multiples of 5
    else: #if we aren't in the innermost layer, navigate one layer deeper
        for i in range(5):
            printBoard(array[i], currDim - 1)

def posOfNum(array, index, num): #sets the position list to the position of the num
    global position
    
    for i in range(len(array)):
        x[index] = i

        if array[i] == num:
            position = copy.deepcopy(x)
        elif type(array[i]) is list:
            posOfNum(array[i], index + 1, num)

def layStrings(): #prints all of the strings in the strings list, adding \n in the same way we added spaces above
    for i in range(len(strings)):
        if i != 0 and i % 5 == 0:
            for j in range(largestLog(i)):
                print("")
                
        print(strings[i])

def resetStrings(): #this generates/resets both the strings and the numInString to lists of empty values
    global strings
    global numsInString

    strings = []
    numsInString = []
    
    for i in range(5 ** math.floor((dimensions + 1) / 2)):
        strings.append("")

    for i in strings:
        numsInString.append(0)
            
def playGame(): #main loop
    global board #the actual super array with all of the numbers
    global usedNums #the list of numbers that are in the board
    global filled #the list of numbers we have guessed correctly
    global bingos #the list of all possible bingos for our dimension
    global dimensions
    global strings #the list of each line of the board we want to print
    global numsInString #the amount of numbers in each string
    global counter #just for printBoard
    global position #stores the position of a given number after posOfNum
    global x #stupid awful placeholder that I hate that I don't know how to get rid of
  
    board = []
    usedNums = []
    filled = []
    bingos = []
    dimensions = 0
    strings = []
    numsInString = []
    counter = 0
    position = []
    x = []

    while True: #find dimensions
        try:
            dimensions = int(input("How many dimensions? "))
            break
        except:
            print("Enter an integer")
    
    fillIn(board, 1) #generate the board

    for i in range(dimensions * 3): #generate the bingos
        generateBingo([])

    for i in range(dimensions): #generates an empty bingo, [0, 0, 0, ..., 0]
        x.append(0)

    bingos.remove(x) #because generateBingos includes the empty bingo, lets remove it

    resetStrings() #set the strings to be empty

    while True:
        try:
            resetStrings()
            printBoard(board, dimensions)
            layStrings()
            print("")
            guess = int(input("Enter number: "))
            if guess in usedNums:
                posOfNum(board, 0, guess)
                filled.append(position)
                if checkBingo(position):
                    print("BINGO!!!!")
                    resetStrings()
                    printBoard(board, dimensions)
                    layStrings()
                    exit
            else:
                print("No luck :(")
        except:
            print("Please enter a number")

playGame()
