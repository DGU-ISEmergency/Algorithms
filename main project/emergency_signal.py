import traci as tr
import emergency_detection as ed
import green_time as gt
import vehicle_info as vi

# 다음 phase가(0 -> 1) 아닌 원래 phase로(e.g. 3) 돌아가도록 해보기
# why? 그래야 더 정체될 것
def set_emergency_signal(tls_id, duration):
    if is_green_light(tls_id):
        remain_time = tr.trafficlight.getPhaseDuration(tls_id) - tr.trafficlight.getSpentDuration(tls_id)

        if remain_time < duration:
            set_duration(tls_id, duration)

    else:
        tr.trafficlight.setPhase(tls_id, 0)
        set_duration(tls_id, duration)

def is_green_light(tls_id):
    if tr.trafficlight.getPhase(tls_id) == 0:
            return True

    return False

def set_duration(tls_id, duration):
    tr.trafficlight.setPhaseDuration(tls_id, duration)

def signal_change(edge_id, lane_id, loop_id, processed_emergency_vehicles):
    tls_id = "c" # 교차로 신호 id
    veh_id = ed.get_detected_vehicle_ids(loop_id)[0]

    # 긴급차량인지 확인
    if "emergency" in veh_id:
        # 이미 처리된 긴급차량인지 확인
        if veh_id in processed_emergency_vehicles:
            print(f"이미 처리된 긴급차량: {veh_id}")
            return None
        
        # 처리된 긴급차량 목록에 추가
        processed_emergency_vehicles.add(veh_id)
        
        # 긴급차량 감지 됐을 때만 회피 로직 가능 -> 처음부터 가능하도록 변경
        eme_info = vi.get_vehicle_info(veh_id)

        # 요구 녹색시간 계산
        duration = gt.green_time(lane_id, veh_id, edge_id)
        print(f"응급차량 감지, {duration} steps 동안 신호변경")
        
        # 신호 변경
        set_emergency_signal(tls_id, duration)
        
        return eme_info, duration
    
    return None, 0