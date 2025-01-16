from data import *
from datetime import datetime, timedelta

class Station:
    def __init__(self, name, km):
        self.name = name
        self.km = km
        self.schedule={}
        self.occupied_by=None

    def add_time(self,train,earr):
        if self.name==train.direction:
            self.schedule[train.name]={"ATA": earr,"ETD":None}
            print(f'{earr.time()} - Arrival time of train {train.name} to {self.name}')
        elif self.name==train.origin.name:
            self.schedule[train.name]={"ATA": None,"ETD":earr}
        else:
            if self.name in train.non_stop():
                self.schedule[train.name]={"ATA": earr,"ETD":earr}
                print(f"Train {train.name} doesn't stop at {self.name}")
                train.time_now-=timedelta(minutes=self.get_wt(train))
            else:             
                self.schedule[train.name]={"ATA": earr,"ETD":earr+timedelta(minutes=self.get_wt(train))}
                print(f'{(earr+timedelta(minutes=self.get_wt(train))).time()} - Departure time of train {train.name} from {self.name}')
        train.time_now+=timedelta(minutes=self.get_wt(train))
        
    def change_time(self,train,rdep):
        self.schedule[train.name]["ATD"]= rdep
        train.time_now=rdep
        print(f'{rdep.time()}. New departure time (ATD) of train {train.name} from {self.name}. Last departure time (ETD): {self.schedule[train.name]["ETD"]}')

    def occupy(self,train):
        lim=stations_all.index("Strandlykkja")
        p=stations_all.index(self.name)
        if p>=lim:
            print(f'Next section has double track, so no locking here')
            self.occupied_by=None
        else:
            self.occupied_by=train
            print(f'{self.name} occupied by {self.occupied_by}')


    def clear(self):
        self.occupied_by=None
##        print(f'{self.name} free')


    def get_wt(self,train):
        return wt[self.name][train.name-1]

#Create the stations
F6 = []
for i in range(len(stations_all)):
    globals()[stations_all[i]] = Station(stations_all[i], length_all[i])
    F6.append(globals()[stations_all[i]])

class Section:
    def __init__(self, origin, end, length):
        self.origin= origin
        self.end = end
        self.length = length
        
    def get_section(self,train):
        if train.direction == "Trondheim_S":
            return self.end, self.origin, self.length
        return self.origin, self.end, self.length


    def calculate_time(self, speed):
        return int((self.length / speed) * 3600)  # in seconds

    def __repr__(self):
        return f"Track ({self.origin.name} <-> {self.end.name}, {self.length:.2f} km)"

#Create the sections
sections = []
for i in range(len(stations_all)-1):
    ea=F6[i]
    es=F6[i+1]
    sections.append(Section(ea,es,abs(ea.km-es.km)))

class Train:
    def __init__(self, name, start, direction, speeds, sections):
        self.name = name
        self.start = start
        self.direction = direction.name
        self.sections = sections
        self.origin = Trondheim_S if self.direction=="Oslo_S" else Oslo_S
        self.position = 0
        self.speeds = speeds
        self.time_now = start

    def move_position(self):
        self.position += 1

    def get_section(self):
        return self.sections[self.position]
    
    def get_next_section(self):
        if self.position==len(sections)-1:
            pass
        else:
            return self.sections[self.position+1]

    def get_station(self):
        return F6[self.position] if self.direction == "Oslo_S" else F6[::-1][self.position]

    def get_last_station(self):
        return F6[self.position-1] if self.direction == "Oslo_S" else F6[::-1][self.position-1]
    
    def non_stop(self):
        return non_stop[self.name-1]

    def get_arrival(self,train): #to know when the train arrives to station self
        return self.get_station().schedule[train.name]["ATA"]

    def get_next_departure(self,train): #to know when will the train leave the next station
        if train.name in self.get_station().schedule:
            if "ATD" in self.get_station().schedule[train.name]:
                return self.get_station().schedule[train.name]["ATD"]
            return self.get_station().schedule[train.name]["ETD"]

    def get_last_departure(self,train): #to know when did the train leave from the station before self
        if "ATD" in self.get_last_station().schedule[train.name]:
            return self.get_last_station().schedule[train.name]["ATD"]
        return self.get_last_station().schedule[train.name]["ETD"]
       
    def get_next_station(self):
        return F6[self.position+1] if self.direction == "Oslo_S" else F6[::-1][self.position+1]

    def get_wt(self,station):
        return wt[station.name][self.name-1]

    def calculate_arrival_time(self, section, speed):
        time_section = section.calculate_time(speed)
        return self.time_now + timedelta(seconds=time_section)
    
    def delete(self):
        trains.remove(globals()[f't{self.name}'])

    def get_route(self):
        d=[]
        for i in F6:
            d.append(i.schedule[self.name])
        return d

    def __repr__(self):
        return f"train({self.name}, {self.direction})"

