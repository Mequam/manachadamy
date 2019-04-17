import gameclasses
def CheckColl(Pos1,Hit1,Pos2,Hit2):
        #this function takes two positions and hitboxes and checks to see if there is a hitbox collison
        if not (Pos1[0] + Hit1[0] < Pos2[0] or Pos2[0] + Hit2[0] < Pos1[0]) and not (Pos1[1] + Hit1[1] < Pos2[1] or Pos2[1] + Hit2[1] < Pos1[1]):
                return True
        else:
                return False

def ListBoxCheck(hitboxlistA,hitboxlistB,onColl,VarList):
#this function takes an array of arrays that are structerd in the format [object_/w_pos,[hitboxXl,hitboxYl]]
#it then runns onColl with the two objects as paramaters for every posative hit                         
        for A in range(0,len(hitboxlistA)):
                for B in range(0,len(hitboxlistB)):
                        if CheckColl(hitboxlistA[A][0].pos,hitboxlistA[A][1],hitboxlistB[B][0].pos,hitboxlistB[B][1]):  
                            onColl(hitboxlistA[A][0],hitboxlistB[B][0],VarList)
def updateSpellArr(player,proj,VarList):
        if proj.OnDeath > -1 and player != proj.plr and len(VarList[0]) > 0:
                proj.plr.spells.append(gameclasses.spell(proj.OnDeath,player))
                proj.rm(VarList[0])
def CheckCollision(HitBoxList,Proj_Array):
        #this is one of the main functions of the game, it takes a list of hitboxlists and checks the the collision 
        #between them, placing the proper spell onto the players spell array, 
        #IMPORTANT HitBoxList[0] is assumed to only contain players
        for x in range(1,len(HitBoxList)):
                ListBoxCheck(HitBoxList[0],HitBoxList[x],updateSpellArr,[Proj_Array])
