Command to run python file:
python AIProject.py

-Input to the program:
Input will be given as a CSV file whose format is given below:

CourseName, Core or Elective, Day and time appended together

e.g AI,elective,Monday1,Wednesday3

i.e. AI is an elective course which can happen on Monday at 1pm or on Wednesday at 3pm.

Last row of the CSV file contains the name of available rooms

e.g. Room1, Room2

-Program asks the user to provide the path to the inut CSV file. Preferably keep the input CSV file in the same folder as of python program.

-Then program asks the user to choose between two algorithms for the Constraint Satisfaction Problem

1) Backtracking
2) Minimum Remaining Values using Least constraing Value

-Program prints the assignment of time and day to all the courses if an assignment is possible. 
Otherwise program prints that no assignment is possible.

-Program creates a CSV file for the output as well as it prints the output on the console.
format of the output: subject name, day and time assigned, room assigned
