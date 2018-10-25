class Activity:
    def __init__(self, id, duration, predecessors=[]):
        self.id = id
        self.duration = duration
        self.predecessors = predecessors
        self.successors = []
        self.es = None
        self.ef = None
        self.ls = None
        self.lf = None


numberOfTasks = input("How many tasks? ")
activities = []

def findEarlyFinishFromPredecessorList(arrOfTasks):
    if len(arrOfTasks) == 0:
        return 0
    elif len(arrOfTasks) == 1:
        return arrOfTasks[0].ef
    else:
        return max(task.ef for task in arrOfTasks)

def findLateStartFromSuccessorList(arrOfTasks, activities):
    if len(arrOfTasks) == 0:
        return findGreatestEarlyFinish(activities)
    elif len(arrOfTasks) == 1:
        return arrOfTasks[0].ls
    else:
        return min(task.ls for task in arrOfTasks)

def findGreatestEarlyFinish(activities):
    return max(activity.ef for activity in activities)

def walkForward(activities):
    for activity in activities:
       
        ES = findEarlyFinishFromPredecessorList(activity.predecessors) + 1
        EF = activity.duration + ES - 1

        activity.es = ES
        activity.ef = EF

def walkBackward(activities):
    activities.reverse()
    for idx,activity in enumerate(activities):

        print(activity.id)
        LF = findLateStartFromSuccessorList(activity.successors,activities) if idx == 0 else findLateStartFromSuccessorList(activity.successors,activities) - 1
        LS = LF - activity.duration + 1

        print(LF, LS)

        activity.ls = LS
        activity.lf= LF
    activities.reverse()

def criticalPath(activities):
    result = []
    for activity in activities:
        if (activity.ef - activity.lf == 0) and (activity.es - activity.ls == 0):
            result.append(activity.id)
    
    return result

for i in range(numberOfTasks):
    id = raw_input("Task ID ")
    duration = input("Task Duration")
    newPredsList = []
    
    if i != 0:
        predecessor_input = raw_input("Predecessors? ")

        predsList = predecessor_input.split(",")
        for predValue in predsList:
            for activity in activities:
                if activity.id == predValue:
                    newPredsList.append(activity)
                
        
    newActivity = Activity(id, duration, newPredsList) #newActivity = B 

    for pred in newActivity.predecessors:
        pred.successors.append(newActivity)

    activities.append(newActivity)

walkForward(activities)
walkBackward(activities)

result = criticalPath(activities)

print(result)

for activity in activities:
    print(activity.es , "------>ES")
    print(activity.ef , "------>EF")
    """print(activity.ls, "------>LS")
    print(activity.lf, "------>LF")"""








    
        

    
    