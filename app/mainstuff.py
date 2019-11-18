from app import db
from app.models import player,hero,player_hero,ana,match,player_match
import requests
import collections
import random
class playertable():

    def getinfo(self,playerid):
        plist=[]
        plist.append(playerid)
        req1=requests.get(f'https://api.opendota.com/api/players/{playerid}/wl')
        json1=req1.json()
        for key,value in json1.items():
            plist.append(value)
        plist.append(int(plist[1]+plist[2]))
        req2=requests.get(f"https://api.opendota.com/api/players/{playerid}/totals")
        json2=req2.json()

        #gpm calc
        for i in json2:
            if i['field']=='gold_per_min':
                mydict=i
                break

        l1=[]
        for key,values in mydict.items():
            l1.append(values)
        gpm=l1[2]/l1[1]
        plist.append(int(gpm))

        #xpm calc
        for i in json2:
            if i['field']=='xp_per_min':
                mydict=i
                break
        l1=[]
        for key,values in mydict.items():
            l1.append(values)

        xpm=l1[2]/l1[1]
        plist.append(int(xpm))   #[id,win,loss,totalmatches,gpm,xpm]

        #kda calc
        for i in json2:
            if i['field']=='kda':
                mydict=i
                break

        l1=[]
        for key,values in mydict.items():
            l1.append(values)

        kda=l1[2]/l1[1]
        plist.append(kda)  #[id,win,loss,totalmatches,gpm,xpm,kda]

        req3=requests.get(f"https://api.opendota.com/api/players/{playerid}")
        json3=req3.json()
        for key,values in json3.items():
            if key=="solo_competitive_rank":
                plist.append(values)           #[id,win,loss,totalmatches,gpm,xpm,kda,mmr]

        player_user=player(pid=plist[0],no_wins=plist[1],no_losses=plist[2],no_match=plist[3],avg_gpm=plist[4],avg_xpm=plist[5],avg_kda=plist[6],mmr=plist[7])
        db.session.add(player_user)
        db.session.commit()


        ####!!!!!!!!!!!player Performance table !!!!!!!!!!!!!#

        re1=requests.get(f'https://api.opendota.com/api/players/{playerid}/rankings')
        j1=re1.json()
        print(j1)
        id=[d['hero_id'] for d in j1]
        perc=[d['percent_rank'] for d in j1]
        size=len(id)
        print(size)

        playerdict=dict(zip(id,perc))
        print(playerdict)
        odpd=collections.OrderedDict(sorted(playerdict.items()))
        print(odpd)

        perc1=list(odpd.values())
        print(perc1)
        id1=list(odpd.keys())
        print(id1)
        print(len(id1))
        k=0
        result=0
        score=0
        desc=[]
        while k<size:
            result=perc1[k]
            print(result)
            if result <= 0.2:
                desc.append("Herald")

            elif result >0.2 and result<=0.3:
                desc.append("Guardian")


            elif result >0.3 and result<=0.4:
                desc.append("Crusader")


            elif result >0.4 and result<=0.5:
                desc.append("Archon")


            elif result >0.5 and result<=0.7:
                desc.append("Legend")

            elif result>0.7 and result<=0.8:
                desc.append("Ancient")

            elif result >0.8 and result <=0.9:
                desc.append("Divine")

            else:
                desc.append("Immortal")

            k=k+1


        print(desc)
        names=[]
        k=0
        while k<size:
            nam=hero.query.filter_by(hid=id1[k]).all()
            for n in nam:
                nama=n.hero_name
            names.append(nama)
            k=k+1


        print(names)


        k=0
        while k<size:
            user=player_hero(hero_id=id1[k],score=perc1[k],player_id=playerid,Performance=desc[k],heroname=names[k])
            db.session.add(user)
            db.session.commit()
            k=k+1



