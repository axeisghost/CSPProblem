Two questions are created in the extra part.

1. Class Schedule Schedule
a. variables and values:
This question have five variables which stand for five classes one want to take in the upcoming semester.
The domains of variables represent the avaiable section of each classes. For example, M9,10 represent
the section is on Monday, Wednesday and Friday from 9am to 10am. T9.5,11 represents the section on Tuesday
and Thursday from 9.5am to 11am.

b. Constraints 
NotOverlapConstriant:
The sections we picked cannot overlap with each other. Therefore, each pair of classes has this binary
constraints.
LazySchedule:
Oh I have 8 am class tomorrow! No, nobody want 8am classes, so all the classes start before 9am will be
considered bad classes and will be eliminated. Also because of the rush hour around 5-6 at Atlanta, we
do not want the classes end too late. Therefore, the classes end after 14pm will be elimiated too.

2.Simplified Eight Queens
a. variables and values:
This question is a simplified form of Eight Queens problem which only have four queens instead. Each
queen is a variable. The domains contain their possible position on the 4*4 board.
b. Constraints:
NotAffectedConstraint:
Queens cannot threaten each other. Therefore, their x-axis of the position cannot be the same, y-axis
cannot be the same and the difference of x,y axis cannot be the same.
