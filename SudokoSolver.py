import numpy as np
from numpy import array
np.set_printoptions(precision=3)

def scrapdata(filename):
    rawSudoku = open(filename,"r")
    dataLine = [int(x) for line in rawSudoku for x in line if x.isnumeric()]
    return dataLine

def getListsFromFlatList(flatList):
    rows = [flatList[i:i + 9] for i in range(0, len(flatList), 9)]
    columns = list(map(list, zip(*rows)))

    threex3 = []
    for a in range(3):
        for b in range(3):
            # print(a,b)
            # print("threex3.append([dataLine[i:i + 3] for i in range(" + str(a*9 + b*3) + ", " + str(int((1+a)*len(dataLine)/3)) + ", " + str(9) +")])")
            threex3.append(
                [z for tree in [flatList[i:i + 3] for i in range(a * 27 + b * 3, int((1 + a) * len(flatList) / 3), 9)]
                 for z in tree])

    return rows, columns, threex3

def get3x3index(xaxis,yaxis):
    if int(xaxis / 3) == 0 and int(yaxis / 3) == 0:
        square3 = 0
    elif int(xaxis / 3) == 0 and int(yaxis / 3) == 1:
        square3 = 1
    elif int(xaxis / 3) == 0 and int(yaxis / 3) == 2:
        square3 = 2
    elif int(xaxis / 3) == 1 and int(yaxis / 3) == 0:
        square3 = 3
    elif int(xaxis / 3) == 1 and int(yaxis / 3) == 1:
        square3 = 4
    elif int(xaxis / 3) == 1 and int(yaxis / 3) == 2:
        square3 = 5
    elif int(xaxis / 3) == 2 and int(yaxis / 3) == 0:
        square3 = 6
    elif int(xaxis / 3) == 2 and int(yaxis / 3) == 1:
        square3 = 7
    elif int(xaxis / 3) == 2 and int(yaxis / 3) == 2:
        square3 = 8
    return square3

def replaceValue(iaxis,jaxis,value,flatList):
    print("replacing " + str(iaxis) + str(jaxis) + " with " + str(value))
    flatList[9*iaxis+jaxis] = value
    return flatList

def mainLogic(rows, columns, threesx3, flatList):
    counter = 0
    while ((0 in flatList or -1 in flatList) and counter < 50):

        counter += 1
        for i in rows:
            iaxis = rows.index(i)
            for j in i:
                jaxis = i.index(j)
                if j == 0:
                    i[jaxis] = -1
                    if USEBOXELEM == 1:
                        currentFlatList = boxElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)
                    if USEROWELEM == 1 and currentFlatList == None:
                        currentFlatList = rowElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)
                    if USEPOSELEM == 1 and currentFlatList == None:
                        currentFlatList = possibleValuesElem(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)

                elif j == -1:
                    i[jaxis] = 0
                    if USEBOXELEM == 1:
                        currentFlatList = boxElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)
                    if USEROWELEM == 1 and currentFlatList == None:
                        currentFlatList = rowElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)
                    if USEPOSELEM == 1 and currentFlatList == None:
                        currentFlatList = possibleValuesElem(flatList, rows, columns, threesx3, i, j, iaxis, jaxis)

        rows, columns, threesx3 = getListsFromFlatList(flatList)

        for row in rows:
            for n in row:
                # print('writing to file ' + str(n))
                if n == -1:
                    sudukoOut.write(str(0))
                else:
                    sudukoOut.write(str(n))
            sudukoOut.write("\n")
        sudukoOut.write("\n")

    print("finished in " + str(counter) + " iterations")

def boxElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis):
    #print(iaxis, jaxis)
    square3 = get3x3index(iaxis, jaxis)  # index of the 3x3 matrix within the 9x9
    #print('threexthree' + str(square3))
    #print('possible value ' + str(k))
    if jaxis % 3 == 0 and iaxis % 3 == 0:
        #print("top left")
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis + 2] > 0 or k in columns[jaxis + 2]) and (
                        rows[iaxis+1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis+1][jaxis+1]>0 or k in rows[iaxis+1] or k in columns[jaxis+1]) and (
                        rows[iaxis+1][jaxis+2]>0 or k in rows[iaxis+1] or k in columns[jaxis+2]) and (
                        rows[iaxis+2][jaxis] > 0 or k in rows[iaxis + 2]) and (
                        rows[iaxis+2][jaxis+1] > 0 or k in rows[iaxis + 2] or k in columns[jaxis+1]) and (
                        rows[iaxis+2][jaxis+2] > 0 or k in rows[iaxis + 2] or k in columns[jaxis+2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 1 and iaxis % 3 == 0:
        #print("top middle")
        possibleValue = []
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        rows[iaxis + 1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis + 1][jaxis + 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis + 1][jaxis - 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis + 2][jaxis] > 0 or k in rows[iaxis + 2]) and (
                        rows[iaxis + 2][jaxis + 1] > 0 or k in rows[iaxis + 2] or k in columns[jaxis + 1]) and (
                        rows[iaxis + 2][jaxis - 1] > 0 or k in rows[iaxis + 2] or k in columns[jaxis - 1]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 2 and iaxis % 3 == 0:
        #print("top right")
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        i[jaxis - 2] > 0 or k in columns[jaxis - 2]) and (
                        rows[iaxis + 1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis + 1][jaxis - 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis + 1][jaxis - 2] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 2]) and (
                        rows[iaxis + 2][jaxis] > 0 or k in rows[iaxis + 2]) and (
                        rows[iaxis + 2][jaxis - 1] > 0 or k in rows[iaxis + 2] or k in columns[jaxis - 1]) and (
                        rows[iaxis + 2][jaxis - 2] > 0 or k in rows[iaxis + 2] or k in columns[jaxis - 2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 0 and iaxis % 3 == 1:
        #print("middle left")
        possibleValue = []
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis + 2] > 0 or k in columns[jaxis + 2]) and (
                        rows[iaxis + 1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis + 1][jaxis + 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis + 1][jaxis + 2] > 0 or k in rows[iaxis + 1] or k in columns[jaxis + 2]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis + 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 1][jaxis + 2] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 1 and iaxis % 3 == 1:
        #print("middle middle")
        possibleValue = []
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        rows[iaxis + 1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis + 1][jaxis + 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis + 1][jaxis - 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis + 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 1][jaxis - 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 1]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 2 and iaxis % 3 == 1:
        #print("middle right")
        possibleValue = []
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        i[jaxis - 2] > 0 or k in columns[jaxis - 2]) and (
                        rows[iaxis + 1][jaxis] > 0 or k in rows[iaxis + 1]) and (
                        rows[iaxis + 1][jaxis - 1] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis + 1][jaxis - 2] > 0 or k in rows[iaxis + 1] or k in columns[jaxis - 2]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis - 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis - 1][jaxis - 2] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 0 and iaxis % 3 == 2:
        #print("bottom left")
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis + 2] > 0 or k in columns[jaxis + 2]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis + 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 1][jaxis + 2] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 2]) and (
                        rows[iaxis - 2][jaxis] > 0 or k in rows[iaxis - 2]) and (
                        rows[iaxis - 2][jaxis + 1] > 0 or k in rows[iaxis - 2] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 2][jaxis + 2] > 0 or k in rows[iaxis - 2] or k in columns[jaxis + 2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    elif jaxis % 3 == 1 and iaxis % 3 == 2:
        #print("bottom middle")
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis + 1] > 0 or k in columns[jaxis + 1]) and (
                        i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis + 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 1][jaxis - 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis - 2][jaxis] > 0 or k in rows[iaxis - 2]) and (
                        rows[iaxis - 2][jaxis + 1] > 0 or k in rows[iaxis - 2] or k in columns[jaxis + 1]) and (
                        rows[iaxis - 2][jaxis - 1] > 0 or k in rows[iaxis - 2] or k in columns[jaxis - 1]):
                    return replaceValue(iaxis,jaxis,k,flatList)

    elif jaxis % 3 == 2 and iaxis % 3 == 2:
        #print("bottom right")
        possibleValue = []
        for k in range(1, 10):
            if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
                if (i[jaxis - 1] > 0 or k in columns[jaxis - 1]) and (
                        i[jaxis - 2] > 0 or k in columns[jaxis - 2]) and (
                        rows[iaxis - 1][jaxis] > 0 or k in rows[iaxis - 1]) and (
                        rows[iaxis - 1][jaxis - 1] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 1]) and (
                        rows[iaxis - 1][jaxis - 2] > 0 or k in rows[iaxis - 1] or k in columns[jaxis - 2]) and (
                        rows[iaxis - 2][jaxis] > 0 or k in rows[iaxis - 2]) and (
                        rows[iaxis - 2][jaxis - 1] > 0 or k in rows[iaxis - 2] or k in columns[jaxis - 1]) and (
                        rows[iaxis - 2][jaxis - 2] > 0 or k in rows[iaxis - 2] or k in columns[jaxis - 2]):
                    return replaceValue(iaxis,jaxis,k,flatList)


    # check other rows and columns

def rowElemination(flatList, rows, columns, threesx3, i, j, iaxis, jaxis):
    #print(iaxis, jaxis)
    square3 = get3x3index(iaxis, jaxis)
    for k in range(1, 10):
        if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
            #Check columns and boxes
            colsEleminated = 0
            for n in range(1, 9):
                if i[(jaxis+n)%9] > 0 or k in columns[(jaxis+n)%9] or k in threesx3[get3x3index(iaxis,(jaxis+n)%9)]:
                    colsEleminated += 1
            if colsEleminated == 8:
                return replaceValue(iaxis, jaxis, k, flatList)

            #Check rows and boxes
            rowsEleminated = 0
            for n in range(1, 9):
                if columns[jaxis][(iaxis+n)%9] > 0 or k in rows[(iaxis+n)%9] or k in threesx3[get3x3index((iaxis+n)%9,jaxis)]:
                    rowsEleminated += 1
            if rowsEleminated == 8:
                return replaceValue(iaxis, jaxis, k, flatList)

def possibleValuesElem(flatList, rows, columns, threesx3, i, j, iaxis, jaxis):
    square3 = get3x3index(iaxis, jaxis)
    possibleValues = []
    for k in range(1, 10):
        if k not in i and k not in threesx3[square3] and k not in columns[jaxis]:
            possibleValues.append(k)

    if len(possibleValues) == 1:
        return replaceValue(iaxis, jaxis, possibleValues[0], flatList)


USEROWELEM = 1
USEBOXELEM = 1
USEPOSELEM = 1

#Transform sudoku into list of 81 intergers
flatList = scrapdata(r'./Sudoku.txt')

#Output text file
sudukoOut = open(r'./SudokuIterations.txt', 'a')

rows, columns, threesx3 = getListsFromFlatList(flatList)

mainLogic(rows, columns, threesx3, flatList)

