
from Main import main
import sys

if __name__ == "__main__":
    infileNum = 26

    for i in xrange(infileNum):

        inputFileName = ""
        outputFileName = ""
        if len(sys.argv) == 3:
            inputFileName = sys.argv[1] + "/input" + str(i + 1) + ".txt"
            outputFileName = sys.argv[2] + "/output" + str(i + 1) + ".txt"
        elif len(sys.argv) == 2:
            inputFileName = sys.argv[1] + "/input" + str(i + 1) + ".txt"
            outputFileName = "TestOutputs/output" + str(i + 1) + ".txt"
        elif len(sys.argv) == 1:
            inputFileName = "TestInputsAndSolutions/input" + str(i + 1) + ".txt"
            outputFileName = "TestOutputs/output" + str(i + 1) + ".txt"
        else:
            print "Usage: python Test.py [input files folder (optional)] [output files folder (optional)]"
            exit(1)

        main(inputFileName, outputFileName)