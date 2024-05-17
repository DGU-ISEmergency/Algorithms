import traci as tr

def get_detected_vehicle_ids(loop_id):
    vehicle_ids = tr.inductionloop.getLastStepVehicleIDs(loop_id)
    return vehicle_ids