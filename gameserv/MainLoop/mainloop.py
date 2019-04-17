import sys
sys.path.append('./Parse')
sys.path.append('./Collision')
sys.path.append('./Update')
sys.path.append('./Network')
import RunCode
import collide
import update_proj
import gameclasses
import threading
import output
import time
from threading import Thread
#initialise the arrays that the game runs on
global Player_Array
Player_Array = []
Proj_Array = []
HitBox_Array = [[],[]]
class MovePlr(Thread):
        def __init__(self):#,Player_Array):
                Thread.__init__(self)
                #self.p_arr = Player_Array
        def run(self):
                print('[MoveThread] RUNNING')
                while True:
                        time.sleep(.1)
                        for i in range(0,len(Player_Array)):
                                #only send data over the wire if we need to update somthing
                                if Player_Array[i].direction[0] != 0 or Player_Array[i].direction[1] != 0:
                                        #I almost want to make this send to the player to confirm that the server 
                                        #is accepting that move
                                        print('[MoveThread] moving player ' + Player_Array[i].username + ' whos vect is ' + str(Player_Array[i].direction))
                                        Player_Array[i].net_move(Player_Array[i].direction)
def Debug():
        #print(gameclasses.checkWhiteList('123456789','abcdefghijklmnopqrstuvwxyz'))
        print(gameclasses.getPref('a'))
        for x in range(0,len(Player_Array)):
                Player_Array[x].output2screen()
        for x in range(0,len(Proj_Array)):
            print(type(Proj_Array[x]))
            print('[*] projectile located at ' + str(Proj_Array[x].pos) + ' to call ' + str(Proj_Array[x].plr.username) + '\'s ' + ' spell ' + str(Proj_Array[x].OnDeath))
            print('[*] its id is:' + str(Proj_Array[x].Id))
        print('[*] proj length:' + str(len(Proj_Array)))
        if raw_input('->') == 'q':
                quit()
if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
                Player_Array = [gameclasses.player('p0',100,100,1,[],[20,100]), gameclasses.player('p1',100,100,1,[],[20,0])]
                Player_Array[0].spells = [gameclasses.spell(5,Player_Array[1])]
                HitBox_Array[0] = [[Player_Array[0],[2,2]],[Player_Array[1],[2,2]]]
                Proj_Array = [gameclasses.proj(Player_Array[1],100,.25,[8,9],3,-1,[2,2],HitBox_Array[1],0)]
                Proj_Array[0].pos = [-5,0]
p_input = MovePlr()
p_input.start()
print('[*] it doesnt block!')
output.net(Player_Array)
while True:
        Debug()
        #update_player_pos
        print('[main] ' + str(Proj_Array))
        RunCode.Run_Code(Player_Array,HitBox_Array,Proj_Array)
        update_proj.Update_List(Proj_Array)
        collide.CheckCollision(HitBox_Array,Proj_Array)
        for i in range(0,len(Player_Array)):
                if Player_Array[i].mana > 100:
                        Player_Array[i].mana = 100
                if Player_Array[i].mana < 100:
                        Player_Array[i].mana += 1
        #output to clients
