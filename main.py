from datetime import datetime, timedelta
from classes import *
from data import *

def simulation(trains,disruption):
    lt=trains.copy()
    while len(trains)!=0:
        for train in trains:
            lha=[train.time_now for train in trains]
            last_move=min(lha)
            
            print(f'[Train {train.name}] - Current time: {train.time_now.time()}. Last movement: {last_move.time()}')

            section_now = train.get_section()
            next_section = train.get_next_section()
            CEst = train.get_station()
            NEst=train.get_next_station()

            speed = train.speeds[train.position]*3.6
            arrival_time=train.calculate_arrival_time(section_now, speed)
            print(f'Current station: {CEst.name}. Next station: {NEst.name}. Arrival time: {arrival_time.time()}')

            for fault in disruption:
                if CEst in fault.stations and (fault.track_locked or fault.track_closed):
                    start,end=fault.timings
                    ini_s,end_s=fault.stations[0],fault.stations[-1]
                    if fault.track_closed:
                        if start<arrival_time<end:
                            print(f'Line is closed in the section {ini_s.name} <-> {end_s.name} between {start.time()} and {end.time()} due to {fault.tipus}')
                            CEst.change_time(train,end)
                            others = [time for time in lha if time>end]
                            last_move=min(others) if others!=[] else min(lha)
                            continue
                    elif fault.track_locked==train:
                        print(f'Track {ini_s.name} <-> {end_s.name} is occupied by train {train.name} for {end}h due to {fault.tipus}')
                        stop=train.time_now+end
                        fault.timings=train.time_now,stop
                        CEst.change_time(train,stop)
                        fault.track_locked=None
                        fault.track_closed=True
                        continue
            
            if train.origin.name==train.get_station().name: #initial Station
                train.origin.add_time(train,train.start)
##            print(train.get_next_departure(),last_move,train.get_next_departure()>last_move)

            if train.get_next_departure(train)-timedelta(minutes=train.get_station().get_wt(train))>last_move and len(trains)!=1:
                print(f'Train {train.name} should wait to leave until {train.get_next_departure(train).time()}')
                if CEst.occupied_by!=None and CEst.occupied_by!=train:
                    occupying=CEst.occupied_by
                    print(f'Track {section_now} is still occupied by {occupying.name} until {train.get_next_departure(occupying)}. Check departure time')
##                    print(train.name, train.get_arrival(train).time(), train.get_next_departure(train).time())
##                    print(occupying.name, train.get_arrival(occupying).time(), train.get_next_departure(occupying).time())
                    if train.get_next_departure(train)>train.get_arrival(occupying) and train.get_next_departure(occupying)>train.get_arrival(train):
                        print(f'Trains {occupying.name} and {train.name} cross at {CEst.name} between {max(train.get_arrival(occupying),train.get_arrival(train)).time()} and {min(train.get_next_departure(train),train.get_next_departure(occupying)).time()}')
                        pass
                    elif train.get_next_departure(train)>train.get_arrival(occupying) and train.get_next_departure(occupying)<train.get_arrival(train):
                         CEst.change_time(occupying,train.get_next_departure(train))
                         last_move=min(lha)               
                continue

            if not CEst.occupied_by or CEst.occupied_by==train: #station free or occupied by the current train 
                if CEst.name in ["Trondheim_S", "Oslo_S"] and NEst.occupied_by:
                    continue
                print(f'Train {train.name} will arrive to {NEst.name} at {arrival_time.time()} (avg speed: {speed} km/h)')
                train.time_now=arrival_time
                NEst.add_time(train,arrival_time)
                last_move=arrival_time
##                print(section_now)
                NEst.occupy(train)
                CEst.clear()
                print(f'[Train {train.name}] - {section_now} free' if {NEst.name==train.direction} else '[Train {train.name}] - {next_section} occupied and {section_now} free')
                if NEst.name==train.direction: #check is the next station is the last one
                    NEst.clear()
                    train.delete()
                    print(f'Train {train.name} arrived to {train.direction} at {train.time_now.time()}. Final destination.')
            else:
                occupying=CEst.occupied_by
                last_dep_occupying=occupying.get_last_departure(occupying)
                next_departure=train.get_next_departure(train)
                print(f'Track {train.get_section()} occupied by {occupying.name}')
                print(f'[Train {train.name}]-{next_departure.time()}')
                print(f'[Train {occupying.name}]-{last_dep_occupying.time()}')

                if last_dep_occupying.time()>next_departure.time(): #train arrived before, thus, occupying should wait
