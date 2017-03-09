
from CSP import CSP
from BackTracking import BackTracking
import sys
import time


def run(inFileName, outFileName):

    # Open file for reading
    infile = open(inFileName, 'r')

    # Create the CSP object
    # the three bool corresponding to LCV, MRV, and Forward checking
    csp = CSP(True, True, True)

    # Read the input file
    read(infile, csp)

    # Run back tracking search, and record time elapsed
    start = time.time()
    bt = BackTracking()
    result = bt.backtrackSearch(csp)
    end = time.time()
    execuTime = (end - start) * 1000

    # Print output to console
    print "==============================="
    if not result.isComplete():
        print "Assignment not possible..."
        # if result.checkTopLimit():
        #     print "checkTopLimit failed"
        # if result.checkBottomLimit():
        #     print "checkBottomLimit failed"
        # if result.checkUnaryIn():
        #     print "checkUnaryIn failed"
        # if result.checkUnaryEx():
        #     print "checkUnaryEx failed"
        # if result.checkBinaryEq():
        #     print "checkBinaryEq failed"
        # if result.checkBinaryNEq():
        #     print "checkBinaryNEq failed"
        # if result.checkMutualIn():
        #     print "checkMutualIn failed"
        # if result.checkMaxCapacity():
        #     print "checkMaxCapacity failed"
        print "==============================="
        exit(1)

    else:
        print "Assignment Complete..."
    print "Execution time: " + str(execuTime) + " milliseconds"
    print "==============================="

    # Write final result to output file
    outfile = open(outFileName, 'w')
    write(outfile, result)
    exit(0)


# Reads from the input file, and create a CSP for it
def read(infile, csp):
    section = 0
    for line in infile.readlines():
        line = line.split()

        if line[0] == "#####":
            section += 1

        elif section == 1:  # Read Variables
            csp.addVar(line[0], line[1])

        elif section == 2:  # Read Values
            csp.addValue(line[0], line[1])

        elif section == 3:  # Read Limits
            csp.addLimits(line[0], line[1])

        elif section == 4:  # Read Unary Inclusive
            csp.addUnaryIn(line[0], line[1:len(line)])

        elif section == 5:  # Read Unary Exclusive
            csp.addUnaryEx(line[0], line[1:len(line)])

        elif section == 6:  # Read Binary Equals
            csp.addBinaryEq(line[0], line[1])

        elif section == 7:  # Read Binary NOT Equals
            csp.addBinaryNEq(line[0], line[1])

        elif section == 8:  # Mutual Inclusion
            csp.addMutualIn(line[0], line[2], line[1], line[3])

    # In case the limits are not given
    if not csp.limits:
        csp.limits = [0, len(csp.vars)]


# Write output to file
def write(outfile, csp):
    if not csp.isComplete():
        outfile.write("no solution")
        return
    cap = csp.calcUsedCapacity()
    for value in csp.values:
        if value in cap.keys():
            outfile.write(value + ' ')
            count = 0
            for var in csp.assignment:
                if csp.assignment[var] == value:
                    outfile.write(var + ' ')
                    count += 1
            outfile.write("\nnumber of Items: " + str(count) + '\n')
            outfile.write("total Weight: " + str(cap[value]) + '/' + str(csp.values[value]) + '\n')
            outfile.write("waster Capacity: " + str(csp.values[value] - cap[value]) + '\n\n')


if __name__ == "__main__":
    inFileName = ""
    outFileName = ""
    # Read input and output file names
    if len(sys.argv) == 2:
        inFileName = sys.argv[1]
        outFileName = "output.txt"
    elif len(sys.argv) == 3:
        inFileName = sys.argv[1]
        outFileName = sys.argv[2]
    else:
        print "Usage: python Main.py [input file name] [output file name (optional)]"
        exit(1)
    # Run the program
    run(inFileName, outFileName)