class matchtable():


    def getmatch(self,matchid):



        re5=requests.get(f"https://api.opendota.com/api/matches/{matchid}")
        js5=re5.json()


        list5=[]
        for key,values in js5.items():
            if key=="players":
                list5.append(values)

        print(list5)
        death=[]
        for i in list5:
            for j in i:

                for key,values in j.items():
                    if key=="deaths":
                        death.append(values)
        sumd=sum(death)
        print(sumd)
        assist=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="assists":
                        assist.append(values)

        suma=sum(assist)
        print(suma)
        kills=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="kills":
                        kills.append(values)

        sumk=sum(kills)
        print(sumk)




        [d[0] for d in list5]

        #total gold

        tot_gold=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="total_gold":
                        tot_gold.append(values)




        print(tot_gold)
        sumg=sum(tot_gold)


        tot_xp=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="total_xp":
                        tot_xp.append(values)

        sumx=sum(tot_xp)

        for key,values in js5.items():
            if key=="duration":
                duration=round(values/60)

        print(duration)

        for key,values in js5.items():
            if key=="radiant_win":
                if values:
                    winner="Radiant"
                else:
                    winner="Dire"

        print(winner)

        matchtab=match(mid=matchid,tot_kills=sumk,tot_assist=suma,tot_death=sumd,tot_gold=sumg,tot_xp=sumx,duration=duration,winner=winner)
        db.session.add(matchtab)
        db.session.commit()


        ############!!!!!!!!!!!!PLAYER_MATCH TABLE !!!!!!!!!!!!!!!!!!!!##############
        kda=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="kda":
                        kda.append(values)

        print(kda)

        gpm=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="gold_per_min":
                        gpm.append(values)

        print(gpm)

        xpm=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="xp_per_min":
                        xpm.append(values)


        print(xpm)


        playernames=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="personaname":
                        playernames.append(values)


        print(playernames)


        playerids=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="account_id":
                        if values==None:
                            randkey=random.randrange(1000,9999,20)
                            playerids.append(randkey)
                        else:
                            playerids.append(values)


        print(playerids)

        heroids=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="hero_id":
                        heroids.append(values)

        print(heroids)

        heronames=[]
        k=0
        while k<10:
            heroes=hero.query.filter_by(hid=heroids[k]).all()
            for h in heroes:
                heronames.append(h.hero_name)
            k=k+1

        print(heronames)
        radstat=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="isRadiant":
                        radstat.append(values)


        print(radstat)
        teamstat=[]
        for i in radstat:
            if i:
                teamstat.append("Radiant")
            else:
                teamstat.append("Dire")
        print(teamstat)


        winstatus=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="win":
                        winstatus.append(values)
        print(winstatus)

        actwinstat=[]
        for i in winstatus:
            if i:
                actwinstat.append("WON")
            else:
                actwinstat.append("LOST")

        print(actwinstat)


        k=0
        while k<10:
            user=player_match(matchid=matchid,playerid=playerids[k],kill_count=kills[k],death_count=death[k],assist_count=assist[k],kdaratio=kda[k],playername=playernames[k],xpm=xpm[k],gpm=gpm[k],team=teamstat[k],result=actwinstat[k],heroname=heronames[k])
            db.session.add(user)
            db.session.commit()
            k=k+1




        ########!!!!!!!!!!!!!!! ANA TABLE !!!!!!!!!!!!!! #########
        #re1=requests.get("https://api.opendota.com/api/players/311360822/rankings")
        #js1=re1.json()
        #id=[d['hero_id'] for d in js1]
        #perc=[d['percent_rank'] for d in js1]
        #prodict=dict(zip(id,perc))
        #print(prodict)
        #odpd=collections.OrderedDict(sorted(prodict.items()))
        #print(odpd)
        #k=0
        #for key,values in odpd.items():
            #user=ana(hero_id=key,score=values)
            #db.session.add(user)
            #db.session.commit()
            #k=k+1



        #!!!!!!!!!!!Hero TABle !!!!!!!!!!!#
        #def getheroinfo(self):
        #idar=[]
        #total=[]
        #names=[]
        #wins=[]
        #loss=[]
        #l1=[]
        #l2=[]

        #req1=requests.get("https://api.opendota.com/api/heroes")
        #json1=req1.json()

        #for i in json1:
            #if i['id']:
                #idar.append(i['id'])

        #for i in json1:
            #if i['localized_name']:
                #names.append(i['localized_name'])

        #print(names)
        #print(len(names))
        #print(len(idar))
        #print(idar)

        #k=1
        #while k < 113:
        #req2=requests.get(f"https://api.opendota.com/api/heroes/128/durations")
        #json2=req2.json()
        #print(json2)

        #for i in json2:
            #if i['games_played']:
                #l1.append(i['games_played'])

        #tots=sum(l1)
        #total.append(tots)

        #for i in json2:
            #if i['wins']:
                #l2.append(i['wins'])

        #w=sum(l2)
        #wins.append(w)

        #l=tots-w
        #loss.append(l)
        #k=k+1

        #print(wins)
        #print(len(total))




        #m=0
        #while m < 117:
            #user=hero(hero_name=names[m],hid=idar[m],tot_match=total[m],wins=wins[m],loss=loss[m])
            #db.session.add(user)
            #db.session.commit()
            #m=m+1
