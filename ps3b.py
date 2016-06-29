# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''
random.seed(0)

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        chance = random.random()
        
        #print "doesClear prob. = " + str(chance)
        
        if chance > self.clearProb: 
            return False
        else: 
            return True

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        chance = random.random()
        
        #print "reproduce prob. = "+str(chance)
        #print "reproduction threashold = " + str(self.maxBirthProb * (1 - popDensity))
        
        if chance < self.maxBirthProb * (1 - popDensity): 
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException('virus particle does not reproduce')


#A = SimpleVirus(1.0, 0)
#A = SimpleVirus(1.0, 0.5)
#A = SimpleVirus(1.0, 1)
#print A.getMaxBirthProb()
#print A.getClearProb()
#print A.doesClear()
#print A.reproduce(0.2)



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO
        return len(self.viruses)      


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        unClearList = []
        for iVirus in self.viruses:
            if iVirus.doesClear():
                continue
            else:
                unClearList.append(iVirus)
        
        reproducedList = [] 
        newVirusAdded = 0         
        for jVirus in unClearList:
            reproducedList.append(jVirus)
            try: 
                popDensity = float(len(unClearList)+newVirusAdded)/self.getMaxPop()
                temp = jVirus.reproduce(popDensity) 
                reproducedList.append(temp)
                newVirusAdded += 1
            except NoChildException:
                continue
        
        self.viruses = reproducedList
        
        return len(reproducedList)           


''' 
virus = SimpleVirus(1.0, 1.0)
X = Patient([virus], 100)
X.update()
X.update()
X.update()
X.update()
print X.getTotalPop()

#--------------------------------
       
virus = SimpleVirus(1.0, 0.0)
X = Patient([virus], 100)
X.update()
X.update()
X.update()
X.update()
print X.getTotalPop()

#--------------------------------

A = SimpleVirus(1.0, 0)
B = SimpleVirus(1.0, 0.5)
C = SimpleVirus(1.0, 1)

list = [A, B, C]

X = Patient(list, 5)
print X.getViruses()
print X.getMaxPop()
print X.getTotalPop()
print X.update()

print X.getViruses()
print X.getMaxPop()
print X.getTotalPop()
'''


#
# PROBLEM 3
#

#from ps3b_precompiled_27 import * 

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO
    numVirusAllTrails = [0]*300
    
    for j in range(numTrials):
        
        virusList = []
        for i in range(numViruses):
            A = SimpleVirus(maxBirthProb, clearProb)
            virusList.append(A)
    
        X = Patient(virusList, maxPop)
    
        #numVirus = []
        for i in range(300):
            X.update()
            #numVirus.append(X.getTotalPop())
            #numVirusAllTrails.append[numVirus]
            numVirusAllTrails[i] += X.getTotalPop()

    for j in range(len(numVirusAllTrails)):
        numVirusAllTrails[j] = numVirusAllTrails[j]*1.0 / numTrials

    
    pylab.plot(numVirusAllTrails)
    pylab.xlabel('number of elapsed time steps')
    pylab.ylabel('average size of virus population in patient')
    pylab.title('No drug treatment simulation')
    pylab.legend('Average # of virus')
    pylab.show()


'''
#simulationWithoutDrug(100, 1000, 0.1, 0.05, 20)
'''                          
                          
#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        # TODO
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        # TODO
        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException('virus particle does not reproduce')           
        
        chance = random.random()
        
        #print "chance = "+str(chance)
        
        if chance < self.maxBirthProb * (1 - popDensity): 

            childResistances = {}
            for trait in self.resistances:
                chance = random.random()
                if chance < 1-self.mutProb:
                    childResistances[trait] = self.resistances[trait]
                else:
                    childResistances[trait] = not self.resistances[trait]
        else:
            raise NoChildException('virus particle does not reproduce')
            
            #for trait in childResistances:
                #print trait + " : " + str(childResistances[trait])
                                    
        return ResistantVirus(self.maxBirthProb, self.clearProb, childResistances, self.mutProb)
   
'''           
B = ResistantVirus(1.0, 0, {'a':True, 'b':False, 'c': False}, 0.0)

print B.getResistances()
print B.getMutProb()
print B.isResistantTo('b')
print B.reproduce(0.1, ['a'])
'''

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.drugsAdmin = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if newDrug not in self.drugsAdmin:
            self.drugsAdmin.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugsAdmin


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        numVirusResist = 0
        for iVirus in self.viruses:
            flag = 0
            for drug in drugResist:
                if not iVirus.isResistantTo(drug):
                    flag = 1
                    break
            if flag == 0:
                numVirusResist += 1
        
        return numVirusResist



    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        unClearList = []
        for iVirus in self.viruses:
            if iVirus.doesClear():
                continue
            else:
                unClearList.append(iVirus)
                
        #print "unClearList length = "+str(len(unClearList))
        
        reproducedList = [] 
        newVirusAdded = 0         
        for jVirus in unClearList:
            reproducedList.append(jVirus)
            try: 
                popDensity = float(len(unClearList)+newVirusAdded)/self.getMaxPop()
                #print "popDensity = "+str(popDensity)
                temp = jVirus.reproduce(popDensity, self.getPrescriptions()) 
                reproducedList.append(temp)
                newVirusAdded += 1
                
                #print temp.getResistances()
                #print temp.getMutProb()
                #print temp.isResistantTo('b')
                #print temp.reproduce(0.1, ['c'])

            except NoChildException:
                continue
        
        self.viruses = reproducedList
        
        return len(reproducedList)



'''
B = ResistantVirus(1.0, 0, {'a':True, 'b':False, 'c': False}, 0.1)
Y = TreatedPatient([B], 100)
Y.addPrescription('a')

print Y.getPrescriptions()
print Y.getResistPop('d')
print Y.getResistPop('a')
Y.update()
Y.update()
Y.update()
Y.update()
print Y.getTotalPop()
'''

#
# PROBLEM 5
#

#from ps3b_precompiled_27 import * 

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    # TODO
    numVirusAllTrails = [0]*300
    numGuttagonolResist = [0]*300
    
    for j in range(numTrials):
        
        virusList = []
        for i in range(numViruses):
            B = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            virusList.append(B)
    
        Y = TreatedPatient(virusList, maxPop)
    
        for i in range(150):
            Y.update()
            numVirusAllTrails[i] += Y.getTotalPop()
            numGuttagonolResist[i] += Y.getResistPop(['guttagonol'])
            #print "before: "+str(Y.getResistPop(['guttagonol']))
            
        Y.addPrescription('guttagonol')
        
        for i in range(150):
            Y.update()
            numVirusAllTrails[i+150] += Y.getTotalPop()
            numGuttagonolResist[i+150] += Y.getResistPop(['guttagonol'])
            #print "after: "+str(Y.getResistPop(['guttagonol']))
        

    for j in range(len(numVirusAllTrails)):
        numVirusAllTrails[j] = numVirusAllTrails[j]*1.0 / numTrials
        numGuttagonolResist[j] = numGuttagonolResist[j]*1.0 / numTrials

    
    pylab.plot(numVirusAllTrails, label = 'Average # of virus')
    pylab.plot(numGuttagonolResist, label = 'Average # of guttagonol-resistant virus')
    
    pylab.xlabel('number of elapsed time steps')
    pylab.ylabel('average size of virus population in patient')
    pylab.title('')
    #pylab.legend()
    pylab.show()


simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 10)