#import sys
#sys.path.insert(0,'./Parse')
import parse_scode
import gameclasses

def Buff_Index(retId_0,buff_array):
	#returns the index of the buff_array spell that we want the variable to return to
	for x in range(0,len(buff_array)):
		if buff_array[x].callerId == retId_0:
			return x
	#returns -1 on error
	return -1

def Run_Code(player_array,hit_arr,proj_arr):
	#loop over each of the games players
	for x in range(0,len(player_array)):
		#loop over each of the games spells
		offset = 0
                print('[Run_Code] player_index:' + str(x))

		for i in range(0,len(player_array[x].spells)):
			#store the ip of the spell so that we can reset it if the function makes a call
			buff_ip = player_array[x].spells[i+offset].ip

			print('[Run_Code] RUNING ' + str(player_array[x].spells[i+offset].code))
			print('[Run_Code] call_index:' + str(player_array[x].spells[i+offset].call_index))
			#run the spell and store wether or not the function decided to finish
			print('[Run_Code] proj_arr ' + str(proj_arr))
                        end_result = player_array[x].spells[i+offset].run(player_array[x],hit_arr,proj_arr)
			print('[Run_Code] finished?:' + str(end_result[0]))
                        print('[Run_Code] result:' + str(end_result[1]))
			#need to execute the check for if the call function returned only once
			#becuse of it iterating over the variables and as a result executing yet another
			#loop within the loop itereations so we want to minimise the # of times it gets
			#executed

			#they want to call somthing so ignore any resolution attempts
			retTest = player_array[x].spells[i+offset].CheckFinish()
			print('[RunCode] CheckFinish returned ' + str(retTest))
			print('[RunCode] it was given these as input ' + str(player_array[x].spells[i+offset].ret_vars))
			#we need to fix the appending n problem to fix the misinterpretation on this end
			if player_array[x].spells[i+offset].callFlag != 0 and retTest == False: #player_array[x].spells[i+offset].CheckFinish():
				print('[RunCode call] WE WANT TO CALL!!!!!')
				#set the caller id to the same uniq Id that the parsing function did
				player_array[x].spells[i+offset].callerId = player_array[x].gen_uniqId()
				#reset the instruction pointer of the spell
				player_array[x].spells[i+offset].ip = buff_ip
				#reset the call_index of the spell
				player_array[x].spells[i+offset].call_index = 0
				print('[Run_Code call] call_index spell array:' + str(player_array[x].spells[i+offset].call_index))
				#copy the spell into the buff array
				player_array[x].buff_spells.append(player_array[x].spells[i+offset])
				print('[Run_Code call] call_index buff spells array:' + str(player_array[x].buff_spells[len(player_array[x].buff_spells) - 1].call_index))
				#remove it from execution
				del player_array[x].spells[i+offset]
				offset -= 1
			else:
				if end_result[0] == True:
					print('[Run_Code] END!')
					#the spell that we just ran finished
					if player_array[x].spells[i+offset].retId != -1:
						print('[Run_Code] WE WANNA RETURN!')
						#the spell wants to return a value to an index
						#get the index of the buff_array spell that it wants to return to
						Index = Buff_Index(player_array[x].spells[i+offset].retId[0],player_array[x].buff_spells)
						#store the parsed return value into the return array of that spell
						player_array[x].buff_spells[Index].ret_vars[player_array[x].spells[i+offset].retId[1]] = end_result[1]
						#decriment the callFlag of the function we returned to
						player_array[x].buff_spells[Index].callFlag -= 1
						#move the waiting spell back onto the main execution stack and delete from the wait q if its callFlag says its not waiting for anymore spell calls to complete
						if player_array[x].buff_spells[Index].callFlag == 0:
							player_array[x].spells.append(player_array[x].buff_spells[Index])
							del player_array[x].buff_spells[Index]

                                        print('[RunCode] Deleting!')
					#delete the spell that finished executing from the main spell q and decriment the offset
                                        print('[RunCode] len:' + str(len(player_array[x].spells)))
                                        print('[RunCode] id to delete:' + str(player_array[x].spells[i+offset].code))
                                        del player_array[x].spells[i+offset]
                                        print('[RunCode] len:' + str(len(player_array[x].spells)))
                               		offset -= 1
def Run_Test(i):
	player_array = [ gameclasses.player('p0',100,100,1,[],[0,0]),
	gameclasses.player('p1',100,100,1,[],[0,0]),
	gameclasses.player('p2',100,100,1,[],[0,0]),
	gameclasses.player('p3',100,100,1,[],[0,0]),
	gameclasses.player('p4',100,100,1,[],[0,0]),
	]

	player_array[0].spells = [gameclasses.spell(5,player_array[4])]
	#player_array[1].spells = [gameclasses.spell(0,player_array[2]),gameclasses.spell(3,player_array[1])]
	for w in range(0,i):
		Run_Code(player_array)
		#print('[*] player 0 buff array:' + str(len(player_array[0].buff_spells)))
		#print('[*] p0.buffspells[0].callerval: ' +str(player_array[0].buff_spells[0].callerId))
		print('[*] p0 buff_spells len:' + str(len(player_array[0].buff_spells)))
		for x in range(0,len(player_array[0].buff_spells)):
			print('[*]	p0 buff_spells:' + player_array[0].buff_spells[x].ToString())
		print('[*] p0 spell array:' + str(len(player_array[0].spells)))
		for x in range(0,len(player_array[0].spells)):
                        print('[*]      p0 spells:' + player_array[0].spells[x].ToString())
		player_array[0].output2screen()
		player_array[4].output2screen()
