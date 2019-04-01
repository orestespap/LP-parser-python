from open_write_files import list_lines_txt,write_to_text_file
import re

def objective_function_check(firstline):
	minmaxmap={'min':-1,'max':1}
	
	bits=list(map(lambda abit: abit.lower(),filter(None,firstline.replace('\t','').split(' ')))) #first removse empty characters from list, then lowercase everything
	
	if bits[0] in ('min','max'):
		c_table=check_xs(bits[1::],check_plus_minus(bits[1:]),'o')
		return c_table,minmaxmap[bits[0]]		

	else:
		raise TypeError('Missing min or max tag before objective function in line 1')
		

def check_plus_minus(bits):
	if bits[0] in ('-','+'):
		for abit in bits[0::2]:
			if abit not in ('+','-'):
				raise TypeError('Missing +/- symbol or you didn\'t leave a space between operands and variable')
		return 1 #check even
	else:
		for abit in bits[1::2]:
			if abit not in ('-','+'):
				raise TypeError('Missing +/- symbol or you didn\'t leave a space between operands and variable')
		return 0 #check odd

def check_xs(bits,flag,key,var_count=None):
	wheretostartfrom,prev={1:1,0:0},0
	
	start=wheretostartfrom[flag]
	

	for abit in bits[start::2]:
		pattern=re.compile(r'^(\d+(\.\d+)?)?x\d+$')
		check=pattern.search(abit)
		
		if not check:
			raise TypeError(f'Objective function variables must be of format: INTEGERXi\ni.e. 5x1, 2.5x1\nYours were: {abit}')

		xi=abit.split('x')[-1]
		
		if key=='o':
			if int(xi)!=prev+1:
				raise TypeError(f'Objective function variable identifiers (i) must follow a specific order: i= (1,2,3,...n)\nCorrect input: x{prev+1}\nYour input: x{xi}')
			
			prev+=1
		else:
			if int(xi)<=prev or int(xi)>var_count:
				raise TypeError(f'Constrain\'s variable identifiers (i) must follow a specific order: i= (1,2,3,...n) and belong to the range of 1 to {var_count}\nCorrect input: x{prev+1}\nYour input: x{xi}')
			prev=int(xi)

	return table(bits,flag,key,var_count)

def table(bits,flag,key,var_count=None):
	wheretostartfrom={1:1,0:0}
	
	xs_pos=wheretostartfrom[flag]
	
	if flag:
		operands_pos=wheretostartfrom[0]
	else:
		operands_pos=wheretostartfrom[1]
	
	weights,operands=[abit.split('x')[0] if abit.split('x')[0]!='' else '1' for abit in bits[xs_pos::2]],[abit for abit in bits[operands_pos::2]]
			
	if len(weights)!=len(operands):
		operands.insert(0,'+') #if lists' sizes not equal, it means that the first variable's operand is + and the user did not type it

	table=list(float(atuple[0]+atuple[1]) for atuple in zip(operands,weights))
	
	if key=='c':
		#add 0 for vars with weight 0

		varsin=[int(abit.split('x')[-1]) for abit in bits[xs_pos::2]] #variables without 0 weight in constrains inequalities
		varsmissing=[i for i in range(1,var_count+1) if i not in varsin] #variables with 0 weight
		for i in varsmissing:
			table.insert(i-1,0)
	
	return table


def constrains_check(lines,var_count):
	eqin,a_table,b_table=[],[],[]
	
	for index,aline in enumerate(lines):

		bits=list(map(lambda abit: abit.lower(),filter(None,aline.replace('\t','').split(' ')))) #removes potential \t characters, splits text line on spaces and lowercases all chars
		
		if index==0:
			st_check(bits[0])
			bits.pop(0) #removes 'subject to' tag
		
		eqin.append(ineq_operand_check(bits[-2]))
		b_table.append(get_right_side_of_ineq(bits[-1]))
		a_table.append(check_xs(bits[:-2],check_plus_minus(bits[:-2]),'c',var_count))

	return a_table,b_table,eqin
	

def ineq_operand_check(abit):
	eqdict={'<=':-1,'>=':1,'=':0}

	if eqdict.get(abit) or abit=='=': #for some reason get(key) doesn't recognize = as a key of the dictionary
		return eqdict[abit]
	
	raise TypeError(f'Second to last character in constrains must be one of the following: >, >=, <, <=, =\nYour input was: {abit}')

def get_right_side_of_ineq(abit):
	if re.match(r'^\d+(\.\d+)?$', abit):
		return float(abit)

	raise ValueError(f'Right side of inequality must contain numbers and be great than zero.\ni.e. 2, 2.5\nYour input was {abit}')


def st_check(abit):
	if abit not in ('s.t.', 'st', 'subject'):
		raise TypeError(f'Subject to tag missing or misspelled in first constrain.\nAvailable options: s.t., st, subject\nYour input was {abit}')
			
	
def remove_junk_chars(lp1):
	#removes empty lines, lines containining \t character, and lines containing just whitespace characters
	return list(filter(lambda x: x!='',filter(lambda x: x!='\t',filter(lambda x: not re.match(r'^\s*$', x), lp1)))) 

lp1=remove_junk_chars(list_lines_txt('lp1.txt'))
c,MinMax=objective_function_check(lp1[0])
a,b,eqin=constrains_check(lp1[1:len(lp1)-1],len(c))
write_to_text_file('outputfile.txt',f"Min or Max:\n{MinMax}\nC Table:\n{c}\nA table:\n{a}\nInequalities operands (eqin table):\n{eqin}\nB table:\n{b}")