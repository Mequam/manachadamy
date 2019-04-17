import gameclasses
import math
#the only thing that we changed is the decriment of the ord function inside of the findArgs function if there are errors a
#dd that -1 back in after the ord

def printSpellCode(SpellCode,silent = True):
    import sys
    #this is a simple debuging function to output spellcode
    ret_val = []
#    #print('LENGTH OF SPELLCODE ' + str(len(SpellCode))) 
    for x in range(0,len(SpellCode)):
        ret_val.append(hex(ord(SpellCode[x])))
        if silent == False:
            sys.stdout.write('\\' + hex(ord(SpellCode[x])))
    if silent == False:
        sys.stdout.write('\n')
    return ret_val
def argVal(func,ctrl_flow=False):
	# this function returns the number of delimiters that we need to search for
	# in a given function
	if ctrl_flow == False:
		#not in control flow
		if func == '\x05':
			return 1
		if func == '\x06':
			return 1
		if func == '\x07':
			return 1
		if func == '\x08':
			return 1
		if func == '\x09':
			return 1
		if func == '\x0A':
			return 1
		if func == '\x0B':
			return 1
		if func == '\x0C':
			return 1
		if func == '\x0D':
			return 1
		if func == '\x12':
			return 1
		if func == '\x14':
			return 1
		if func == '\x15':
			return 1
                if func == '\x1A':
                        return 1
                if func == '\x1B':
                        return 1
                if func == '\x1C':
                        return 1
                if func == '\x1D':
                        return 5
		else:
			return -1
	else:
	#jump to control flow and dont bother checking the other calculations
		if func == '\x10':
			return 2
		if func == '\x13':
			return 2
		else:
			return -1
def findArgs(SpellCode,ctrl_flow=False):
	#the delimit argument is a bool to protect the inner function and make sure 
	#that it only gets the arguments that we expect
	#the outer argument is named control flow to indicate what it is suposed to be inputed
	#print('[findArgs] initial SpellCode len:' + str(len(SpellCode)))
	delimit = '\x01'
	if ctrl_flow == True:
		delimit = '\x00'
	#this is a function for finding the delimiters between variables

	#Solved is the number of delimiters that we need to search for until we reach the end of our function
	#we need to make a special case for byte code \x18 becuse it has variableised functions that need to be determined 
	#ourselfs
	Solved = 0
	i = 1
	if SpellCode[0] != '\x18':
		#non special case
		Solved = argVal(SpellCode[0],ctrl_flow)
	else:
		#variable variable numbers
		Solved = ord(SpellCode[2])
		i = 3

	#ignor is the var that we use to determin wether or not a delimiter is in our function or a nested function 
	#(it basicaly tells the program to ignor inside of parenthasys)
	ignor = 0
	#we store the argvalue in here so that we dont have to compute it twice for each function
	argVal_buff = 0
	#the index that we are currently on
	# this is the return value that the function will return to its caller function
	RetVal = []

	while Solved != 0:
		#print('[findArgs] ' + str(printSpellCode((SpellCode[i:len(SpellCode)]))))
		argVal_buff = 0
		if SpellCode[i] != '\x18':
			#non special case
			argVal_buff = argVal(SpellCode[i],ctrl_flow)
		else:
                        #variableised functions
			argVal_buff = ord(SpellCode[i + 2])

		#this code knows which values are non functions becuse those return -1 from the argVal func
		if argVal_buff == -1:
			# we did not find a function
			if SpellCode[i] != '\x00' and SpellCode[i] != '\x01':
				#we found a constant
				#increment i by 2 to skip the next value
				i += 2
			else:
				#we have found a delimiter
				if SpellCode[i] == delimit:
					if ignor <= 0:
						#not supposed to be ignored
						RetVal.append(i)
						Solved -= 1
					else:
						#supposed to be ignored
						ignor -= 1
					#continue to the next value
					i += 1
				else:
					#it is the alternet delimiter so we can ignore it
					i += 1
			#we found a function
		else:
			#we found another command that has an amount of variables to be passed
			#incriment for the delimiters
			ignor += argVal_buff
			#increment for the actual function bytecode
			if SpellCode[i] != '\x18':
				i += 1
			else:
				i += 3
	return RetVal
def parse_list(SpellCode,caster,castee,spell,Delimiters,From_Call=False,offset = -3):
	#parses a series of deliminated spellcode and returns the result in an array
	#this is used in the calling function to know if any of the bellow functions are going to call somthing else
	ret_array = []
	ret_array.append(parse(SpellCode[0:Delimiters[0]+offset],caster,castee,spell))
        for x in range(0,len(Delimiters) - 1):
		#print('[parse_list] loop:' + str(printSpellCode(SpellCode[Delimiters[x] + 1 + offset: Delimiters[x + 1] + offset])))
		ret_array.append(parse(SpellCode[Delimiters[x] + 1 + offset: Delimiters[x + 1] + offset],caster,castee,spell,From_Call))
	##print('[parse_list] end:' + str(SpellCode[Delimiters[-1] + offset + 1:len(SpellCode)]))
	#ret_array.append(parse(SpellCode[Delimiters[-1] + offset + 1 : len(SpellCode)],caster,castee,spell,From_Call))
	return ret_array

