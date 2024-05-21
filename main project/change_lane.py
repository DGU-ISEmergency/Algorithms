import traci as tr
import vehicle_info as vi

def change(veh_list, eme_info, lcmode, lctime, detect_range):
    for veh_id in veh_list:
        res = vi.get_vehicle_info(veh_id)
        tr.vehicle.setLaneChangeMode(veh_id, lcmode)

        # 긴급 차량과의 거리, 같은 차선 확인
        if (0 < res[5] - eme_info[5] < detect_range) and res[4] == eme_info[4] and res[3] > 3:
            # 차선 변경 가능 여부 확인
            lcsl = tr.vehicle.couldChangeLane(veh_id, 1)  # 왼쪽 차선 변경 가능 여부
            lcsr = tr.vehicle.couldChangeLane(veh_id, -1)  # 오른쪽 차선 변경 가능 여부
            
            if lcsl:
                tr.vehicle.changeLaneRelative(veh_id, 1, lctime)
                print(f"vid:{veh_id}, change left")
            elif lcsr:
                tr.vehicle.changeLaneRelative(veh_id, -1, lctime)
                print(f"vid:{veh_id}, change right")
        
        # 긴급 차량과의 거리 확인
        elif (0 < res[5] - eme_info[5] < detect_range) and res[3] > 3:
            if res[4] - eme_info[4] > 0:  # 왼쪽 차선으로 변경
                tr.vehicle.changeLaneRelative(veh_id, 1, lctime)
                print(f"vid:{veh_id}, change left")
            elif res[4] - eme_info[4] < 0:  # 오른쪽 차선으로 변경
                tr.vehicle.changeLaneRelative(veh_id, -1, lctime)
                print(f"vid:{veh_id}, change right")

def get_small_lane(lane_ids):
    min_queue_length = float('inf')
    best_lane_id = None

    for lane_id in lane_ids:
        queue_length = tr.lane.getLastStepVehicleNumber(lane_id)
    
        if queue_length < min_queue_length:
            min_queue_length = queue_length
            best_lane_id = lane_id

    return best_lane_id

# 긴급차량이 대기행렬 짧은 차선으로 이동
def change_small_lane(eme_info, lctime):
    lane_ids = ["4c_0", "4c_1", "4c_2", "4c_3", "4c_4"]
    best_lane_id = get_small_lane(lane_ids)

    if best_lane_id != eme_info[4]:
        best_lane_index = lane_ids.index(best_lane_id)
        tr.vehicle.changeLane(eme_info[0], best_lane_index, lctime)
        print(f"vid:{eme_info[0]}, change lane")
        
    elif best_lane_id == None:
        pass