##                    speed = train.speeds[train.position]*3.6
                    print(f'Train {train.name} remains leaving at {next_departure.time()}. Arrival time to {occupying.get_last_station().name}: {arrival_time.time()}')
                    CEst.clear()
                    if arrival_time>last_dep_occupying: #change occupying timings
                        new_departure=arrival_time
                        LEst_occupying=occupying.get_last_station()
                        LEst_occupying.change_time(occupying,new_departure)
##                        occupying.time_now=new_departure
                        occupying.position-=1
                    else:
                        pass
                elif next_departure>train.get_arrival(occupying): #trains cross each other at the station
                    print(f'Trains {occupying.name} and {train.name} cross at {CEst.name} between {max(train.get_arrival(occupying),train.get_arrival(train)).time()} and {min(train.get_next_departure(train),train.get_next_departure(occupying)).time()}')
                else: #occupying arrived before, thus, train should wait
                    delta=timedelta(minutes=train.get_station().get_wt(occupying))
                    new_time=train.get_next_departure(occupying)-delta
                    CEst.change_time(train,new_time)
##                    train.time_now=new_time
                train.position-=1
            train.move_position()
##    print(f' Delays for: {fa.tipus}')

    delays(lt)
##    crossings(lt)

            
def delays(lt):
    for train in lt:
        globals()[f'dr{train.name}']={}
        t=0
        for i in F6:
            if "ATD" in i.schedule[train.name]:
                if i.schedule[train.name]["ETD"]<i.schedule[train.name]["ATD"]:
                    tot=(i.schedule[train.name]["ATD"]-i.schedule[train.name]["ETD"]).total_seconds()//60
                    print(f'Delay of {tot} minutes at {i.name}')
                    globals()[f'dr{train.name}'][i.name]=tot
                    t+=tot
                
                else:
                    tot=(i.schedule[train.name]["ETD"]-i.schedule[train.name]["ATD"]).total_seconds()//60
                    globals()[f'dr{train.name}'][i.name]=tot
                    print(f'Recuperación de {tot} minutos en {i.name}')
                    t-=tot
        print(f'Train {train.name} had a delay of {t} minutes.')
##        return globals()[f'dr{train.name}']


def crossings(lt):
    for t1 in lt:
        tref=t1.name
        t0=Heimdal.schedule[tref]["ETD"]
        lp={}
        lc=[]
        for t2 in lt:
            train=t2.name
            c=0
            t1=Heimdal.schedule[train]["ETD"]
            if train==tref:
                continue
            if t0<t1:
                for i in F6[2:-1]:
                    for values in i.schedule[tref].values():
                        if values in i.schedule[train].values() and values!= None:
                            if train not in lp:
                                lp[train] = f'{i.name} at {values.time()}'
                            else:
                                pass
                    if i.schedule[tref]["ETD"]>i.schedule[train]["ETD"] and c<1:
                        if train not in lp:
                            lc.append(f'{train} - before arriving to {i.name}')
                            c+=1
                        else:
                            pass
            if t0>t1:
                for i in F6[2:-1]:
                    for values in i.schedule[tref].values():
                        if values in i.schedule[train].values() and values!= None:
                            if train not in lp:
                                lp[train] = f'{i.name} at {values.time()}'
                            else:
                                pass
                    if i.schedule[tref]["ETD"]<i.schedule[train]["ETD"] and c<1:
                        if train not in lp:
                            lc.append(f'{train} - before leaving from {i.name}')
                            c+=1
                        else:
                            pass
        if lp!={}:
            print(f'Train {tref} cross with: {", ".join(f"{key} - {value}" for key, value in lp.items())}')

        if lc!=[]:
            print(f'Train {tref} cross during double track with: {", ".join(resto for resto in lc)}')





if __name__ == "__main__":
    simulation(trains,D)


for i in ltotal:
    print(f'data{i.name}=',i.get_route())





    
