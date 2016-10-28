Scheduler
==========
Written in Python.

Problem Statement
---------------
Given a JSON file with courses and lists of prerequisites for each course, print out courses in an order that they can be taken. All prerequisites for a course need to be printed before the course itself can be printed.

Problem Solution
---------------
###Key Data Structures
- prerequisities dictionary: key is a course name, value is a set of courses that are prerequisities to key's course
- dependencies dictionary: key is a course name, value is a set of courses that depend on key's course, meaning that the key's course is a prerequisite to all of the courses stored in the value set
- taken set: courses that have been printed already
- queue: courses that are ready to get printed

###Steps
1. Iterate through each course given in the input file.
2. Print out courses that have no prerequisites or courses where each of its prerequisites are in taken. Add the printed course to taken.
3. When a course C gets printed out:
    a. Get all courses that depend on C by using the dependencies dictionary (if C exists in that dictionary). 
    b. For each of those courses, delete C from its prerequisites in the prerequisites dictionary.
    c. If there are no more unprinted prerequisites for any of those courses, print the course out. Otherwise, add the course to the queue. 
    d. Delete C from the dependencies dictionary, since all courses with C as a prerequisite have now all removed C as a prerequisite. C is already not in prerequisities, otherwise it wouldn't have been printed in the first place.
    Note: Each course will only be added to the queue a maximum of on time, because there will only be one time during which all of its prerequisites turn to zero - namely when its last prerequisite gets printed out.
4. If a course has prerequisites not in taken:
    a. Add an entry to prerequisities with course as key and a set of all of its prerequisites that are not in taken as value.
    b. Add an entry to dependencies with each prerequisite that is not in taken as key, and create or add course to set of values (if it already exists).
5. Finish processing each course once.
6. Loop through the queue until no more elements exist.
    a. Upon getting dequeued, a course will automatically get printed. Do step 3.

###Assumptions
- JSON file is correctly formatted, meaning a list is given, with course names as strings, prerequisites as lists.
- Each course name is unique and will only have one list of prerequisites (ie one course will not show up as the key twice in the JSON file).

###Test Cases
- Given <Course>: [<prerequisities>] of A: [], B: [], C: [A, B], D: [C]:
    - File order of A B C D (all prerequisites are listed before courses that have those prerequisites)
    - File order of D C A B (all prerequisites are listed after courses that have those prerequisites)
    - File order of A C B D (for a given course, some of its prerequisites are listed before the course and some are listed after)
    - File order of C D A B (some prerequisites are listed before and some are listed after courses that have those prerequisites)
- No file is passed into the command line.
- Provided file does not exist.
- Circular dependencies are identified.

### Example Run-Through
Given <Course>: [<prerequisities>] of C: [A, B], A: [], B: [], D: [C]:

1. First process C: [A, B]. Since neither A nor B is in taken yet:
    - Add an entry to prerequisites with C as key, set(A, B) as value.
    - Add an entry to dependencies with A as key and set(C) as value, as well as B as key and set(C) as value.
    - Summary: prerequisites = { C: set(A, B) }; dependencies = { A: set(C), B: set(C) }; queue = (); taken = (); nothing printed yet
2. Next, process A: []. 
    - Since A has no prerequisites, print A out and add it to taken.
    - Get all courses that depend on A by using the dependencies dictionary: dependencies[A] = set(C).
    - For C, delete A from its prerequisites in the prerequisites dictionary: prerequisites[C].delete(A).
    - prerequisites[C] isn't empty yet, so we can't add C into the queue yet.
    - Since A is printed, delete it from dependencies.
    - Summary: prerequisites = { C: set(B) }; dependencies = { B: set(C) }; queue = (); taken = (A); A has been printed
3. Next, process B: []. 
    - Since B has no prerequisites, print B out and add it to taken.
    - Get all courses that depend on B by using the dependencies dictionary: dependencies[B] = set(C).
    - For C, delete B from its prerequisites in the prerequisites dictionary: prerequisites[C].delete(B).
    - prerequisites[C] is now empty, so add C to the queue.
    - Since B is printed, delete it from dependencies.
    - Summary: prerequisites = {}; dependencies = {}; queue = (C); taken = (A, B); A, B have been printed in that order
4. Next, process D: [C]. Since C is not in taken yet:
    - Add an entry to prerequisites with D as key, set(C) as value.
    - Add an entry to dependencies with C as key and set(D) as value.
    - Summary: prerequisites = { D: set(C) }; dependencies = { C: set(D) }; queue = (C); taken = (A, B); A, B have been printed in that order
5. We're finally done processing the data once. Now, onto the queue!
6. C is the only item on the queue, so let's process it:
    - Print C and add to taken.
    - Get all courses that depend on C by using the dependencies dictionary: dependencies[C] = set(D).
    - For D, delete C from its prerequisites in the prerequisites dictionary: prerequisites[D].delete(C).
    - prerequisites[D] is now empty, so add D to the queue.
    - Since C is printed, delete it from dependencies.
    - Summary: prerequisites = {}; dependencies = {}; queue = (D); taken = (A, B, C); A, B, C have been printed in that order
7. Next in the queue is D, so let's process it:
    - Print D and add to taken.
    - D does not exist in dependencies dictionary, do nothing.
    - Summary: prerequisites = {}; dependencies = {}; queue = (); taken = (A, B, C, D); A, B, C, D have been printed in that order

Runtime Analysis
==========
Each record in the file will get processed once, incurring O(n).
The program guarantees to check each record again a maximum of one time from the queue (courses without prerequisites won't get enqueued, and courses get enqueued only when its last unprinted prerequisite gets printed, which can only happen once). This would incur O(n).
So, overall runtime is O(n), where n is the number of unique classes in the provided file.
