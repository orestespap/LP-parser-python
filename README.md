Initially, the parser breaks down the input file into two chunks; the first line, which is supposed to contain the objective function,
and the rest of the lines minus the last one, which contain the technological and natural constrains respectively.

All the lines (m count) are now stored into a 1xm array. Each line (item in list) then undergoes a whitespace character cleaning process,
in which whitespace and \t characters are being removed.

To ensure the validity of the objective function's format, the parser splits the text line on spaces, and does the following:
	
	- Checks that the first element is either min or max
	
	- Then checks the second element of the array. If it is an operand (+ or -), it assumes that all operators are located in the
	odd positions of the array, while the operands are located in the even positions of the array (and vice versa).
	
	- Then it checks if the operators are located in the right positions, and then moves on to checking the operands' positions.
	When it comes to the latter, along with position checking, the parser also validates their format by using regular expressions.
	
	- Once the above have been validated, it moves on to the creation of the C table. It then creates two sub-tables, one contains the
	operands and the other contains the operators. 

	-It then checks the size of the two arrays; if it isn't even, it assumes that x1's operator is + (the user didn't type it), 
	zips the two arrays and converts the string items into floats.

The parsing process for the constrains is almost identical. The only noteworthy difference is the addition of 0 values in the operands
table for the variables that have a 0 weight in a given constrain.

For any further questions or suggestions don't hesitate to email me at orestespap@gmail.com.
