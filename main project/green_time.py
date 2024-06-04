import traci as tr

def green_time(lane_id, veh_id, edge_id):
    # 대기 차량 소거시간 계산
    qc = tr.edge.getLastStepHaltingNumber(edge_id) / (tr.edge.getLaneNumber(edge_id) - 1) * 2

    # 긴급차량 통과시간 계산
    print("=============================================")
    print(f"긴급차량 속도: {tr.vehicle.getSpeed(veh_id)}")
    print(f"edge_id: {edge_id}")
    print(f"lane_id: {lane_id}")
    print(f"대기 차량 수 : {tr.edge.getLastStepHaltingNumber(edge_id)}")
    print(f"차선 수: {tr.edge.getLaneNumber(edge_id)}")
    print(f"차선 길이: {tr.lane.getLength(lane_id)}")
    print(f"qc: {qc}")
    t = (tr.lane.getLength(lane_id) - (qc * tr.vehicle.getSpeed(veh_id))) / max(tr.vehicle.getSpeed(veh_id), 1)
    g = qc + t
    print(f"g: {g}")
    print("=============================================")

    return g