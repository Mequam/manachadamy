import math
import parse_scode
def get_scode(filename,offset=0):
        #a simple function that returns the spell code from a file at a given offset

        #we have to read in all of the bytecode into memory becuse we do not know when the function will stop as
        #most functions have no ending delimiters, in the future if player spellcode proves to be to large for memory
        #we might want to concider adding them, but for the time bieng this function should suffice
        file_info = []
	with open(filename,'rb') as f:
		f.seek(offset)
                file_info.append(f.read())
		#print('[get_scode] file_info[0]:' + str(file_info[0]))
		f.seek(0,2)
		file_info.append(f.tell())
        return file_info

class GameObject:
	pos = [0,0]
	angle = 0
        #the graphics that the clients need to draw perhaps dont hold this in server memory for very long as we dont realy
        #need it in order to run the server
	t_array = []
	def __init__(self,pos,angle,t_array):
		#set up the variables in the class
		self.pos = pos
		self.angle = angle
		self.t_array = t_array
class Tile:
	posR = [0,0]
	color = '#000000'
	def __init__(self,posR,color):
		self.posR = posR
		self.color = color
class proj(GameObject):
        #a pointer to the player who owns the projectile
	plr = ''
        #the index of the array where the projectile is stored
        Id = 0
        life = 100 
        #the percentage that it jumps to the new position
        speed = .25 
        #the number of "tics" that the proj will stay alive

        #these are the spell id's of the projectiles events and are to be placed on the 
        #spell q by the hitbox check of the main loop when each event happens
        #-1 means that we dont want to call any of the events
        para = [0,0]
        OnDeath = -1
        OnBirth = -1
        def __init__ (self,plr,life=100,speed=.25,para=[0,0],OnDeath=-1,OnBirth=-1,HitBox=[-1,0],HitBoxArr=[],Id=0):
                self.plr = plr
                self.life = life
                self.OnDeath = OnDeath
                self.OnBirth = OnBirth
                #attach a hitbox to the game object if one is specified
                self.para = para
                self.Id=Id
                self.pos = plr.pos
                if HitBox[0] >= 0:
                        HitBoxArr.append([self,HitBox])
        def __delitem__(self,arg2):
                print('DEAD')
                print(arg2)
        def rm(self,proj_array):
                del proj_array[self.Id]
                for x in range(self.Id,len(proj_array)):
                        proj_array[x].Id -= 1
                self.plr.bridge.Broadcast('RM ' + str(self.Id))
        def update(self,proj_array):
                if self.life <= 0:
                        self.rm(proj_array)
                print('[proj] running ' + str(self.para[0]))
                deltx = spell(self.para[0],self.plr,[self.life]).run(self.plr)[1] - self.pos[0]
                delty = spell(self.para[1],self.plr,[self.life]).run(self.plr)[1] - self.pos[1]
                print('target ' + '(' + str(deltx) + ',' + str(delty) + ')')
                print('[proj] running ' + str(self.para[1]))

                # x and y are where we want to go but what parametric function are we going to use to get there
                # we want to get there at a speedy pace so perhaps define a default parametric function that takes a straight route to get there?
                if deltx == 0 and delty == 0:
                        # catch
                        #call a divide by zero parametric error
                        print('division by zero is no joke ya dingus')
                else:
                        if delty == 0:
                                self.pos[0] += self.speed
                        else:
                                if deltx == 0:
                                        #catch
                                        self.pos[1] += self.speed
                                else:
                                        #safe case
                                        #move them in a direction twords their target at a speed of s
                                        print('[proj] x slope ' + str((float(delty)/float(deltx))))
                                        print('[proj] y slope ' + str((float(deltx)/float(delty))))
                                        if 0 < deltx:
                                                self.pos[0] += self.speed * math.sqrt(1/(((float(delty)/float(deltx))**2) + 1))
                                        else:
                                                self.pos[0] -= self.speed * math.sqrt(1/(((float(delty)/float(deltx))**2) + 1))
                                        if 0 < delty:
                                                self.pos[1] += self.speed * math.sqrt(1/(((float(deltx)/float(delty))**2) + 1))
                                        else:
                                                self.pos[1] -= self.speed * math.sqrt(1/(((float(deltx)/float(delty))**2) + 1))
                self.plr.bridge.Broadcast('MP ' + str(self.Id) + ' ' + str(self.pos[0]) + ' ' + str(self.pos[1]))
                self.life -= 1
