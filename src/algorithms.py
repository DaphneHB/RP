# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 00:07:45 2016

@author: daphnehb
"""

import tools, time, random, itertools


class Solver:

    def __init__(self, grid, dictionnaire, **kwargs):
        self.grid = grid
        self.dictionnaire = tools.deepish_copy(dictionnaire)
        self.variables = self.grid.variables
        self.contraintes = self.grid.contraintes
        self.domain = {X: list(
                self.dictionnaire.get(self.contraintes.tailleFixeVars[X], list())
                ) for X in self.variables}
        self.random = kwargs.get('random', False)
        self.runningTime = 0
        if self.random:
            for numVar in self.domain:
                random.shuffle(self.domain[numVar]) # shuffle dictionnary

    def run(self, ac3=False, fc=False, cbj=False, **kwargs):
        verbose = kwargs.get("verbose", 0)
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
            self.grid.fillGrid(instance)
            if verbose > 1: print self.grid.variables
            self.grid.solution = True
            return True
        else:
            assert isinstance(instance, bool), "Error, instance type is not standard"
            print "Aucune solution."
            self.grid.solution = False
            return False

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
            dX = self.domain[numVarX]
            dY = self.domain[numVarY]
            revised = False
            for v in list(dX):
                # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
                if not any(self.isConsistent(numVar_1, v, numVar_2, vv) for vv in dY):
                    revised = True
                    dX.remove(v)
            assert dX, "AC3 cant made CSP consistent"
            return revised

        valCommuneVars = tools.deepish_copy(self.contraintes.valeurCommuneVars)
        queue = [(numVarX, numVarY) for numVarX in valCommuneVars for numVarY in valCommuneVars[numVarX]]
        queue = set(tuple(sorted(l)) for l in queue) # Removing permutations from queue
        while queue:
            numVarX, numVarY = queue.pop()
            revised(numVarX, numVarY)

    def mrv(self, instance, variables):
        """
        Minimum-remaining-value (MRV) heuristic
        @return the variable from amongst those that have the fewest legal values
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

    def launchForwardChecking(self):
        return self.forwardChecking(first=True)

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

        numVar = self.mrv(instance, variables)
        variables.pop(numVar, None)
        var_orig = tools.deepish_copy(variables)
        dom_orig = tools.deepish_copy(self.domain)
        for v in self.domain[numVar]:
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

    def isInstanceConsistent(self, instance, numVar, v):
        interDict = self.contraintes.intersectIndexes
        c1_conflict = set()
        c2_conflict = set()
        for var in instance:
            if var == numVar:
                continue
            if var > numVar:
                tupleVar = numVar, var
                v_ = v
                vv_ = instance[var]
            else:
                tupleVar = var, numVar
                v_ = instance[var]
                vv_ = v
            if not c2_conflict and not self.areDifferentWords(v_, vv_):
                c1_conflict.add(var)
            if not c1_conflict and tupleVar in interDict and not self.areLetterIntersect(v_, vv_, *interDict[tupleVar]):
                c2_conflict.add(var)
        return c1_conflict | c2_conflict

    def launchConflictBackJumping(self):
        return self.conflictBackJumping(self.variables,{})

    def conflictBackJumping(self, variables={}, instance={}, depth=0, **kwargs):
        """
        CBJ fait appel à la fonction consistante qui recoit une
        instanciation et retourne l'ens des variables de la contrainte
        violée si i est inconsistante.
        """

        if kwargs.get('first', False):
            instance = {} #iPython debug
            variables = tools.deepish_copy(self.variables)

        if not variables:
            assert self.isComplete(instance)
            return instance

        if depth == 0:
            self.dom_orig = tools.deepish_copy(self.domain)

        numVar = depth+1
        self.domain[numVar] = tools.deepish_copy(self.dom_orig)[numVar]
        conflict = set()
        nonBJ = True
        for v in self.domain[numVar]:
            if not nonBJ: break
            local_conflict = self.isInstanceConsistent(instance, numVar, v)
            if len(local_conflict) == 0:
                variables_ = tools.deepish_copy(variables)
                variables_.pop(numVar, None)
                instance_ = tools.deepish_copy(instance)
                instance_[numVar] = v
                child_conflict = self.conflictBackJumping(variables_, instance_, depth+1)
                if numVar in child_conflict:
                    conflict |= child_conflict - {numVar}
                else:
                    #print instance, depth, len(self.domain[numVar])
                    return child_conflict
            else:
                self.domain[numVar].remove(v)
                conflict |= local_conflict
        return conflict
