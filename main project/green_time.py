import traci as tr

def green_time(lane_id, veh_id, edge_id):
    # 긴급차량 통과시간 계산
    t = (tr.lane.getLength(lane_id) - (qc * tr.vehicle.getSpeed(veh_id))) / max(tr.vehicle.getSpeed(veh_id), 1)
    
    # 대기 차량 소거시간 계산
    qc = tr.edge.getLastStepHaltingNumber(edge_id) / (tr.edge.getLaneNumber(edge_id) - 1) * 2
    g = qc + t

    return g