from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import numpy as np

import emergency_signal as es
import emergency_detection as ed
import green_time as gt
import vehicle_info as vi
import change_lane as cl

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

#==============================================================================

# cross.sumocfg 실행

def generate_routefile():
    random.seed(10)
    N = 350 # number of time steps

    # 1분당 교통량 데이터
    traffic_volume_per_hour = {
        "WE": 5212,
        "EW": 6207,
        "NS": 870,
        "SN": 2974,
        "LT1": 1114,
        "LT2": 2596,
        "RT1": 30,
        "RT2": 25,
        "RT3": 20,
        "RT4": 15,
        "UT1": 10,
        "UT2": 10,
    }

    # 1초당 교통량 데이터로 변환 (Poisson 분포의 λ)
    traffic_lambda_per_second = {k: v / 3600 for k, v in traffic_volume_per_hour.items()}

    lanes = ["0", "1", "2", "3", "4"]

    with open("config/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="passenger" accel="5" decel="10" sigma="0.5" length="5" minGap="2" departSpeed="16.67" maxSpeed="16.67" guiShape="passenger" color="grey"/>
        <vType id="emergency" vClass="emergency" accel="5" decel="10" sigma="0.5" length="7" minGap="2" departSpeed="16.67" maxSpeed="35" color="red"/>
        <vType id="bus" accel="5" decel="10" sigma="0.5" length="12" minGap="2" departSpeed="12" maxSpeed="12" guiShape="bus" color="0,0,255"/>
        <vType id="truck" accel="5" decel="10" sigma="0.5" length="10" minGap="2" departSpeed="10" maxSpeed="10" guiShape="truck" color="0,255,0"/>
        
        <route id="right" edges="3c c4" />
        <route id="left" edges="4c c3" />
        <route id="down" edges="1c c2" />
        <route id="up" edges="2c c1" />
        <route id="leftTurn1" edges="4c c2" />
        <route id="leftTurn2" edges="3c c1" />
        <route id="rightTurn1" edges="2c c4" />
        <route id="rightTurn2" edges="4c c1" />
        <route id="rightTurn3" edges="1c c3" />
        <route id="rightTurn4" edges="3c c2" />
        <route id="uTurn1" edges="1c c1" />
        <route id="uTurn2" edges="2c c2" />
        """, file=routes)

        vehNr = 0
        for i in range(N):
            # Generate emergency vehicles every 500 steps
            if i in [50]:
                lane = random.choice(lanes)
                print('    <vehicle id="emergency_%i" type="emergency" route="left" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if i % 100 <= 50: 
                for direction, lambda_val in traffic_lambda_per_second.items():
                    num_vehicles = np.random.poisson(lambda_val)
                    for _ in range(num_vehicles):
                        lane = random.choice(lanes)
                        vehicle_type_random = random.uniform(0, 1)

                        # Assigning vehicle type based on arbitrary ratios for each route
                        if direction == "WE":
                            if vehicle_type_random < 77/5212:
                                type_choice = "bus"
                            elif vehicle_type_random < (77/5212 + 4777/5212):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "right"
                        elif direction == "EW":
                            if vehicle_type_random < 22/6207:
                                type_choice = "bus"
                            elif vehicle_type_random < (22/6207 + 5891/6207):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "left"
                        elif direction == "NS":
                            if vehicle_type_random < 13/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (13/870 + 854/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "down"
                        elif direction == "SN":
                            if vehicle_type_random < 10/2974:
                                type_choice = "bus"
                            elif vehicle_type_random < (10/2974 + 2913/2974):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "up"
                        elif direction == "LT1":
                            if vehicle_type_random < 0/1114:
                                type_choice = "bus"
                            elif vehicle_type_random < (0/1114 + 1018/1114):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "leftTurn1"
                        elif direction == "LT2":
                            if vehicle_type_random < 0/2596:
                                type_choice = "bus"
                            elif vehicle_type_random < (0/2596 + 2500/2596):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "leftTurn2"
                        elif direction == "RT1":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "rightTurn1"
                        elif direction == "RT2":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "rightTurn2"
                        elif direction == "RT3":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "rightTurn3"
                        elif direction == "RT4":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "rightTurn4"
                        elif direction == "UT1":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "uTurn1"
                        elif direction == "UT2":
                            if vehicle_type_random < 5/870:
                                type_choice = "bus"
                            elif vehicle_type_random < (5/870 + 860/870):
                                type_choice = "passenger"
                            else:
                                type_choice = "truck"
                            route = "uTurn2"

                        # Output vehicle definition
                        print('    <vehicle id="%s_%i" type="%s" route="%s" depart="%i" departLane="%s" />' % (
                            route, vehNr, type_choice, route, i, lane), file=routes)
                        vehNr += 1
        print("</routes>", file=routes)

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>

# 회피 관련
lcmode = 0b011001000101 # 차량 차선 변경 모드
lctime = 3 # 차선 변경 지속 시간 -> 차선 변경하고 다시 돌아온다는 건가?
detect_range = 80 # 긴급차량 감지 범위

# main
def run():
    """execute the TraCI control loop"""
    step = 0
    temp_step = 99999
    traci.trafficlight.setProgram("c", 0)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        print(f"초기 Program: {traci.trafficlight.getProgram("c")}")
        print(f"step: {step}")

        loop = ["0", "1", "2", "3", "4"]
        edge_id = "4c"
        eme_info = None
        for loop_id in loop:
            lane_id = f"{edge_id}_{loop_id}"
            if ed.get_detected_vehicle_ids(loop_id):
                eme_info, duration = es.signal_change(edge_id, lane_id, loop_id)
                print(f"temp_step: {temp_step}")
                
                if eme_info:
                    temp_step = step + duration
                    break  # 긴급차량 감지 시 반복 중단
        
        veh_list = traci.edge.getLastStepVehicleIDs(edge_id)

        if eme_info:
            cl.change(veh_list, eme_info, lcmode, lctime, detect_range) 
            cl.change_small_lane(eme_info, lctime)
    
        if temp_step < step:
            traci.trafficlight.setProgram("c", 1)
        
        print(f"변경 후 Program: {traci.trafficlight.getProgram("c")}")

        step += 1
        

    
    traci.close()
    sys.stdout.flush()
    data_rangling()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=True, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def make_csv():
    import pandas as pd

    # my_data.csv 파일 생성
    my_data = pd.DataFrame(columns=['time', 'lane_id', 'queueing_length'])
    my_data.to_csv('my_data.csv', index=False)
    print("my_data.csv 파일 생성 완료")

def data_rangling():
    import xml.etree.ElementTree as ET
    import pandas as pd

    # my_data.csv 파일 불러오기
    my_data = pd.read_csv('my_data.csv')
    print(my_data)
    print("my_data.csv 파일 불러오기 완료")

    tree = ET.parse('queueinfo.xml')
    print("queueinfo.xml 파일 불러오기 완료")
    print(tree)
    root = tree.getroot()

    # Extract data from XML
    data = []
    for timestep in root.findall('data'):
        time = float(timestep.get('timestep'))
        for lane in timestep.find('lanes').findall('lane'):
            lane_id = lane.get('id')
            queueing_length = float(lane.get('queueing_length'))
            data.append((time, lane_id, queueing_length))

    df = pd.DataFrame(data, columns=['time', 'lane_id', 'queueing_length'])
    df = df[~df['lane_id'].str.startswith('c')]
    # lane_id 가 1c_0, 1c_1, 1c_2, 1c_3, 1c_4 인 행을 1c 로 통일. 이때, 같은 time의 queueing_length 는 해당 time의 각 lane_id 의 queueing_length 의 평균으로 대체
    df['lane_id'] = df['lane_id'].apply(lambda x: x.split('_')[0])
    df = df.groupby(['time', 'lane_id']).mean().reset_index()
    print(df)
    # df를 my_data와 merge
    my_data = pd.concat([my_data, df])

    # my_data.csv 파일로 저장
    my_data.to_csv('my_data.csv', index=False)



# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()
    make_csv()
    # 시뮬레이션 100회 반복
    for i in range(100):
        # this script has been called from the command line. It will start sumo as a
        # server, then connect and run
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        # first, generate the route file for this simulation
        generate_routefile()

        # this is the normal way of using traci. sumo is started as a
        # subprocess and then the python script connects and runs
        # 파일 덮어쓰기로 되어있음
        traci.start([sumoBinary, "-c", "config/cross.sumocfg",
                    "--tripinfo-output", "tripinfo.xml",
                    "--queue-output", "queueinfo.xml",])
                    # "--tripinfo-output", f"tripinfo_{i}.xml",
                    # "--queue-output", f"queueinfo_{i}.xml",])
        run()
