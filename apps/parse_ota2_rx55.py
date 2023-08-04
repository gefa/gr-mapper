#!/usr/bin/env python
import sys
def parse_line(line):
    # Remove any leading/trailing whitespaces and split the line by spaces
    parts = line.strip().split()
#    print(parts)
    # Check if the line is of the desired format
    if len(parts) == 6 and parts[0] == "('GRAND": #and parts[2] == "[" and parts[5] == "])":
        # Extract the 4-element array and convert it to a list of integers
        #array = [int(x) for x in parts[3][1:-1].split(',')]
        grand0 = parts[2][1:-1]#.split(',')
        grand1 = parts[3][:-1]#.split(',')
        grand2 = parts[4][:-1]#.split(',')
        grand3 = parts[5][:-2]#.split(',')
        grands = [grand0,grand1,grand2,grand3]
        #print(grands)
        array = [int(x) for x in grands]
        return array
    else:
        return None

def main(file_path):
    total_array = [0, 0, 0, 0]

    try:
        with open(file_path, 'r') as file:
            for line in file:
                array = parse_line(line)
                if array:
                    #print(array)
                    # Add the array to the total_array
                    total_array = [sum(x) for x in zip(total_array, array)]
    except FileNotFoundError:
        print("File not found.")
        return

    print("Total array:", total_array)

if __name__ == "__main__":
    file_path = sys.argv[1] #"your_file.txt"  # Replace this with the path to your file
    main(file_path)
exit()
import re

def main(file_path):
    total_array = [0, 0, 0, 0]

    try:
        with open(file_path, 'r') as file:
            for line in file:
             try:
              if line.strip().split()[0]=="('GRAND":
                # Use regular expression to find lines with the desired format, \('GRAND',
                match = re.match(r" \[(\d+), (\d+), (\d+), (\d+)\]\)", line.strip().split()[1:])
                if match:
                    print(match)
                    # Extract the numbers from the regular expression match
                    array = [int(match.group(i)) for i in range(1, 5)]

                    # Add the array to the total_array
                    total_array = [sum(x) for x in zip(total_array, array)]
             except IndexError:
              pass
    except FileNotFoundError:
        print("File not found.")
        return

    print("Total array:", total_array)

if __name__ == "__main__":
    file_path = sys.argv[1]#"your_file.txt"  # Replace this with the path to your file
    main(file_path)

exit()
