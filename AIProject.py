import csv
import time as TIME

#function to read CSV file and return the data read from CSV file line by line
def inputData(fileName):
    with open(fileName) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        data = []
        for line in readCSV:
            oneline = []
            for l in line:
                if l:
                    oneline.append(l)
            data.append(oneline)
        return data
    
def outputData(fileName, data):
    dataStr = ""
    for row in data:
        rowStr = ""
        for col in row:
            rowStr += col + ','
        else:
            rowStr = rowStr[:-1]
        dataStr += rowStr + '\n'
    else:
        dataStr = dataStr[:-1]
    with open(fileName, 'w') as fileOb:
        fileOb.write(dataStr)
    
#Function to find the solution of constaint satisfaction problem by using backtracking 
def backtracking(assignment,slots,level):
    if level == len(assignment):
        return True
    global subs
    global rooms
    sub = subs[level][0]
    category = subs[level][1]
    available = subs[level][2:]
    # If the course to be assigned a time and room is "core" (no other subject can clash with it in terms of time and room)
    if category == "core":
        for slot in available:
            if slots[slot] == -1:
                assignment[level] = [sub,slot,rooms[0]]
                slots[slot] = rooms[0]
                if backtracking(assignment, slots, level+1):
                    return True
                else:
                    slots[slot] = -1
                    assignment[level] = [sub,-1,-1]
        # else for "for" loop i.e if no slot is avilable for a core subject
        else:
            return False
    # If the course to be assigned a time and room is "elective"(two elective course can happen at the same time but in different rooms)
    elif (category == "elective"):                   
        for slot in available:                  
            if (slots[slot] == -1):            
                assignment[level] = [sub, slot, rooms[0]] 
                slots[slot] = [rooms[0]]      
                if (backtracking(assignment, slots, level+1)):
                    return True                
                else:
                    slots[slot] = -1
                    assignment[level] = [sub, -1, -1]
            elif (type(slots[slot]) == list):
                asRooms = slots[slot]
                temp = asRooms[:]
                if (len(asRooms) == len(rooms)):
                    continue
                asRooms.append(rooms[len(asRooms)])
                assignment[level] = [sub, slot, asRooms[-1]]
                slots[slot] = asRooms
                if (backtracking(assignment, slots, level+1)):
                    return True
                else:
                    slots[slot] = temp
                    assignment[level] = [sub, -1, -1]
        else:
            return False
        
        
        
#degreeCalculate is a helper function for the function degreeHeuristic. It calculates the degree of a variable
def degreeCalculate(mins):
    count=0
    allpossiblevalues = schedule[mins]
    for possible in allpossiblevalues:
        
        for sched in schedule:
            if possible in schedule[sched]:
                count+=1
    return count
  

def degreeHeuristic(minLengths,schedule):
    if len(minLengths) == 1:
        return minLengths[0]
    else:
        maxDegree = -1
        maxDegreeValue = ""
        for mins in minLengths:
            if not Assigned[mins]:
                degree = degreeCalculate(mins)
                if degree>maxDegree:
                    maxDegree = degree
                    maxDegreeValue = mins
        return maxDegreeValue                  


def minimumRemainingValues():
    minLength=10000
    minLengths = list()
    for sched in schedule:
        if len(schedule[sched])<minLength:
            minLength = len(schedule[sched])
    for sched in schedule:
        if len(schedule[sched])==minLength:
            minLengths.append(sched)
    variable = degreeHeuristic(minLengths,schedule)
    return variable


def leastConstrainingValue(course):
    maxCount = -1
    maxCountVal = list()
    for timeValue in schedule[course]:
        count=0
        for sched in schedule:
            if timeValue in schedule[sched]:
                count+=(len(schedule[sched])-1)
            else:
                count+=(len(schedule[sched]))
        if count>maxCount:
            maxCount = count
            maxCountVal = timeValue
    return maxCountVal


def main():
    fileName = input('Enter the path to input(CSV) file : ')
    #load the file content in inputDetails variable by calling inputData function
    inputDetails = inputData(fileName)
    
    global subs
    global rooms
    #subs has all the information given in the form Algo,core,Monday1,Monday2
    subs = inputDetails[:-1]
    #rooms has the names of avilable rooms e.g Room1,Room2
    rooms = inputDetails[-1]
    slots = {}
    assignment = []
    courseType = dict()
    for sub in subs:
        courseType[sub[0]] = sub[1]
    # print(subs)
    #Create a dictionary named schedule which has all the courses i.e variables of CSP as key and all the possible values as a combination of day and time and room are put in the value field of variable
    global schedule
    schedule = dict()
    for sub in subs:
        schedule[sub[0]] = list()
        domain = sub[2:]
        for time in domain:
            if sub[1] == "core":
                room = rooms[0]
                schedule[sub[0]].append([time,room])
            elif sub[1] == "elective":
                for room in rooms:
                    schedule[sub[0]].append([time,room])

    #Assigned is a dictionary that has False as a value for a variable that has not been assigned a value yet and True otherwise
    global Assigned
    Assigned = dict()
    for sched in schedule:
        Assigned[sched] = False
    
    #Initialize assignment and slots
    for sub in subs:
        for slot in sub[2:]:
            if slot not in slots:
                slots[slot] = -1
        assignment.append([sub[0],-1,-1])

    algoType = input("Enter the algorithm to use for 'Classroom assignment' CSP :\nEnter 1 for backtracking\nEnter 2 for Minimum Remaining Value\n")
	
    if algoType == '1':
        start = TIME.time()
        result = backtracking(assignment, slots , 0)
        end = TIME.time()
        
        print("\nTime taken by backtracking is ",end-start,'\n')
        if(result):
            outputData('output.csv', assignment)
            for assi in assignment:
                for r in assi:
                    print(r,end = ' ')
                print('\n')
        else:
            print("No assignment possible :(")
			
    elif algoType == '2':
        start = TIME.time()
        finalAssignment = dict()
        numCourses = len(schedule)

        for i in range(numCourses):
            currCourse = minimumRemainingValues()
            lcv = leastConstrainingValue(currCourse)
            if not lcv:
                print("No assignment possible")
                for sched in schedule:
                    Assigned[sched] = False
                finalAssignment.clear()
                break
            finalAssignment[currCourse] = lcv
            Assigned[currCourse] = True
            schedule.pop(currCourse)

            if courseType[currCourse] == "elective":
                for sched in schedule:
                    if lcv in schedule[sched]:
                        schedule[sched].remove(lcv)
            else:
                dayTime = lcv[0]
                for sched in schedule:
                    schedule[sched] = [x for x in schedule[sched] if x[0]!=dayTime]
        end = TIME.time()
        print("\nTime taken by Minimum Remaining Value is ",end-start,'\n')
        if finalAssignment:
            finalAssignmentList = list()
            for key,value in finalAssignment.items():
                myList = list()
                myList.append(key)
                print(key, end = ' ')
                for v in value:
                    print(v , end  = ' ')
                    myList.append(v)
                print('\n')
                finalAssignmentList.append(myList)
                
            outputData('output.csv', finalAssignmentList)
                
        
    else:
        print("Please enter valid input!")
        
        
if __name__ == '__main__':
    main()