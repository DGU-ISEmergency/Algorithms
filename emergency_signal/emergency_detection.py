import traci as tr

# edge_id: emergency edge
def emergency_detection(edge_id):
    # 해당 엣지의 모든 차량 ID
    vehicle_ids = tr.edge.getLastStepVehicleIDs(edge_id)

    # 각 차량의 ID를 사용하여 차량이 긴급차량인지 확인
    for vehicle_id in vehicle_ids:
        vehicle_type = tr.vehicle.getTypeID(vehicle_id)

        if vehicle_type == "emergency": # 이 부분은 설정한 id로 변경해줘
            lane_id = tr.vehicle.getLaneID(vehicle_id)
            print(f"긴급차량 진입 {lane_id}: {vehicle_id}")

            return lane_id

    return None