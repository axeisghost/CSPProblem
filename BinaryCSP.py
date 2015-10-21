from collections import deque
import sys
"""
	Base class for unary constraints
	Implement isSatisfied in subclass to use
"""
class UnaryConstraint:
	def __init__(self, var):
		self.var = var

	def isSatisfied(self, value):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var

class LazySchedule(UnaryConstraint):
	def isSatisfied(self, value):
		start = float(value[1:].split(',')[0])
		end = float(value[1:].split(',')[1])
		if (start < 9):
			return False
		if (end > 14):
			return False
		return True
"""	
	Implementation of UnaryConstraint
	Satisfied if value does not match passed in paramater
"""
class BadValueConstraint(UnaryConstraint):
	def __init__(self, var, badValue):
		self.var = var
		self.badValue = badValue

	def isSatisfied(self, value):
		return not value == self.badValue

	def __repr__(self):
		return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""	
	Implementation of UnaryConstraint
	Satisfied if value matches passed in paramater
"""
class GoodValueConstraint(UnaryConstraint):
	def __init__(self, var, goodValue):
		self.var = var
		self.goodValue = goodValue

	def isSatisfied(self, value):
		return value == self.goodValue

	def __repr__(self):
		return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
	Base class for binary constraints
	Implement isSatisfied in subclass to use
"""
class BinaryConstraint:
	def __init__(self, var1, var2):
		self.var1 = var1
		self.var2 = var2

	def isSatisfied(self, value1, value2):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var1 or var == self.var2

	def otherVariable(self, var):
		if var == self.var1:
			return self.var2
		return self.var1
class NotOverlapConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if (value1[0] != value2[0]):
			return True
		else:
			start1 = float(value1[1:].split(',')[0])
			start2 = float(value2[1:].split(',')[0])
			end1 = float(value1[1:].split(',')[1])
			end2 = float(value2[1:].split(',')[1])
			if (start1 == start2 or (start1 > start2 and start1 < end2)):
				return False
			if (end1 == end2) or (end1 < end2 and end1 > start2):
				return False
			return True
class NotAffectedConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if (int(value1[0]) == int(value2[0])):
			return False
		if (int(value1[1]) == int(value2[1])):
			return False
		if (abs(int(value1[1]) - int(value2[1])) == abs(int(value1[0]) - int(value2[0]))):
			return False
		return True

"""
	Implementation of BinaryConstraint
	Satisfied if both values assigned are different
"""
class NotEqualConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if value1 == value2:
			return False
		return True

	def __repr__(self):
	    return 'BadValueConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
	"""
	Structure of a constraint satisfaction problem.
	Variables and domains should be lists of equal length that have the same order.
	varDomains is a dictionary mapping variables to possible domains.

	Args:
		variables (list<string>): a list of variable names
		domains (list<set<value>>): a list of sets of domains for each variable
		binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
		unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
	"""
	def __init__(self, variables, domains, binaryConstraints = [], unaryConstraints = []):
		self.varDomains = {}
		for i in xrange(len(variables)):
			self.varDomains[variables[i]] = domains[i]
		self.binaryConstraints = binaryConstraints
		self.unaryConstraints = unaryConstraints

	def __repr__(self):
	    return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % ( \
	        ''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
	        ''.join([str(e) + '\n' for e in self.binaryConstraints]), \
	        ''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
	"""
	Representation of a partial assignment.
	Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
	Keeps a second dictionary from variables to assigned values, with None being no assignment.

	Args:
		csp (ConstraintSatisfactionProblem): the problem definition for this assignment
	"""
	def __init__(self, csp):
		self.varDomains = {}
		for var in csp.varDomains:
			self.varDomains[var] = set(csp.varDomains[var])
		self.assignedValues = { var: None for var in self.varDomains }

	"""
	Determines whether this variable has been assigned.

	Args:
		var (string): the variable to be checked if assigned
	Returns:
		boolean
		True if var is assigned, False otherwise
	"""
	def isAssigned(self, var):
		return self.assignedValues[var] != None

	"""
	Determines whether this problem has all variables assigned.

	Returns:
		boolean
		True if assignment is complete, False otherwise
	"""
	def isComplete(self):
		for var in self.assignedValues:
			if not self.isAssigned(var):
				return False
		return True

	"""
	Gets the solution in the form of a dictionary.

	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if not complete.
	"""
	def extractSolution(self):
		if not self.isComplete():
			return None
		return self.assignedValues

	def __repr__(self):
	    return '---Variable Domains\n%s---Assigned Values\n%s' % ( \
	        ''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
	        ''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))



####################################################################################################


