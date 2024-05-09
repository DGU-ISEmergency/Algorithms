import traci as tr
import emergency_signal as es
import emergency_detection as ed
import green_time as gt

# 수모 시뮬 시작하는 코드

edge_id = 'eme_edge' # 실제 긴급차량 진입하는 엣지로 변경해야됨
lane_id = ed.emergency_detection(edge_id)
veh_id = 'emergency' # 실제 긴급차량 id로 변경해야됨
traffic_light_id = 'tl0' # 예시로 설정한거라 변경해야됨

if lane_id:
    duration = gt.green_time(lane_id, veh_id, edge_id)

    # 임시 신호 변경
    tr.trafficlights.setRedYellowGreenState(traffic_light_id, "G")
    tr.simulationStep(duration)
    tr.trafficlights.setRedYellowGreenState(traffic_light_id, "r")