class Disruption:
    def __init__(self,tipus):
        self.tipus=tipus
        self.speed_reduced=None
        self.track_closed=False
        self.track_locked=None
        self.log={}
        self.stations=[]
        self.timings=[]


    def close_section(self,ini_s,end_s,hini,hfin):
        self.log["section closed"]={"stations":[ini_s,end_s],"time":[hini,hfin]}
        self.track_closed=True
        ini=F6.index(ini_s)
        end=F6.index(end_s)
        self.timings=self.log["section closed"]["time"]
        for i in range(ini,end+1):
            self.stations.append(F6[i])
            
    def failure(self,train,station,t):
        self.log["section closed"]={"stations":station,"time":t}
        self.track_locked=train
        self.timings=0,t
        ini=F6.index(station)
        end=F6.index(station)+1 if train.origin == Trondheim_S else F6.index(station)-1
        if ini<end:
            for i in range(ini,end+1):
                self.stations.append(F6[i])
        else:
            for i in range(end,ini+1):
                self.stations.append(F6[i])
        
    def train_speed(self,train,red,ini_s,end_s):
        self.speed_reduced=train
        if "speed variation" not in self.log:
            self.log["speed variation"]={"trains":[],"stations":[]}

        self.log["speed variation"]["trains"]=(train,red)
        self.log["speed variation"]["stations"]=(ini_s,end_s)
            
##        for trains in self.log["speed reduction"]["trains"]:
        t,sred=self.log["speed variation"]["trains"]
##            pos=self.log["speed reduction"]["trains"].index(trains)
        ini=F6.index(ini_s)
        end=F6.index(end_s)
        for v in range(ini,end):
            nv=round(t.speeds[v]*(1+sred),2)
##            print(nv,t.speeds[v])

            t.speeds[v]=nv
##            self.stations.append(F6[v])

    def track_reduction(self,red,ini_s,end_s):
        self.speed_reduced=True
        if "speed variation" not in self.log:
            self.log["speed variation"]={"trains":[],"stations":[]}

        self.log["speed variation"]["stations"]=(ini_s,end_s)
        self.log["speed variation"]["trains"]=("all",red)

        ini=F6.index(ini_s)
        end=F6.index(end_s)
##        print(ini_s.name,end_s.name)
        for t in ltotal:
            for v in range(ini,end):
                if t.name<=6 and t.speeds[v]>red/3.6:
##                    print(t.name,F6[v].name,t.speeds[v]) 
                    t.speeds[v]=round(red/3.6,2)

        for s in ltotal:
            for v in range(-end-1,-ini-1):
                if s.name>6 and s.speeds[v+1]>red/3.6:
##                    print(s.name,F6[::-1][v].name,s.speeds[v+1])
                    s.speeds[v+1]=round(red/3.6,2)
                    
        for i in range(ini,end+1):
            self.stations.append(F6[i])

    def __repr__(self):
        if self.track_closed:
            return f'Closed track ({self.stations[0].name} <-> {self.stations[-1].name}) from {self.timings[0].time()} until {self.timings[-1].time()} due to {self.tipus}'

    
        if self.speed_reduced:
            if type(self.speed_reduced)==Train:
                t,sred=self.log["speed variation"]["trains"]
                ini,end=[p.name for p in self.log["speed variation"]["stations"]]
                return f'Speed changed by {sred*100}% of train {t.name} ({ini} <-> {end}) due to {self.tipus}'
            else:
                t,sred=self.log["speed variation"]["trains"]
                ini,end=[p.name for p in self.log["speed variation"]["stations"]]
                return f'Max speed reduced at {sred} km/h ({ini} <-> {end}) due to {self.tipus}'

        if self.track_locked:
            return f'Closed track ({self.stations[0].name} <-> {self.stations[-1].name}) for {self.timings[1].total_seconds()/3600}h  due to {self.tipus} from train {self.track_locked.name}'
              
        else:
            return f'F6 timetable under normal conditions'            


