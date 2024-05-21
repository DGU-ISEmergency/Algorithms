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
    N = 3600  # number of time steps

    # 1분당 교통량 데이터
    traffic_volume_per_minute = {
        "WE": 100,
        "EW": 120,
        "NS": 80,
        "SN": 90,
        "LT1": 40,
        "LT2": 50,
        "Eme": 1,
        "RT1": 30,
        "RT2": 25,
        "RT3": 20,
        "RT4": 15,
        "UT1": 10,
        "UT2": 10,
    }

    # 1초당 교통량 데이터로 변환 (Poisson 분포의 λ)
    traffic_lambda_per_second = {k: v / 60 for k, v in traffic_volume_per_minute.items()}

    lanes = ["0", "1", "2", "3", "4"]

    with open("config/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="passenger" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2" maxSpeed="16.67" guiShape="passenger"/>
        <vType id="emergency" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="emergency"/>

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
            for direction, lambda_val in traffic_lambda_per_second.items():
                num_vehicles = np.random.poisson(lambda_val)
                for _ in range(num_vehicles):
                    lane = random.choice(lanes)
                    if direction in ["WE", "EW", "NS", "SN"]:
                        route = {"WE": "right", "EW": "left", "NS": "down", "SN": "up"}[direction]
                        if direction == "EW" and random.uniform(0, 1) < traffic_lambda_per_second["Eme"]:
                            print('    <vehicle id="emergency_%i" type="emergency" route="%s" depart="%i" departLane="%s" />' % (
                                vehNr, route, i, lane), file=routes)
                        else:
                            print('    <vehicle id="%s_%i" type="passenger" route="%s" depart="%i" departLane="%s" />' % (
                                route, vehNr, route, i, lane), file=routes)
                    elif direction.startswith("LT"):
                        route = "leftTurn" + direction[-1]
                        print('    <vehicle id="%s_%i" type="passenger" route="%s" depart="%i" departLane="%s" />' % (
                            route, vehNr, route, i, lane), file=routes)
                    elif direction.startswith("RT"):
                        route = "rightTurn" + direction[-1]
                        print('    <vehicle id="%s_%i" type="passenger" route="%s" depart="%i" departLane="%s" />' % (
                            route, vehNr, route, i, lane), file=routes)
                    elif direction.startswith("UT"):
                        route = "uTurn" + direction[-1]
                        print('    <vehicle id="%s_%i" type="passenger" route="%s" depart="%i" departLane="%s" />' % (
                            route, vehNr, route, i, lane), file=routes)
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

def signal_change(edge_id, lane_id, loop_id):
    tls_id = "c" # 교차로 신호 id
    veh_id = ed.get_detected_vehicle_ids(loop_id)[0] # 차량 id -> 왜 0번 인덱스인지 다시 설명 필요(이해못함ㅇㅅㅇ;;)
    # 긴급차량인지 확인
    if "emergency" in veh_id:
        # 요구 녹색시간 계산
        duration = gt.green_time(lane_id, veh_id, edge_id)
        print(f"응급차량 감지, {duration} steps 동안 신호변경")
        # 신호 변경
        es.set_emergency_signal(tls_id, duration)
        
# 신호 관련
def run():
    """execute the TraCI control loop"""
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        loop = ["0", "1", "2", "3", "4"]
        edge_id = "4c"

        # 모든 디텍터 사용해서 긴급차량 감지
        for loop_id in loop:
            lane_id = f"{edge_id}_{loop_id}"
            # 모든 차량 id를 반환하는 거였네..
            if traci.inductionloop.getLastStepVehicleIDs(loop_id):
                signal_change(edge_id, lane_id, loop_id)

        step += 1
    
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    # options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    # if options.nogui:
    #     sumoBinary = checkBinary('sumo')
    # else:
    sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    generate_routefile()

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "config/cross.sumocfg"])

                            # tripinfo xml 로 output 추출하는 코드
                            #  "--tripinfo-output", "tripinfo.xml"]) 
    run()
