import gameclasses
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket
from threading import Thread
class Listen(Thread):
    def __init__(self, p_array):
        Thread.__init__(self)
        self.p_array = p_array
    def run(self):
        network(self.p_array)
        #t = 0
        #while t < 8:
          #  print('[*] test')
           # time.sleep(2)
            #t += 2
        print('[*] FINISHED ON LISTENING THREAD :D')
                
#clients = []
class EchoWebSocket(tornado.websocket.WebSocketHandler):
        #this is needed in the websocket connection otherwise tornado will give a 403 error
        #going to need to make this code more rigid to prevent cross site scripting
        player = None
        def Broadcast(self,msg,DONT_SENDTOSELF=False):
                if DONT_SENDTOSELF == True:
                        for i in range(0,len(self.p_array)):
                            if self.p_array[i].username != self.player.username and self.p_array[i].username != 'bob':
                                    print('[netThread] BROADCASTING:' + msg + ' TO:' + self.p_array[i].username)
                                    self.p_array[i].bridge.write_message(msg)
                else:
                        for i in range(0,len(self.p_array)):
                                if self.p_array[i].username != 'bob':
                                        print('[netThread] BROADCASTING:' + msg + ' TO:' + self.p_array[i].username)    
                                        self.p_array[i].bridge.write_message(msg)
                        
                
        def initialize(self, p_array):
                self.p_array = p_array        
        def check_origin(self, origin):
                return True     

        def open(self):
                print("[netThread] WebSocket opened")
                self.player = gameclasses.player('bob',100,100,1,[],[0,0],self)
                self.p_array.append(self.player)
	#def __init__(self,username,hp,mana,speed,spells,pos,bridge):
            #in the future gonna need to add some security here, but for beta this works fine
            #self.write_message(u"You said: " + message)
        def on_message(self, message):
                print('[netThread] recieved:' + str(message))
                self.write_message(u"You said: " + message)
                parse = str(message).split(' ')
                if parse[0] == 'J':
                        print('[netThread] ADDING NEW PLAYER')
                        #the player wants to join
                        #again MUCH more security is needed here to make sure that we dont trust the name that the user
                        #is giving us, becuse if they gave us another users name then they could access their spell file
                        #actualy they could prbly give us any directory and access that file so that would be a SMAAAAAAL problem
                        #REAAAAAALY need to get that fixed before going online
                        if self.player.username == 'bob':
                                ok = True
                                #only add the player to the game if someone does not already have their uname
                                for i in range(0,len(self.p_array)):
                                        if parse[1] == self.p_array[i].username:
                                                ok = False
                                                break
                                print('[NetThread] ok_value:' + str(ok))
                                #only add them if their uname only contains whitelist charicters, NO DOT ATTACK!, hopefully :/
                                if ok == True:
                                        ok = gameclasses.checkWhiteList(parse[1],'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
                                print('[NetThread] ok_value after check:' + str(ok))
                                if ok == True:
                                        self.player.username = parse[1]
                                        #send them their key bindings
                                        self.write_message('kb ' + gameclasses.getPref(parse[1]))
                                        #send them their spawn point
                                        self.write_message('s ' + str(self.player.pos[0]) + ' ' + str(self.player.pos[1]))
                                        #send them the game state
                                        print('[netThread] LEN OF P_ARRAY:' + str(len(self.p_array)))
                                        for i in range(0,len(self.p_array)):
                                                #tell them what players are logged in
                                                if self.p_array[i].username != parse[1] and self.p_array[i].username != 'bob':
                                                        self.write_message('APL ' + str(self.p_array[i].pos[0]) + ' ' + str(self.p_array[i].pos[1]) + ' ' + self.p_array[i].username)
                                        print('[netThread] False Broadcast')
                                        #tell everyone else that we joined the server, but not ourselfs
                                        self.Broadcast('APL ' + str(self.player.pos[0]) + ' ' + str(self.player.pos[1]) + ' ' + self.player.username,True)
                                        #perhaps tell them which projecetiles exist
                                else:
                                        self.write_message(u'ERROR, UNAME ALREADY EXISTS!!!')
                        else:
                                self.write_message(u'YOU HEATHEN, YOU ARE ALREADY LOGGED IN!!')
                else:
                        if parse[0] == 'M':
                                print('[netThread] recived move command! current player:' + self.player.username + ' direction:' + str(self.player.direction))
                                #the player wants to move in a certain direction
                                #we mark a toggle so that the gameserver knows to move them that way
                                if parse[1] == 'w' and self.player.direction[1] > -1:
                                        self.player.direction[1] -= 1
                                if parse[1] == 's' and self.player.direction[1] < 1:
                                        self.player.direction[1] += 1
                                if parse[1] == 'a' and self.player.direction[0] > -1:
                                        self.player.direction[0] -= 1
                                if parse[1] == 'd' and self.player.direction[0] < 1:
                                        self.player.direction[0] += 1
                                print('[netThread] setting ' + self.player.username + ' direction to ' + str(self.player.direction))
                                print('[netThread] recived ' + parse[1] + ' as an arg')
                                #for i in range(0,len(self.p_array)):
                                #            print(str(self.p_array[i].direction))
                        else:
                                if parse[0] == 'C':
                                        #THE PLAYER IS GOING TO CAST A SPELL
                                        #YEAAAAAAAAH IT ONLY TOOK US MULTIPLE MONTHS AND HUNDREDS OF LINES OF CODE TO GET TO THIS 
                                        #MOMENT, BUT YEAAAAAAAA
                                        #perhaps append the click position to the spell here so the players can use it as an
                                        #argument
                                        self.player.spells.append(gameclasses.spell(int(parse[1]),self.player))
                                else:
                                        if parse[0] == 'UM':
                                                print('[netThread] recived UNmove command! current player:' + self.player.username + ' direction:' + str(self.player.direction))
                                                #the player wants to CEACE moveing in a certain direction
                                                #we mark a toggle so that the gameserver knows to move them that way
                                                if parse[1] == 'w': #and self.player.direction[1] < 1:
                                                        self.player.direction[1] += 1
                                                if parse[1] == 's':# and self.player.direction[1] > -1:
                                                        self.player.direction[1] -= 1
                                                if parse[1] == 'a':# and self.player.direction[0] < 1:
                                                        self.player.direction[0] += 1
                                                if parse[1] == 'd':# and self.player.direction[0] > -1:
                                                        self.player.direction[0] -= 1
                                                print('[netThread] setting ' + self.player.username + ' direction to ' + str(self.player.direction))
                                                print('[netThread] recived ' + parse[1] + ' as an arg')
                                                #for i in range(0,len(self.p_array)):
                                                #            print(str(self.p_array[i].direction))


        def on_close(self):
                print("[*] WebSocket closed")
                self.Broadcast('RMP ' + self.player.username,True)
                for i in range(0,len(self.p_array)):
                        if self.p_array[i].username == self.player.username:
                                #this should completly remove all references to the player (save spells)
                                #once these are removed the garbage collecter SHOULD delete them from memory
                                #more testing needed
                                del self.p_array[i]
                                del self.player
                                del self

                                break


def network(p_array):
        application = tornado.web.Application([
            (r'/', EchoWebSocket, dict([('p_array',p_array)])),
        ])
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
        print('[*] FINISHED LISTENING')
def net(p_array):
        l1 = Listen(p_array)
        l1.start()        
#print('[*] NO ERRORS!!!?')
#network([0,0])
#net()
