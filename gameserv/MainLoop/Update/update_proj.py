#loop over a list of projectiles and update them
def Update_List(ent_list):
        for x in range(0,len(ent_list)):
                ent_list[x].update(ent_list)
