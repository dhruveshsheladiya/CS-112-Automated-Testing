#!/bin/bash

# fetch all the files from the folder and save in a variable
yourfilenames=`ls $2/`
#to keep track of number of files tested
count=1

#loop to go through each file
for eachfile in $yourfilenames
do
#creating filepath
newfile="$2/$eachfile"
#printing on your terminal
#helps you remove a file which causes problem
echo $newfile
#echos on a newfile.txt count and name of file being tested
echo "$count)$newfile" >> $3
#increase count
count=$(($count + 1))
#Testing the file
python3 $1 $newfile >> $3

 

#windows user

#py $1 $newfile >> $3


# separator
echo "-----------------------------------------------------------------------------------" >> $3

done
# end of script