t1 = Train(1, datetime(2024, 1, 1, 5, 55), Oslo_S, st[0],sections)
t2 = Train(2, datetime(2024, 1, 1, 8, 16), Oslo_S, st[1],sections)
t3 = Train(3, datetime(2024, 1, 1, 10, 18), Oslo_S, st[2], sections)
t4 = Train(4, datetime(2024, 1, 1, 13, 6), Oslo_S, st[3], sections)
t5 = Train(5, datetime(2024, 1, 1, 15, 26), Oslo_S, st[4], sections)
t6 = Train(6, datetime(2024, 1, 1, 23, 17), Oslo_S, st[5], sections)
t7 = Train(7, datetime(2024, 1, 1, 8, 2), Trondheim_S, st[6][::-1], sections[::-1])
t8 = Train(8, datetime(2024, 1, 1, 10, 2), Trondheim_S, st[7][::-1], sections[::-1])
t9 = Train(9, datetime(2024, 1, 1, 14, 2), Trondheim_S, st[8][::-1], sections[::-1])
t10 = Train(10, datetime(2024, 1, 1, 16, 2), Trondheim_S, st[9][::-1], sections[::-1])
t11 = Train(11, datetime(2024, 1, 1, 18, 2), Trondheim_S, st[10][::-1], sections[::-1])
t12 = Train(12, datetime(2024, 1, 1, 22, 50), Trondheim_S, st[11][::-1], sections[::-1])

trains=[t1,t7,t2,t3,t8,t4,t9,t5,t10,t11,t12,t6]
ltotal = trains.copy()

##------------CASE 0---------------##
##D= Disruption("General")

##------------CASE 1---------------##
##D= Disruption("Testing train")
##D.train_speed(t1,-0.25,Hjerkinn,Oyer) #Testing train, speed reduction

##------------CASE 2---------------##
##D = Disruption("Slippery track")
##D.track_reduction(60,Lillehammer,Hamar)  #Slippery track, max speed 60 km/h

##------------CASE 3---------------##
##D=Disruption("Maintenance work")
##D.close_section(Vinstra,Faberg,datetime(2024,1,1,22,0),datetime(2024,1,2,2,0)) #Closed track due to maintenance work

##------------CASE 4---------------##
##D=Disruption("Breakdown")
##D.failure(t4,Otta,timedelta(minutes=120)) #Closed track between due to train failure

##------------CASE 5---------------##
##D1=Disruption("Winter storm")
##D1.close_section(Oppdal,Dombas,datetime(2024,1,1,7,0),datetime(2024,1,1,10,0))
##D2= Disruption("Slippery track")
##D2.track_reduction(60,Dombas,Hamar)

##D=[D1,D2]

##------------SCENARIO 1---------------##
##D1=Disruption("Electricity problems")
##D1.failure(t6,Selsbakk,timedelta(minutes=80)) #Closed track between due to tree over the overhead line
##D2=Disruption("Electricity problems")
##D2.failure(t6,Heimdal,timedelta(minutes=60)) #Closed track between due to tree over the overhead line
##
##D3=Disruption("Train problems")
##D3.failure(t6,Fokstua,timedelta(minutes=65)) #Closed track between due to train failure
##D4=Disruption("Wait for train")
##D4.failure(t12,Dovre,timedelta(minutes=100)) #Waiting for the next train

##D=[D1,D2,D3,D4]

##------------SCENARIO 2---------------##
##D1=Disruption("Train problems")
##D1.train_speed(t7,-0.15,Hjerkinn, Oyer) #Speed reduction due to train problems

##D2=Disruption("Salt coating")
##D2.failure(t12,Dombas,timedelta(minutes=40)) #Closed track due to salt coating

##D=[D1,D2]


##------------SCENARIO 3---------------##
##D1=Disruption("Collision")
##D1.failure(t3,Fagerhaug,timedelta(minutes=55))
##
##D2=Disruption("Collision")
##D2.failure(t4,Lundamo,timedelta(minutes=60))
##
##D3=Disruption("Collision")
##D3.failure(t2,Storen,timedelta(minutes=50))
##
##D4=Disruption("Speed regulation")
##D4.train_speed(t3,0.25,Faberg,Oslo_S)

##D=[D1,D2,D3,D4]