class player(GameObject):
	#these variables should b pretty self explanitory
	hp = 500
	mana = 500
	speed = 1
	username = 'null'
        direction = [0,0]
        #this is the mechenisim that the program uses to send data to the players "terminals"
        #call bridge.write_data(data) to send
        bridge = None
	#each of these arrays hold spell code program objects to be run by the main loop
	#the spells are to be run and the buff_spells are waiting for other spells that they called to return until they can
	#run again
	spells = []
	buff_spells = []
	def __init__(self,username,hp,mana,speed,spells,pos,bridge=None):
		self.username = username
		self.hp=hp
		self.mana=mana
		self.speed=speed
		self.spells = spells
		self.pos = pos
                self.bridge = bridge
                self.direction = [0,0]
	def calc_mana(self,cost):
		if cost <= self.mana:
			self.mana -= cost
		else:
			self.hp -= (cost - self.mana)
			self.mana = 0
	def add_spell(self,caller,spell_num,args):
		self.args.append([0,[],caller,spell_num])
	def gen_uniqId(self):
		#creates a uniqId not maching any callerIds inside of the players buff_spell array
		if len(self.buff_spells) == 0:
			return 0
		i = 0
		test = False
		while test != True:
			test = True
			for x in range(0,len(self.buff_spells)):
				if i == self.buff_spells[x].callerId:
					test = False
					break
			if test == False:
				i+=1
		return i
        def move(self,direct):
                #the player wants to move in a certain direction
                #check if they want to move in the y dir
                if direct[1] == 1:
                        self.pos[1] += self.speed
                else:
                        if direct[1] == -1:
                                self.pos[1] -= self.speed
                #check if they want to move in the x dir
                if direct[0] == -1:
                        self.pos[0] -= self.speed
                else:
                        if direct[0] == 1:
                                self.pos[0] += self.speed
        def net_move(self,direction):
                self.move(direction)
                self.bridge.Broadcast('MPL ' + self.username + ' ' + str(self.pos[0]) + ' ' + str(self.pos[1]))
        def output2screen(self):
		tag = '[' + self.username + ']'
		delim = '  |  '
		tab = '		'
		print(tag + ' printing stats...')
		print(tab + 'hp' + delim + 'mana' + delim + 'speed' + delim + 'x' + delim + 'y')
		print(tab + str(self.hp) + delim + str(self.mana) + delim + str(self.speed) + delim + str(self.pos[0]) + delim + str(self.pos[1]))
		print(tag + ' printing spells...')
                print(tag + 'direction' + str(self.direction))
		for x in range(0,len(self.spells)):
			print(tab + self.spells[x].ToString())
class spell():
	#the number of the code to be executed
	code = 0
	#the variable used to distribute the indexes for the call instructions
	call_index = 0
	#how many spells need to reslove before we can continue execution?
	callFlag = 0
	#this is used upon return to the call instructions
	ret_vars = []
	#this is the instruction pointer for the code, and needs to be incremented every instruction to point to the
	#charicter of the next statement to be ran expect errors here if there gonna happen
	ip = 0
	#the local variables of the current function
	args = []
	#this is the castee that the script will be using,determined by the on hit function inside of the main game loop
	castee = player('null',100,100,1,[],[0,0])
	#this value is used if the spell was called from within another spell to know where to return 2
	callerId = -1 # -1 means void
	retId  = [-1,0]
	def __init__(self,code,castee,args=[],call = -1,ret = -1):
		self.code = code
		self.castee = castee
		self.args = args
		self.callerId = call
		self.retId = ret
	def ToString(self):
		return 'castee:' + self.castee.username + ' ID:' + str(self.code) + ' ip:' + str(self.ip) + ' retId:' + str(self.retId) + ' args:' + str(self.args) 
	def run(self,caster,hit_arr=None,proj_arr=None):
		#this function runs the spell code and returns true if it finished and false if there are still more statements
		#to be parsed
		#get the file info
                print('[gameclasses] ' + str(proj_arr))
		File_Info = get_scode(caster.username + '/' + str(self.code) + '.spellcode',self.ip)
		
		print('[spell.run] len of spell code:' + str(len(File_Info[0])))
		#parse the spell code and store the result
		result = parse_scode.parse(File_Info[0],caster,self.castee,self,False,hit_arr,proj_arr)

		#return the result and wether or not the code ended
		end = True
		if self.ip < File_Info[1] - 1:
			end = False

		return [end,result]
	def CheckFinish(self):
		#this function checks if the call statement finished retriving its variables
		retVal = True
		if len(self.ret_vars) > 0:
			for x in range(0,len(self.ret_vars)):
				if self.ret_vars[x] == 'N':
					retVal = False
					break
		return retVal

def setStat(loc_player1,loc_player2,stat,num):
	if stat == 0:
		#set hp
		loc_player1.calc_mana(abs(loc_player2.hp - num))
		if loc_player1.hp > 0:
			loc_player2.hp = num
	if stat == 1:
		#set mana
		loc_player1.calc_mana(abs(loc_player2.mana - num))
		if loc_player1.hp > 0:
                        loc_player2.mana = num
	if stat == 2:
		#set speed
		loc_player1.calc_mana(abs(loc_player2.speed - num))
                if loc_player1.hp > 0:
                        loc_player2.speed = num
	if stat == 3:
		#set x cord
		loc_player1.calc_mana(abs(loc_player2.pos[0] - num))
		if loc_player1.hp > 0:
                        loc_player2.pos[0] = num
	if stat == 4:
		#set y cord
                loc_player1.calc_mana(abs(loc_player2.pos[1] - num))
                if loc_player1.hp > 0:
                        loc_player2.pos[1] = num
def setStat_net(loc_player1,loc_player2,stat,num):
        setStat(loc_player1,loc_player2,stat,num)
        #update all of the clients on the position of the moved player
        print('[setStat_net] broadcasting:' + str(stat))
        if stat == 3 or stat == 4: 
                loc_player1.bridge.Broadcast('MPL ' + str(loc_player2.username) + ' ' + str(loc_player2.pos[0]) + ' ' + str(loc_player2.pos[1]))
def getStat(player,stat):
	if stat == 0:
                #set hp
                return player.hp
        if stat == 1:
                #set mana
                return player.mana
        if stat == 2:
                #set speed
                return player.speed
        if stat == 3:
                #set x cord
                return player.pos[0]
        if stat == 4:
                #set y cord
                return player.pos[1]
def checkWhiteList(teststr,allowed):
        safe = True
        for i in range(0,len(teststr)):
                safe=False
                for j in range(0,len(allowed)):
                        if teststr[i] == allowed[j]:
                                safe=True
                if not safe:
                        break
        return safe
        
def getPref(uname):
        #make sure the username only contains whitelisted charicters
        
        if checkWhiteList(uname,'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                f = open(uname + '/prefs.txt')
                prefs = f.readline()[0:-1]
                f.close()
                return prefs
        return False