"""
	Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
	Do not assign value to var. Only check if this value would be consistent or not.
	If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.

	Args:
		assignment (Assignment): the partial assignment
		csp (ConstraintSatisfactionProblem): the problem definition
		var (string): the variable that would be assigned
		value (value): the value that would be assigned to the variable
	Returns:
		boolean
		True if the value would be consistent with all currently assigned values, False otherwise
"""
def consistent(assignment, csp, var, value):
	for cons in csp.binaryConstraints:
		if (cons.affects(var)):
			if (assignment.isAssigned(cons.otherVariable(var))):
				if (not (cons.isSatisfied(value, assignment.assignedValues[cons.otherVariable(var)]))):
					return False
	return True


"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.

	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
	next = selectVariableMethod(assignment, csp)
	avaliableVal = orderValuesMethod(assignment, csp, next)
	for nextval in avaliableVal:
		if (consistent(assignment, csp, next, nextval)):
			assignment.assignedValues[next] = nextval
			if (assignment.isComplete()):
				return assignment
			result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
			if (result):
				return result
	assignment.assignedValues[next] = None
	return None


"""
	Uses unary constraints to eleminate values from an assignment.

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
	Returns:
		Assignment
		An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
	domains = assignment.varDomains
	for var in domains:
		for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
			for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
				domains[var].remove(value)
				if len(domains[var]) == 0:
				 	# Failure due to invalid assignment
				 	return None
	return assignment


"""
	Trivial method for choosing the next variable to assign.
	Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
	for var in csp.varDomains:
		if not assignment.isAssigned(var):
			return var


"""
	Selects the next variable to try to give a value to in an assignment.
	Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		the next variable to assign
"""
def minimumRemainingValuesHeuristic(assignment, csp):
	nextVar = None
	domains = assignment.varDomains
	minDomain = sys.maxint
	degrees = {}
	for var in domains:
		degrees[var] = calculateDegree(var, csp)
	degree = 0
	for var in domains:
		if (not assignment.isAssigned(var)):
			if (len(domains[var]) < minDomain):
				minDomain = len(domains[var])
				degree = degrees[var]
				nextVar = var
			elif (len(domains[var]) == minDomain):
				if (degrees[var] >degree):
					degree = degrees[var]
					nextVar = var
	return nextVar

def calculateDegree(var, csp):
	count = 0
	for cons in csp.binaryConstraints:
		if (cons.affects(var)):
			count = count + 1
	return count

"""
	Trivial method for ordering values to assign.
	Uses no heuristics.
"""
def orderValues(assignment, csp, var):
	return list(assignment.varDomains[var])


"""
	Creates an ordered list of the remaining values left for a given variable.
	Values should be attempted in the order returned.
	The least constraining value should be at the front of the list.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable to be assigned the values
	Returns:
		list<values>
		a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
	values = []
	prior = []
	involved = []
	for cons in csp.binaryConstraints:
		if (cons.affects(var)):
			involved.append(cons)
	for value in assignment.varDomains[var]:
		count = 0
		for cons in involved:
			if (cons.affects(var)):
				for otherValue in assignment.varDomains[cons.otherVariable(var)]:
					if (not cons.isSatisfied(value, otherValue)):
						count = count + 1
		if (not values):
			values.append(value)
			prior.append(count)
		else:
			ind = 0
			while (ind < len(values)):
				if (count < prior[ind]):
					break
				else:
					ind = ind + 1
			values.insert(ind, value)
			prior.insert(ind, count)
	return values


"""
	Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
	return set([])


"""
	Implements the forward checking algorithm.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
	inferences = set([])
	domains = assignment.varDomains
	for cons in csp.binaryConstraints:
		if (cons.affects(var)):
			if (not assignment.isAssigned(cons.otherVariable(var))):
				tempdomain = domains[cons.otherVariable(var)]
				for possibleVal in tempdomain:
					if (not cons.isSatisfied(possibleVal, value)):
						if (len(domains[cons.otherVariable(var)]) <= 1):
							return None
						else:
							inferences.add((cons.otherVariable(var), possibleVal))
	for change in inferences:
		domains[change[0]].remove(change[1])
	return inferences

"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.

	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.


	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking


	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
		inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
				Can be forwardChecking or maintainArcConsistency
	Returns:
		Assignment

		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
	next = selectVariableMethod(assignment, csp)
	avaliableVal = orderValuesMethod(assignment, csp, next)
	for nextval in avaliableVal:
		if (consistent(assignment, csp, next, nextval)):
			# print ('Var: ' + next + ' ' + 'Val: ' + nextval)
			assignment.assignedValues[next] = nextval
			if (assignment.isComplete()):
				return assignment
			inference = inferenceMethod(assignment, csp, next, nextval)
			if (inference != None):
				# print assignment.varDomains
				result = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
			else:
				continue
			if (result):
				return result
			else:
				for recover in inference:
					assignment.varDomains[recover[0]].add(recover[1])
	# print assignment.assignedValues
	assignment.assignedValues[next] = None
	# print assignment.assignedValues
	return None


"""
	Helper funciton to maintainArcConsistency and AC3.
	Remove values from var2 domain if constraint cannot be satisfied.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var1 (string): the variable with consistent values
		var2 (string): the variable that should have inconsistent values removed
		constraint (BinaryConstraint): the constraint connecting var1 and var2
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def revise(assignment, csp, var1, var2, constraint):
	inferences = set([])
	for var2Val in assignment.varDomains[var2]:
		con = False
		for var1Val in assignment.varDomains[var1]:
			if (constraint.isSatisfied(var1Val, var2Val)):
				con = True
		if (not con):
			inferences.add((var2, var2Val))
	if (len(inferences) >= len(assignment.varDomains[var2])):
		return None
	else:
		for change in inferences:
			assignment.varDomains[change[0]].remove(change[1])
	return inferences


