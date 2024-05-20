from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

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

    # 태경이가 준 교통량 넣으면 될듯
    pWE = 1. / 10
    pEW = 1. / 10
    pNS = 1. / 10
    pSN = 1. / 10
    pLT1 = 1. / 10
    pLT2 = 1. / 10
    pEme = 1. / 3
    pRT1 = 1. / 10
    pRT2 = 1. / 10
    pRT3 = 1. / 10
    pRT4 = 1. / 10
    pUT1 = 1. / 10
    pUT2 = 1. / 10

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
            if random.uniform(0, 1) < pUT1:
                lane = random.choice(lanes)
                print('    <vehicle id="uTurn1_%i" type="passenger" route="uTurn1" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pUT2:
                lane = random.choice(lanes)
                print('    <vehicle id="uTurn2_%i" type="passenger" route="uTurn2" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWE:
                lane = random.choice(lanes)
                print('    <vehicle id="right_%i" type="passenger" route="right" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                lane = random.choice(lanes)
                if random.uniform(0, 1) < pEme:
                    print('    <vehicle id="emergency_%i" type="emergency" route="left" depart="%i" departLane="%s" />' % (
                        vehNr, i, lane), file=routes)
                else:
                    print('    <vehicle id="left_%i" type="passenger" route="left" depart="%i" departLane="%s" />' % (
                        vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                lane = random.choice(lanes)
                print('    <vehicle id="right_%i" type="passenger" route="down" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSN:
                lane = random.choice(lanes)
                print('    <vehicle id="right_%i" type="passenger" route="up" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pLT1:
                lane = random.choice(lanes)
                print('    <vehicle id="leftTurn1_%i" type="passenger" route="leftTurn1" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pLT2:
                lane = random.choice(lanes)
                print('    <vehicle id="leftTurn2_%i" type="passenger" route="leftTurn2" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pRT1:
                lane = random.choice(lanes)
                print('    <vehicle id="rightTurn1_%i" type="passenger" route="rightTurn1" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pRT2:
                lane = random.choice(lanes)
                print('    <vehicle id="rightTurn2_%i" type="passenger" route="rightTurn2" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pRT3:
                lane = random.choice(lanes)
                print('    <vehicle id="rightTurn3_%i" type="passenger" route="rightTurn3" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pRT4:
                lane = random.choice(lanes)
                print('    <vehicle id="rightTurn4_%i" type="passenger" route="rightTurn4" depart="%i" departLane="%s" />' % (
                    vehNr, i, lane), file=routes)
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

def signal_change(edge_id, lane_id, loop_id, tls_id = "c"):
    # 긴급차량 id
    veh_id = ed.get_detected_vehicle_ids(loop_id)[0]
    if "emergency" in veh_id:
        # 요구 녹색시간 계산
        duration = gt.green_time(lane_id, veh_id, edge_id)
        print(f"응급차량 감지, {duration} steps 동안 신호변경")
        # 신호 변경
        es.set_emergency_signal(tls_id, duration)
        # break # 긴급차량 하나만 처리하고 중단
# 신호 관련
def run():
    """execute the TraCI control loop"""
    step = 0

    # 긴급차량 등장 edge, lane 설정
    tls_id = "c" # 교차로 신호 id

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # 디텍터 사용해서 모든차량 감지
        if traci.inductionloop.getLastStepVehicleIDs("0"):
            loop_id = "0"
            edge_id = "4c"
            lane_id = "4c_0"

            signal_change(edge_id, lane_id, loop_id)

        elif traci.inductionloop.getLastStepVehicleIDs("1"):
            loop_id = "1"
            edge_id = "4c"
            lane_id = "4c_1"

            signal_change(edge_id, lane_id, loop_id)

        elif traci.inductionloop.getLastStepVehicleIDs("2"):
            loop_id = "2"
            edge_id = "4c"
            lane_id = "4c_2"

            signal_change(edge_id, lane_id, loop_id)

        elif traci.inductionloop.getLastStepVehicleNumber("3"):
            loop_id = "3"
            edge_id = "4c"
            lane_id = "4c_3"

            signal_change(edge_id, lane_id, loop_id)

        elif traci.inductionloop.getLastStepVehicleNumber("4"):
            loop_id = "4"
            edge_id = "4c"
            lane_id = "4c_4"

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
