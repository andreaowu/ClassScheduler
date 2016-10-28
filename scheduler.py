import json
import os
import Queue
import sys

def data_from_file(fname):
    '''Checks existence of given filename and returns data from it.

    Input:
    - fname: file that holds data to be processed

    Output:
    - None if fname is not an existing file, data in given file otherwise
    '''

    # Check for path validity
    if not os.path.isfile(fname):
        print "Error: " + fname + " is not a valid existing file."
        return None

    # Grab the data
    with open(fname) as data_file:
        data = json.load(data_file)
    return data

def aggregate_dependencies(new_dependencies, existing_dependencies):
    '''Merges new_dependencies with old dependencies.

    Since values in dependencies dictionary is a set, this function merges
    the two sets if the dependency exists in both dictionaries. Otherwise,
    all the new dependencies are copied over into the existing dependencies
    dictionary.

    Input:
    - new_dependencies: new dictionary with string of course name as key, 
      set of courses that depend on key's course (ie the key's course is a 
      prerequisite of each course in the set) as value to be merged
      with existing dependencies
    - existing_dependencies: existing dependencies dictionary with string of 
      course name as key, set of courses that depend on key's course as value

    Output:
    - dependencies: merged dictionary of new_dependencies and 
      existing_dependencies with string of course name as key, set of courses
      that depend on key's course as value
    '''
    for d in new_dependencies:
        if d in existing_dependencies:
            # Dependencies for given course already exists, merge sets
            existing_dependencies[d] = existing_dependencies[d] | temp[d]
        else:
            # Dependency for given course does not exist yet, make a new entry
            existing_dependencies[d] = set()
            existing_dependencies[d].add(new_dependencies[d])
    return existing_dependencies

def process_dependencies(dependencies, prereqs, queue, course, taken):
    ''' 
    Deletes given course from courses that have it as its prerequisite. Adds
    course to queue if there are no more unprinted prerequisites for that
    course (ie the set of courses that have the given course as its 
    prerequisite is empty).
    
    Input:
    - dependencies: dependencies dictionary with string of course name as key, 
      set of courses that depend on key's course as value
    - prereqs: prerequisites dictionary with string of course name as key, set
      of courses that are prerequisites to key's course as value
    - queue: queue of courses that have not been printed yet
    - course: string of course name that has just been printed, so need to
      update all courses that have it as a prerequisite
    - taken: set of courses that have been printed

    Output:
    - dependencies: updated dependencies dictionary
    - prereqs: updated prerequisites dictionary
    - queue: updated queue of courses to be printed
    '''
    if course in dependencies:
        # Loop through all courses that have given course as a prerequisite
        for d in dependencies[course]:
            # d no longer needs to wait for course to get printed before d can
            # get printed
            prereqs[d].remove(course)

            if len(prereqs[d]) == 0:
                # course was d's last prerequisite that had to be printed, and d
                # no longer depends on any prerequisites that have not been printed
                del prereqs[d]

                if d not in taken:
                    # d is ready to get printed, if statement prevents
                    # courses without prerequisites to get added to the queue
                    queue.put(d)
        del dependencies[course]
    return dependencies, prereqs, queue

def process_data(data):
    ''' Processes the data and prints out courses in correct order.

    Reads through given data once, printing out all courses that can be printed
    out at the time (ie courses without prerequisites and courses with 
    prerequisites that have already been printed). As more courses get printed, 
    courses that cannot get printed yet get added to the queue. Each course only 
    gets added to the queue at most once. Queue gets processed and courses get 
    printed.

    Input:
    - data: data with course names and corresponding prerequisites

    Output:
    - No return object(s), but prints out course names or error if courses
      have circular dependency.
    '''
    # Initialize all data structures
    taken = set() # courses that have been printed out already
    queue = Queue.Queue() # courses that have yet to be printed out
    prereqs = {} # key: course, value: set of courses that are prerequisites to key
    dependencies = {} # key: course, value: set of courses that depend on key

    # Loop through all courses in data
    for course in data:
        name = course['name']
        prerequisites = course['prerequisites']
        allTaken = True # whether all prerequisites have been printed out already
        new_dependencies = {} # temporary storage of dependencies
        new_prereqs = set() # temporary storage of course's unprinted prerequisites
        # Loop through all prerequisites
        for prereq in prerequisites:
            if prereq not in taken:
                # Found a prereq that hasn't been printed yet
                allTaken = False
                # Course depends on prereq, ie prereq is a prerequisite to course
                new_dependencies[prereq] = name
                new_prereqs.add(prereq)

        if allTaken:
            # All prerequisites for this course have already been printed, so
            # print this course and delete it from all courses that depend
            # on it
            print name
            dependencies, prereqs, queue = process_dependencies(dependencies, 
                                           prereqs, queue, name, taken)
            taken.add(name)
        else:
            # Not all prerequisites for this course have been printed yet, so
            # merge temp with existing dependencies
            prereqs[name] = new_prereqs
            dependencies = aggregate_dependencies(new_dependencies, dependencies)

    # Go through the queue to process courses
    while not queue.empty():
        course = queue.get()
        print course
        taken.add(course)
        dependencies, prereqs, queue = process_dependencies(dependencies, 
                                       prereqs, queue, course, taken)

    # All dependencies and prereqs should be removed. If not, there is a
    # circular dependency!
    if len(dependencies) != 0 or len(prereqs) != 0:
        print "Error: Impossible outcome, there are circular dependencies."

def main():
    # Checks that a file was passed as command-line argument
    if len(sys.argv) < 1:
        print "Error: Need a filename to be passed in."
        return

    fname = sys.argv[1]
    # Get data from file
    data = data_from_file(fname)    
    if data is None:
        return
    # Print out courses in correct ordering
    process_data(data)

if __name__ == "__main__":
    main()
