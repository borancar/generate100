# Generate 100 files

## Task

* Each file should contain a line with between 1 and 65 randomly chosen
  printable characters (both the number of the characters and the characters
  themselves are random)
* Line "This is every 5th file!" should appear in every 5th file
* Every 7th file ignores the previous two rules and contains the concatencated
  contents of all of the previous files.
* Write test-suite for your implementation.

## Solution

Implement the 3 cases using 3 separate methods, mod7\_file, mod5\_file and
random\_file. These methods only return the content to allow easier testing.
The decision which method should be run is done by evaluate\_rules which also
only returns the content for easier testing. Finally, unify the writing to the
file in the main method.

## Testing

evaluate\_rules is tested by using Python3's unittest.mock which allows
patching of methods and classes so we can check what was actually called and
how many times. As for mod7\_file which reads files, the method was modified
to take in a open\_fn method so we can provide a custom mock that checks which
file was opened, how was it read and stub the results.
