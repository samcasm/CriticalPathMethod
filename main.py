import activityClass  # constructor class for each activity
import sys
import csv


# import csv
file_name = sys.argv[1]
data = []
for row in csv.reader(open(file_name)):
    newrow = ",".join(row)
    newrow = newrow.replace('\t', ' ')
    data.append(newrow)

csvdata = map(lambda x: x.split(' '), data)


def findEarlyFinishFromPredecessorList(predecessorList):
    if len(predecessorList) == 0:
        return 0
    elif len(predecessorList) == 1:
        return predecessorList[0].ef
    else:
        return max(task.ef for task in predecessorList)


def findLateStartFromSuccessorList(successorList, activities):
    if len(successorList) == 0:  # if last node find greatest early finish from all activities
        return max(activity.ef for activity in activities)
    elif len(successorList) == 1:
        return successorList[0].ls
    else:
        return min(task.ls for task in successorList)


def walkForward(activities):
    for activity in activities:

        ES = findEarlyFinishFromPredecessorList(activity.predecessors) + 1
        EF = activity.duration + ES - 1

        activity.es = ES
        activity.ef = EF


def walkBackward(activities):
    activities.reverse()  # Reverse the tasks in place for backward walking
    for activity in activities:

        if len(activity.successors) == 0:
            LF = findLateStartFromSuccessorList(
                activity.successors, activities)
        else:
            LF = findLateStartFromSuccessorList(
                activity.successors, activities) - 1

        LS = LF - activity.duration + 1

        activity.ls = LS
        activity.lf = LF

    activities.reverse()  # Once done backward walking reverse the tasks in place


def criticalPathCalculator(activities):
    criticalPath = []
    for activity in activities:
        if (activity.ef - activity.lf == 0) and (activity.es - activity.ls == 0):
            criticalPath.append(activity.id)

    return criticalPath


def calculateSlack(activities):
    for activity in activities:
        if (activity.ls - activity.es) == (activity.lf - activity.ef):
            activity.slack = activity.ls - activity.es
        else:
            print("Error: The slacks do not match. Incorrect")
            sys.exit(1)


# Create activities list
print("**************  CRITICAL PATH CALCULATOR  *****************\n")

numberOfTasks = len(csvdata)
activities = []  # where all the tasks given by the user are stored

for row in csvdata:
    #print(row, "check inputs debugger")
    id = str(row[0])
    duration = int(row[1])
    predecessor_input = "" if row[2].upper() == "NA" else row[2]
    newPredsList = []

    # Split multiple predecessors
    predsList = predecessor_input.upper().replace(" ", "").split(",")

    # find each predecessor object in activities list and append to the predecessors list of current activity
    for predValue in predsList:
        for activity in activities:
            if activity.id == predValue:
                newPredsList.append(activity)

    # create a new activity object from Activity constructor
    newActivity = activityClass.Activity(id, duration, newPredsList)

    # Current activity will be a successor to all in its predeccesor list
    for pred in newActivity.predecessors:
        pred.successors.append(newActivity)

    # finally add newActivity to list of activities
    activities.append(newActivity)


walkForward(activities)  # find early start and early finish of each activity
walkBackward(activities)  # find late start and late finish of each activity


calculateSlack(activities)
criticalPath = criticalPathCalculator(activities)

firstTasks = filter(lambda x: len(x.predecessors) == 0, activities)
lastTasks = filter(lambda x: len(x.successors) == 0, activities)

print("Number of Schedule Tasks: " + str(len(activities)))
print("----------------------FIRST TASKS ---------------------------------")
print("First Tasks Count: " + str(len(firstTasks)) +
      "\n" + str(map(lambda x: x.id, firstTasks)))
print("----------------------LAST TASKS ---------------------------------")
print("Last Tasks Count: " + str(len(lastTasks)) +
      "\n" + str(map(lambda x: x.id, lastTasks)))
print("-----------------------------------------------------------------------")

print("====================  SCHEDULE / PROJECT TASKS =====================\n\n")

for activity in activities:
    if activity.id in criticalPath:
        isCritical = "Yes"
    else:
        isCritical = "No"

    activityPredecessors = map(lambda pred: pred.id, activity.predecessors)
    activitySuccessors = map(lambda succ: succ.id, activity.successors)

    print("Task: " + str(activity.id) +
          "  Dur: " + str(activity.duration) +
          "  ES: Day " + str(activity.es) +
          "  LS: Day " + str(activity.ls) +
          "  EF: Day " + str(activity.ef) +
          "  LF: Day" + str(activity.lf) +
          "  Slack: " + str(activity.slack) +
          "  Is Critical: " + str(isCritical))
    print("Predecessors: " + str(activityPredecessors) +
          "  Successors: " + str(activitySuccessors))

print("\n\n====================     SCHEDULE SUMMARY     =====================\n")
finishDay = max(task.lf for task in activities)
startDay = min(task.es for task in activities)
print("Start Day: " + str(startDay) + " Finish Day: " +
      str(finishDay) + "  Duration: " + str(finishDay) + " Days\n")
print("Critical Path: " + str(criticalPath))

print("\n====================    END     =====================\n")
