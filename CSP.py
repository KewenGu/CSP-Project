
import operator


class CSP:
    vars = {}         # Variables
    values = {}       # Values
    limits = []       # Limits
    unaryIn = {}      # Unary inclusive
    unaryEx = {}      # Unary exclusive
    binaryEq = {}     # Binary equals
    binaryNEq = {}    # Binary not equals
    mutualIn = {}     # Mutual inclusive
    assignment = {}   # Assignments
    failFlag = False  # Failure flag

    leastConstrainingValue = False  # Using least constraining value flag
    minimumRemainingValue = False   # Using minimum remaining value flag
    forwardChecking = False         # Using forward checking flag

    # Constructor
    def __init__(self, leastConstrainingValue=True, MinimumRemainingValue=True, forwardChecking=True):
        self.leastConstrainingValue = leastConstrainingValue
        self.minimumRemainingValue = MinimumRemainingValue
        self.forwardChecking = forwardChecking

    def addVar(self, var, x):
        self.vars[var] = int(x)

    def addValue(self, value, x):
        self.values[value] = int(x)

    def addLimits(self, low, high):
        self.limits = [int(low),int(high)]

    def addUnaryIn(self, var, values):
        self.unaryIn[var] = values

    def addUnaryEx(self, var, values):
        self.unaryEx[var] = values

    def addBinaryEq(self, var, value):
        self.binaryEq[var] = value

    def addBinaryNEq(self, var, value):
        self.binaryNEq[var] = value

    def addMutualIn(self, var1, var2, value1, value2):
        self.mutualIn[var1] = [var2, value1, value2]

    def addAssignment(self, var, value):
        self.assignment[var] = value

    # Remove an assignment made previously
    def removeAssignment(self, var):
        del self.assignment[var]

    # Set fail flag
    def setFailFlag(self):
        self.failFlag = True
        return self

    # Unset the fail flag
    def resetFailFlag(self):
        self.failFlag = False

    # Return true if the constrains are all met
    def isValid(self):
        return self.checkTopLimit() and self.checkUnaryIn() and \
               self.checkUnaryEx() and self.checkBinaryEq() and \
               self.checkBinaryNEq() and self.checkMutualIn() and \
               self.checkMaxCapacity() and not self.failFlag

    # Return true if the CSP has been complete
    def isComplete(self):
        return self.isValid() and \
               self.checkBottomLimit() and \
               not self.findUnassignedVar()

    # Return the unused capacity
    def calcTotalUnusedCapacity(self):
        totalCapacity = self.calcTotalCapacity()
        return totalCapacity - sum(self.calcUsedCapacity().values())

    # Returns the total capacity of all values
    def calcTotalCapacity(self):
        return sum(self.values.values())

    # Return the current usage in value
    def calcUsedCapacity(self):
        cap = {}

        for var in self.assignment:
            if self.assignment[var] in cap:
                cap[self.assignment[var]] += self.vars[var]
            else:
                cap[self.assignment[var]] = self.vars[var]

        return cap

    # Check the maximum capacity has not been exceeded
    def checkMaxCapacity(self):
        if not self.assignment.keys():
            return True

        cap = self.calcUsedCapacity()

        for value in cap:
            if cap[value] > self.values[value]:
                return False
        return True

    # Count number of variables assigned to each value
    def countVarPerValue(self):
        count = {}

        for value in self.values:
            count[value] = 0

        for value in self.assignment.values():
            count[value] += 1

        return count

    # Check the bottom limit
    def checkBottomLimit(self):
        if not self.limits[0]:
            return True
        check = self.countVarPerValue()

        if min(check.values()) < self.limits[0]:
            return False
        return True

    # Check the top limit
    def checkTopLimit(self):
        if not self.limits[1]:
            return True
        check = self.countVarPerValue()

        if max(check.values()) > self.limits[1]:
            return False
        return True

    # Check unary inclusion constrain violation
    def checkUnaryIn(self):
        if not self.unaryIn:
            return True
        for var in self.unaryIn:
            if var in self.assignment.keys():
                if self.assignment[var] not in self.unaryIn[var]:
                    return False
        return True

    # Check unary exclusion constrain violation
    def checkUnaryEx(self):
        if not self.unaryEx:
            return True
        for var in self.unaryEx:
            if var in self.assignment.keys():
                if self.assignment[var] in self.unaryEx[var]:
                    return False
        return True

    # Check binary equality constrain violation
    def checkBinaryEq(self):
        if not self.binaryEq:
            return True
        for var in self.binaryEq:
            if var in self.assignment.keys():
                if self.binaryEq[var] in self.assignment.keys():
                    if self.assignment[var] != self.assignment[self.binaryEq[var]]:
                        return False
        return True

    # Check binary inequality constrain violation
    def checkBinaryNEq(self):
        if not self.binaryNEq:
            return True
        for var in self.binaryNEq:
            if var in self.assignment.keys():
                if self.binaryNEq[var] in self.assignment.keys():
                    if self.assignment[var] == self.assignment[self.binaryNEq[var]]:
                        return False
        return True

    # Check mutual inclusive constrain violation
    def checkMutualIn(self):
        if not self.mutualIn:
            return True
        for var in self.mutualIn:
            if var in self.assignment.keys():
                if self.mutualIn[var][0] in self.assignment.keys():
                    if (self.assignment[var] == self.mutualIn[var][1] and
                                self.assignment[self.mutualIn[var][0]] != self.mutualIn[var][2]) or \
                        (self.assignment[var] == self.mutualIn[var][2] and
                                self.assignment[self.mutualIn[var][0]] != self.mutualIn[var][1]):
                        return False
        return True

    # Returns a list of the unassigned variables
    def findUnassignedVar(self):
        unassigned = []
        for var in self.vars:
            if var not in self.assignment.keys():
                unassigned += [var]
        return unassigned

    # Returns a list of the unfilled values
    def findUnassignedValue(self):
        if not self.assignment.keys():
            return self.values.keys()

        unassigned = []

        cap = self.calcUsedCapacity()

        minWeight = min(self.vars.values())

        for value in self.values:
            if value in cap:
                if cap[value] <= self.values[value] - minWeight:
                    unassigned += value
            else:
                unassigned += value

        return unassigned

    # Count Constraints for each Variables
    def countConstraintsForVars(self):
        count = {}
        for var in self.vars:
            tempCount = 0
            if var in self.unaryIn.keys():
                tempCount += len(self.unaryIn[var])
            if var in self.unaryEx.keys():
                tempCount += len(self.unaryEx[var])
            if var in self.binaryEq.keys() or var in self.binaryEq.values():
                tempCount += 1
            if var in self.binaryNEq.keys() or var in self.binaryNEq.values():
                tempCount += 1
            if var in self.mutualIn.keys() or var in [a[0] for a in self.mutualIn.values()]:
                tempCount += 1
            count[var] = tempCount
        return count

    # Counts Constraints for each Value
    def countConstraintsForValues(self):
        count = {}
        weight = len(self.values)
        usedWeight = self.calcUsedCapacity()
        unusedWeight = {}

        for value in self.values:
            if value in usedWeight:
                unusedWeight[value] = self.values[value] - usedWeight[value]
            else:
                unusedWeight[value] = self.values[value]

        unusedWeight = sorted(unusedWeight.items(), key=operator.itemgetter(1), reverse=True)

        for value in self.values:
            tempCount = 0
            if value in self.unaryIn.values():
                for instance in self.unaryIn.values():
                    if instance == value:
                        tempCount += weight

            if value in self.unaryEx.values():
                for instance in self.unaryIn.values():
                    if instance == value:
                        tempCount += weight

            if value in self.assignment.values():
                for var in self.assignment.keys():
                    if var in self.binaryEq:
                        if self.assignment[var] == value:
                            if self.binaryEq[var] not in self.assignment:
                                tempCount += weight

                    if var in self.binaryNEq:
                        if self.assignment[var] == value:
                            if self.binaryNEq[var] not in self.assignment:
                                tempCount += weight

            count[value] = tempCount

        for value,weight in unusedWeight:
            count[value] += unusedWeight.index((value, weight))

        return count










