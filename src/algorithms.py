# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 00:07:45 2016

@author: daphnehb
"""

import tools, time, random, itertools


class Solver:

    def __init__(self, grid, dictionnaire, **kwargs):
        """
        @grid Object GrilleMots
        @dictionnaire dict: Dictionnaire dont les clés sont les tailles
            et les valeurs les sous ensemble du dictionnaire
        @random bool: Shuffle le dictionnaire
        @return neighbors dict (key: numVar, value: intersect position)
        """
        self.grid = grid
        self.dictionnaire = tools.deepish_copy(dictionnaire)
        self.variables = self.grid.variables
        self.contraintes = self.grid.contraintes
        self.random = kwargs.get('random', False)
        self.runningTime = 0
        self.assignment = {}
        self.domain = {X: list(
                self.dictionnaire.get(self.contraintes.tailleFixeVars[X], list())
                ) for X in self.variables}
        if self.random:
            for numVar in self.domain:
                random.shuffle(self.domain[numVar]) # shuffle dictionnary

 #################################### Run ######################################

    def run(self, ac3=False, fc=False, cbj=False, heuristic=-1, **kwargs):
        verbose = kwargs.get("verbose", 0)
        heuristic = kwargs.get("heuristic", -1)
        if not (kwargs.get("heuristic", False) or heuristic == -1):
            if heuristic == 0:
                heuristic = self.naiveHeuristic
            elif heuristic == 1:
                heuristic = self.constrMaxHeuristic
            else:
                heuristic = self.mrvHeuristic

        if not (kwargs.get("cbj", False) or kwargs.get("fc", False) or fc or cbj):
            fc = True
        self.verbose = verbose
        if verbose > 0: print "\n"
        if ac3 or kwargs.get("ac3", False):
            if verbose > 0: print "AC3 running..."
            start = time.time()
            self.ac3()
            stop = time.time() - start
            if verbose > 0: print "{:10}: {:4}s\n".format("AC3 Running Time", stop)
            self.runningTime += stop
        # l'algo selon les parametres
        if fc or kwargs.get("fc", False):
            if verbose > 0: print "FC running..."
            start = time.time()
            instance = self.forwardChecking(first=True)
            stop = time.time() - start
            if verbose > 0: print "{:10}: {:4}s\n".format("FC Running Time", stop)
            self.runningTime += stop
        elif cbj or kwargs.get("cbj", False):
            if verbose > 0: print "CBJ running..."
            start = time.time()
            instance = self.conflictBackJumping(first=True)
            stop = time.time() - start
            if verbose > 0: print "{:10}: {:4}s\n".format("CBJ Running Time", stop)
            self.runningTime += stop
        else:
            if verbose > 0: print "{:10}: {:4}s\n".format("Solver Running Time", self.runningTime)
            return False
        if verbose > 0: print "{:15}: {:3}s\n".format("Solver Running Time", self.runningTime)
        if verbose > 0: print "Solution:\n", instance
        if isinstance(instance, dict):
            self.assignment = instance
            self.grid.fillGrid(instance)
            if verbose > 1: print self.grid.variables
            self.grid.solution = True
            return True
        else:
            assert isinstance(instance, bool), "Error, instance type is not standard"
            print "Aucune solution."
            self.grid.solution = False
            return False

 #################################### Tools ####################################

    def isComplete(self, instance):
        """
        Check if assignment has complete assigned all variables.
        @param dict (key: numVar, value: current word) - current instantiation
        @return 1-boolean
        """
        for numVar, _ in self.variables.items():
            if numVar not in instance:
                return False
        return True

    def getCommuneVars(self, numVar):
        """
        @param int (variable index)
        @return neighbors dict (key: numVar, value: intersect position)
        """
        return self.contraintes.valeurCommuneVars[numVar]

    def areLetterIntersect(self, motX, motY, indH, indV):
        """
        Intersect Constraint Check
        @param 2-words, 2-letter index
        @return 1-boolean True if valid else False
        """
        return motX[indH] == motY[indV]

    def areDifferentWords(self, motX, motY):
        """
        Word Diff Constraint Check
        @return 1-boolean True if diff else False
        """
        return not motX == motY

    def isConsistent(self, numVar_1, v, numVar_2, vv):
        """
        Checks that the assignment is consistent for this CSP.
        @param 2-int, 2-str
        @return True if it is, False if there are conflicts.
        """
        # Symetry
        if numVar_1 > numVar_2:
            tupleVar = numVar_2, numVar_1
            v, vv = vv, v
        else:
            tupleVar = numVar_1, numVar_2

        # Check letter intersection constraint
        interDict = self.contraintes.intersectIndexes
        if tupleVar in interDict and not self.areLetterIntersect(v, vv, *interDict[tupleVar]):
            return False

        # Check word uniqueness constraint
        return self.areDifferentWords(v, vv)

 #################################### AC-3 ####################################

    def ac3(self):
        """
        Check arc-consistency in CSP data structure
        """

        def revised(numVar_1, numVar_2):
            """
            Update the domain of one variable by excluding the domain value
            from the other variable (Remove inconsistent values)
            @return 1-boolean (True if we remove a value)
            """
            constraints = self.getCommuneVars(numVar_1).get(numVar_2, False)
            if not constraints:
                return False

            dX = self.domain[numVar_1]
            dY = self.domain[numVar_2]
            revised = False
            for v in list(dX):
                anyConsist = False
                for vv in dY:
                    if self.isConsistent(numVar_1, v, numVar_2, vv):
                        anyConsist = True
                        break
                if not anyConsist:
                    revised = True
                    dX.remove(v)
            assert dX, "AC3 cant made CSP consistent"
            return revised

        valCommuneVars = tools.deepish_copy(self.contraintes.valeurCommuneVars)
        queue = [(numVarX, numVarY) for numVarX in valCommuneVars for numVarY in valCommuneVars[numVarX]]
        queue = set(tuple(sorted(l)) for l in queue) # Removing permutations from queue
        while queue:
            numVarX, numVarY = queue.pop()
            if revised(numVarX, numVarY):
                for numVarK in self.getCommuneVars(numVarX):
                    if numVarK != numVarY:
                        queue.add((numVarK, numVarX))

 ################################## Heuristiques ##################################

    def mrvHeuristic(self, instance, variables):
        """
        Minimum-remaining-value (MRV) heuristic
        Variable with the smallest domain in the current assignment
        @return int
        """
        unassigned_x = {}
        vars_left = set(variables.iterkeys()) - set(instance.iterkeys())
        for numVar in vars_left:
            d = self.domain[numVar]
            if len(d) > 0:
                unassigned_x[numVar] = len(d)
        for x in sorted(unassigned_x, key=unassigned_x.get):
            return x
        assert False, "No variable found"

    def naiveHeuristic(self, instance, variables):
        """
        First item in the list of variables to instantiate
        @return int
        """
        return variables.keys()[0]

    def constrMaxHeuristic(self, instance, variables):
        """
        Variable with maximum constraints with other variables
        """
        unassigned_x = {}
        vars_left = set(variables.iterkeys()) - set(instance.iterkeys())
        for numVar in vars_left:
            c = self.getCommuneVars(numVar)
            unassigned_x[numVar] = len(c)
        max_sorted = tuple(x for x, val in unassigned_x.items() if val == max(unassigned_x.values()))
        if max_sorted:
            return random.choice(max_sorted)
        print vars_left, max(unassigned_x, key=unassigned_x.get), sorted(unassigned_x, key=unassigned_x.get)
        assert False, "No variable found"

 ############################ Forward Checking ################################

    def launchForwardChecking(self):
        return self.forwardChecking(first=True)

    def checkForward(self, numVark, v, variables):
        """
        Build every instantiation with non conflicts between variables
        @return dict of instantiation
        """
        for numVarj in variables:
            Dj = self.domain[numVarj]
            for vv in list(Dj):
                if not self.isConsistent(numVark, v, numVarj, vv):
                    Dj.remove(vv)
            if not Dj:
                return False
        return True

    def forwardChecking(self, variables={}, instance={}, **kwargs):
        """
        Search for solution and add to assignment
        @return assignment or False
        """
        if kwargs.get('first', False):
            instance = {} #iPython debug
            variables = tools.deepish_copy(self.variables)

        if not variables:
            assert self.isComplete(instance)
            return instance

        numVar = self.mrvHeuristic(instance, variables)
        variables.pop(numVar, None)
        var_orig = tools.deepish_copy(variables)
        dom_orig = tools.deepish_copy(self.domain)
        Dxk = self.domain[numVar][:]
        while Dxk:
            v = Dxk.pop()
            if self.checkForward(numVar, v, variables):
                instance[numVar] = v # Instanciation du mot
                result = self.forwardChecking(variables, instance)
                if isinstance(result, dict): # isComplete(instance) is True
                    return result
                del instance[numVar]
            variables = tools.deepish_copy(var_orig)
            self.domain = tools.deepish_copy(dom_orig)
        # aucune solution trouvée:
        #raise err.NoSolutionFoundException(self.grid)
        return False

 ################################## CBJ + FC ####################################

    def launchConflictBackJumping(self):
        return self.conflictBackJumping(self.variables,{})

    def conflictBackJumping(self, variables={}, instance={}, prevxk=None, depth=0, **kwargs):

        def consistante(instance, xk, v):
            conflict = set()
            for var, vv in instance.items():
                if not self.isConsistent(xk, v, var, vv):
                    conflict.add(y)
            return list(conflict)

        if kwargs.get("first", False):
            variables = tools.deepish_copy(self.variables)
        if not kwargs.get("heuristic", False):
            heuristic = self.mrvHeuristic
        if instance:
            assert prevxk
            prev = {prevxk}

        if not variables:
            return instance

        xk = heuristic(instance, variables)
        if not self.domain[xk]:
            return set([v for v in self.getCommuneVars(xk) if v in instance])
        conflict = set()
        nonBJ = True
        variables.pop(xk, None)
        saved_domain = dict()
        for var in variables:
            saved_domain[var] = self.domain[var][:]
        Dxk = self.domain[xk][:]
        while Dxk and nonBJ:
            v = Dxk.pop()
            if self.checkForward(xk, v, variables):
                instance_ = {xk: v}
                instance_.update(instance)
                local_conflict = consistante(instance, xk, v)
                if not local_conflict:
                    variables_ = tools.deepish_copy(variables)
                    child_conflict = self.conflictBackJumping(variables_, instance_, xk, depth+1)
                    if isinstance(child_conflict, dict):
                        return child_conflict
                    if xk in child_conflict:
                        conflict |= child_conflict
                    else:
                        conflict = child_conflict
                        nonBJ = False
                else:
                    conflict = local_conflict - {xk}
            for var, domain in saved_domain.items():
                self.domain[var] = domain
        if xk in conflict:
            conflict.remove(xk)
        if not conflict:
            conflict |= prev
        return conflict
