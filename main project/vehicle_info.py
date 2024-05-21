import traci as tr

def get_vehicle_info(veh_id):
    x, y = tr.vehicle.getPosition(veh_id)
    speed = tr.vehicle.getSpeed(veh_id)
    lane_id = tr.vehicle.getLaneIndex(veh_id)
    lane_pos = tr.vehicle.getLanePosition(veh_id)

    return (veh_id, x, y, speed, lane_id, lane_pos)