def parse(SpellCode,caster,castee,spell,From_Call=False,h_r=None,p_r=None):
	#the function that takes spell code and recursivly determins what functions to run on game objects
	delim = []
	if SpellCode[0] == '\x00':
		#add to the pheudo instruction pointer becuse we found a hanging if statement delimiter
		spell.ip += 1

	if SpellCode[0] == '\x02':
		spell.ip += 2
		#return a boolean constant
		if SpellCode[1] == '\x01':
			##print('[parse] True! spell.ip:' + str(caster.args))
			return True
		else:
			##print('[parse] False! spell.ip:' + str(caster.args))
			return False
	if SpellCode[0] == '\x03':
		spell.ip += 2
		#return an intager constant
		return ord(SpellCode[1])
	if SpellCode[0] == '\x04':
		spell.ip += 2
		#return a specified argument
		num = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
		##print('[04] getting spell.args[' + str(int) + ']')
		return spell.args[num]
	if SpellCode[0] == '\x05':
		#add x+y
		spell.ip += 2
		delim = findArgs(SpellCode)
		num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                #if num1 != 'N' and num2 != 'N':
                if spell.callFlag == 0:
                    return num1 + num2
                else:
                    return 'N'
	if SpellCode[0] == '\x06':
		#sub x-y
		spell.ip += 2
		delim = findArgs(SpellCode)
		num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 - num2
                else:
                    return 'N'
	if SpellCode[0] == '\x07':
		#multiply x*y
		spell.ip += 2
		delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 * num2
                else:
                    return 'N'
	if SpellCode[0] == '\x08':
		#divide x/y
		spell.ip += 2
		delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1/num2
                else:
                    return 'N'
	if SpellCode[0] == '\x09':
		#ret x > y
		spell.ip += 2
		delim = findArgs(SpellCode)
		num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 > num2
                else:
                    return 'N'
	if SpellCode[0] == '\x0A':
		#ret x < y
		spell.ip += 2
		delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 < num2
	if SpellCode[0] == '\x0B':
		#ret x == y
		spell.ip += 2
                delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1==num2
                else:
                    return 'N'
	if SpellCode[0] == '\x0C':
		#ret x && y
		spell.ip += 2
                delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 and num2
                else:
                    return 'N'
	if SpellCode[0] == '\x0D':
		#ret x || y
		spell.ip += 2
                delim = findArgs(SpellCode)
                num1 = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num2 = parse(SpellCode[delim[0]+1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                    return num1 or num2
                else:
                    return 'N'
	if SpellCode[0] == '\x0E':
		#create an int var
		#need to abuse this setting as a possible security leak
		spell.ip += 1
		intVal = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
		if spell.callFlag == 0:
		        spell.args.append(intVal)
		        return intVal
                else:
                        return 'N'
	if SpellCode[0] == '\x0F':
	        #Create a bool var
		spell.ip += 1
		boolVal = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
		if spell.callFlag == 0:
		        spell.args.append(boolVal)
		        return boolVal
                else:
                        return 'N'
	if SpellCode[0] == '\x12':
		#update an existing variable
		spell.ip += 2
		delim = findArgs(SpellCode)
		value = parse(SpellCode[(delim[0] + 1):len(SpellCode)],caster,castee,spell,From_Call)
		index = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
		if spell.callFlag == 0:
		        spell.args[index] = value
		        return value
                else:
                        return 'N'
	if SpellCode[0] == '\x10':
		#the if statement bytecode
		#now when this statement is true it leaves a hanging \x00 to be ignored in the future that is not accounted for,
		#by the ip, possibly going to need to fix this in the future

		
                #this is currently handled in the bytecode '\x00' as the first command for the parser		
                delim=findArgs(SpellCode,True)

                condition = parse(SpellCode[1:(delim[0])],caster,castee,spell,From_Call)
                
                if spell.callFlag != 0:
                    #break out of execution if we are waiting for a call to return
                    return 'N'

                if condition:
		    	#the if statement was true, so do not change execution flow, this leaves the hanging '\x00'
		    	spell.ip += 2
		else:
			#the if statement is false, jump to the next instructions
			spell.ip += delim[1] - delim[0] + 2

	if SpellCode[0] == '\x13':
		#this is effectivly a jump statement set the ip to a given index
		jump_ip = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        spell.ip = jump_ip
                else:
                        return 'N'
	if SpellCode[0] == '\x14':
		#while a player has not been hit the castee symbol will be the same as the caster symbol, so be careful!
		#set castee stat
		#set a given player stat to a given value and remove the apropriate mana
		spell.ip += 2
		delim = findArgs(SpellCode)
		stat = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
		num = parse(SpellCode[delim[0] + 1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        #sets the stat of the given player and outputs the stat to all of the clients
			gameclasses.setStat_net(caster,castee,stat,num)
		        return gameclasses.getStat(castee,stat)
                return 'N'
	if SpellCode[0] == '\x15':
		#set caster stat
		spell.ip += 2
                delim = findArgs(SpellCode)
		stat = parse(SpellCode[1:delim[0]],caster,castee,spell,From_Call)
                num = parse(SpellCode[delim[0] + 1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        #sets the stat of a given player and outputs the change to all of the clients
			gameclasses.setStat_net(caster,caster,stat,num)
		        return gameclasses.getStat(caster,stat)
                return 'N'
	if SpellCode[0] == '\x16':
                #get castee stat
                spell.ip += 1
                stat = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        return gameclasses.getStat(castee,stat)
                return 'N'
	if SpellCode[0] == '\x17':
                #get caster stat
                spell.ip += 1
                stat = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        return gameclasses.getStat(caster,stat)
                return 'N'
	if SpellCode[0] == '\x18':
		#print('[call] made it to the call statement')
		i = spell.call_index
		spell.call_index += 1
		#print('[call] i:' + str(i))
		delims = findArgs(SpellCode)
		if len(spell.ret_vars) - 1 < i:
			#print('[call] appending N')
			spell.ret_vars.append('N')

		#even if the n is appended it shouldnt match i here
		if spell.ret_vars[i] == 'N':
			push = True
			checkList = parse_list(SpellCode[3:len(SpellCode)],caster,castee,spell,delims,True)
			
                        #checkList = parse_list(SpellCode[3:len(SpellCode,caster,castee,spell,delims,True)
			#callcommand\spellId\varNum\[deliminatedvars]
			for x in range(0,len(checkList)):
				if checkList[x] == 'N':
					push = False
					break
			if push == True:
				#print('[call] push2q')
				#print('[call] recived ' + str(checkList) + ' as args' )
				caster.spells.append(gameclasses.spell(ord(SpellCode[1]),castee,checkList,-1,[caster.gen_uniqId(),i]))
				spell.callFlag += 1
				return 'N'
			else:
				return 'N'
		else:

			#need to modify the ip so that it points twords the next instruction
			if From_Call == False:
				spell.ip += delims[-1] + 1
			return spell.ret_vars[i]
	if SpellCode[0] == '\x19':
		#makes the ip point to the end of the program so that the main caller knows when to stop execution
		retVal = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
		spell.ip += len(SpellCode)
                return retVal
        if SpellCode[0] == '\x1A':
                #cos x
                spell.ip += 1
                retval = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        return math.cos(float(retval))
                else:
                        return 'N'
        if SpellCode[0] == '\x1B':
                #sin x
                spell.ip += 1
                retval = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                if spell.callFlag == 0:
                        return math.sin(float(retval))
                else:
                        return 'N'
        if SpellCode[0] == '\x1C':
                #tan x
                spell.ip += 1
                retval = parse(SpellCode[1:len(SpellCode)],caster,castee,spell,From_Call)
                #need to clean this code and make this into a safe return function
                #somthing for the future
                if spell.callFlag == 0:
                        return math.tan(float(retval))
                else:
                        return 'N'
        if SpellCode[0] == '\x1D':
                #create a projectile
                spell.ip += 4
                #this is the ONLY function that will use h_r and is ONLY to be called directly from 
                #the only time this should happens is when this function is called directly from RunCode
                #should, this is risky to run
                if len(h_r) != None:
                        #need to figure out a way to get this appended to the proj loop
                        #(self,plr,life=100,speed=.25,para=[0,0],OnDeath=-1,OnBirth=-1,HitBox=[-1,0],HitBoxArr=[],Id=0)
		        print('[parse] CREATING PROJ')
                        delims = findArgs(SpellCode)
                        life = parse(SpellCode[1:delims[0]],caster,castee,spell,From_Call)  
                        speed = float(parse(SpellCode[delims[0] + 1:delims[1]],caster,castee,spell,From_Call))/100
                        p1 = parse(SpellCode[delims[1] + 1:delims[2]],caster,castee,spell,From_Call)
                        p2 = parse(SpellCode[delims[2] + 1:delims[3]],caster,castee,spell,From_Call)
                        Od = parse(SpellCode[delims[3] + 1:delims[4]],caster,castee,spell,From_Call)
                        Ob = parse(SpellCode[delims[4] + 1:len(SpellCode)],caster,castee,spell,From_Call)
                        #it will be interesting to see the effect of setting the castee to the target instead of the caster
                        #it is possible that this will need to be changed in the future
                        L = len(p_r)
                        p_r.append(gameclasses.proj(spell.castee,life,speed,[p1,p2],Od,Ob,[2,2],h_r,L)) 
                        caster.bridge.Broadcast('AP ' + str(caster.pos[0]) + ' ' + str(caster.pos[1]))
#testCode = ['\x18','\x02','\x02','\x03','\x00','\x01','\x03','\x10','\x01']
#testCode = ['\x05','\x03','\x03','\x01','\x03','\x03']
#testCode = ['\x03','\x00']
##print(findArgs(testCode))
#print(len(Player_Array))
