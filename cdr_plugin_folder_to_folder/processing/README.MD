## The Processing Module

### Overview

Processing does the following:

- Iterates through the HASH folders created during pre-processing on HD2
- For each HASH folder:
    - If the status in metadata is not "INITIAL" does nothing
    - Otherwise:
        - Updates the status in metadata to "IN PROGRESS"
        - Sends the file to be processed
        - Saves the processed file to the corresponding directory in HD3
        - Saves the processing report to the HASH folder
        - Updates the status to "COMPLETED"

### The Loops Class

`LoopHashDirectories` function iterates through HASH directories of HD2
For each of the directories, it initiated file processing with a call to `processDirectory` of the `File_Processing` class

### The File_Processing class

The class functionality is accessed with the `processDirectory` function.
The function gets a HASH directory path on HD2 as a parameter and processes it