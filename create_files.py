import sys
import os



def createFiles(fileName):
    with open(fileName, 'r') as f:
         coord_list = f.read().splitlines()
    print(len(coord_list))
    for i in range(0, len(coord_list), 2400):
        outputFile = "outputFileNum" + str(i)
        file = open(outputFile, 'w')
        for j in range(0, 2400):
            if(i+j < len(coord_list)):
                file.write("%s\n" % coord_list[i+j])


if __name__ == '__main__':
    createFiles("coords_day1.csv")

