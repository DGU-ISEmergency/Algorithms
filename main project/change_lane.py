import traci as tr
import vehicle_info as vi

def change(veh_list, eme_info, lcmode, lctime, detect_range):
    for veh_id in veh_list:
        res = vi.get_vehicle_info(veh_id)
        tr.vehicle.setLaneChangeMode(veh_id, lcmode)

        # 긴급 차량과의 거리, 같은 차선 확인
        if (0 < res[5] - eme_info[5] < detect_range) and res[4] == eme_info[4] and res[2] > 3:
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
        elif (0 < res[5] - eme_info[5] < detect_range) and res[2] > 3:
            if res[4] - eme_info[4] > 0:  # 왼쪽 차선으로 변경
                tr.vehicle.changeLaneRelative(veh_id, 1, lctime)
            elif res[4] - eme_info[4] < 0:  # 오른쪽 차선으로 변경
                tr.vehicle.changeLaneRelative(veh_id, -1, lctime)