"""
	Implements the maintaining arc consistency algorithm.
	Inferences take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
 rences made in this call or None if inconsistent assignment
"""
def maintainArcConsistency(assignment, csp, var, value):
	inferences = set([])
	MACqueue = set([])
	domains = assignment.varDomains
	for cons in csp.binaryConstraints:
		if (cons.affects(var)):
			if (not assignment.isAssigned(cons.otherVariable(var))):
				tempdomain = domains[cons.otherVariable(var)]
				for possibleVal in tempdomain:
					if (not cons.isSatisfied(possibleVal, value)):
						if (len(domains[cons.otherVariable(var)]) <= 1):
							return None
						else:
							inferences.add((cons.otherVariable(var), possibleVal))
							MACqueue.add((var, cons.otherVariable(var), cons))
	for change in inferences:
		domains[change[0]].remove(change[1])
	MACqueue = list(MACqueue)
	while (len(MACqueue) > 0):
		curr = MACqueue.pop()
		if (curr[0] == var):
			for cons in csp.binaryConstraints:
				if (cons.affects(curr[1])):
					if (cons.otherVariable(curr[1]) != curr[0] and (not assignment.isAssigned(cons.otherVariable(curr[1])))):
							MACqueue.insert(0, (curr[1], cons.otherVariable(curr[1]), cons))
		else:
			revised = revise(assignment, csp, curr[0], curr[1], curr[2])
			if (revised == None):
				for recover in inferences:
					assignment.varDomains[recover[0]].add(recover[1])
				return None
			elif (len(revised) > 0):
				inferences.update(revised)
				for changed in revised:
					for cons in csp.binaryConstraints:
						if (cons.affects(changed[0])):
							if (cons.otherVariable(changed[0]) != curr[0] and (not assignment.isAssigned(cons.otherVariable(changed[0])))):
								MACqueue.insert(0, (changed[0], cons.otherVariable(changed[0]), cons))
	return inferences


"""
	AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
	before running recursive backtracking.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		Assignment
		the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
	inferences = set([])
	MACqueue = []
	for cons in csp.binaryConstraints:
		MACqueue.insert(0,(cons.var1, cons.var2, cons))
		MACqueue.insert(0,(cons.var2, cons.var1, cons))
	while (len(MACqueue) > 0):
		curr = MACqueue.pop()
		revised = revise(assignment, csp, curr[0], curr[1], curr[2])
		if (revised == None):
			return None
		elif (len(revised) > 0):
			for changed in revised:
				for cons in csp.binaryConstraints:
					if (cons.affects(changed[0])):
						if (cons.otherVariable(changed[0]) != curr[0]):
							MACqueue.insert(0, (changed[0], cons.otherVariable(changed[0]), cons))
	return assignment


"""
	Solves a binary constraint satisfaction problem.

	Args:
		csp (ConstraintSatisfactionProblem): a CSP to be solved
		orderValuesMethod (function): a function to decide the next value to try
		selectVariableMethod (function): a function to decide which variable to assign next
		inferenceMethod (function): a function to specify what type of inferences to use
		useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
	assignment = Assignment(csp)
	assignment = eliminateUnaryConstraints(assignment, csp)
	if assignment == None:
		return assignment

	if useAC3:
		assignment = AC3(assignment, csp)
		if assignment == None:
			return assignment
	if inferenceMethod is None or inferenceMethod==noInferences:
		assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	else:
		assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
	if assignment == None:
		return assignment

	return assignment.extractSolution()
