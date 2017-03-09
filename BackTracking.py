
from copy import deepcopy
import operator


class BackTracking:

    # Back tracking algorithm
    def backtrackSearch(self, csp):
        return self.backtrack(csp)

    def backtrack(self, p):
        csp = deepcopy(p)

        if csp.isComplete():
            return csp

        var = self.selectUnassignedVariable(csp)

        if var not in csp.vars:
            return csp

        for value in self.orderDomainValues(csp):

            csp.addAssignment(var, value)
            inferences = self.inference(csp, var, value)

            for iVar,iValue in inferences:
                csp.addAssignment(iVar, iValue)
            if csp.isValid():
                result = self.backtrack(csp)
                if result.isValid():
                    return result

            csp.removeAssignment(var)
            for iVar,iValue in inferences:
                csp.removeAssignment(iVar)
            csp.resetFailFlag()

        return csp.setFailFlag()


    # Select the next variables to expand - Minimal Remaining Value
    def selectUnassignedVariable(self, csp):
        unassigned = csp.findUnassignedVar()

        if not csp.minimumRemainingValue:
            if not unassigned:
                return -float('infinity')
            return unassigned[0]

        tempMaxVar = -float('infinity')
        tempMaxCount = -float('infinity')

        constraints = csp.countConstraintsForVars()

        for var in unassigned:
            if constraints[var] >= tempMaxCount:
                tempMaxCount = constraints[var]
                tempMaxVar = var

        return tempMaxVar


    # Return the next value to use - Least Constraining Value
    def orderDomainValues(self, csp):
        unassigned = csp.findUnassignedValue()

        if not csp.leastConstrainingValue:
            return unassigned

        constraints = csp.countConstraintsForValues()
        order = []

        sortedConstraints = sorted(constraints.items(), key=operator.itemgetter(1))

        for value in sortedConstraints:
            if value[0] in unassigned:
                order += value[0]

        return order


    # Forward Checking
    def inference(self, csp, var, value):
        if not csp.forwardChecking:
            return []

        inferences = []

        if var in csp.binaryEq:
            inferences += [(csp.binaryEq[var], value)]
        if var in csp.binaryEq.values():
            for var2 in csp.binaryEq:
                if csp.binaryEq[var2] == var:
                    inferences += [(var2, value)]

        return inferences
