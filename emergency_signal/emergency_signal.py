import traci as tr

def set_emergency_vehicle_signal(emergency_edge, duration):
    set_green_light_duration(emergency_edge, duration)

    all_edges = tr.edge.getIDList()

    for edge_id in all_edges:
        if edge_id != emergency_edge:
            set_red_light(edge_id, duration)

# edge_id: emergency edge
def set_green_light_duration(edge_id, duration):
    connected_junctions = tr.edge.getConnectedJunctions(edge_id)

    for junction_id in connected_junctions:
        current_program = tr.junction.getParameter(junctionID=junction_id, parameter='program')

        if is_green_light(current_program):
            modified_program = modify_program_for_duration(current_program, duration)
        else:
            modified_program = change_to_green_light(current_program, duration)

        tr.junction.setParameter(junctionID=junction_id, parameter='program', value=modified_program)

# edge_id: emergency edge
def is_green_light(edge_id):
    connected_junctions = tr.edge.getConnectedJunctions(edge_id)

    for junction_id in connected_junctions:
        current_state = tr.junction.getRedYellowGreenState(junction_id)

        if current_state[edge_id] == "g":
            return True

    return False

def modify_program_for_duration(current_program, duration):
    modified_program = ""

    for phase in current_program:
        if phase == "G":
            modified_program += "G" * duration

    return modified_program

def change_to_green_light(emergency_edge, duration):
    tr.edge.setParameter(edgeID=emergency_edge, param="tl", value="G")

    # duration 이후 traffic light가 원래 상태로 돌아감
    tr.simulation.setParameter(simulation="time-to-teleport", value=duration)

def set_red_light(edge_id, duration):
    tr.edge.setParameter(edgeID=edge_id, param="tl", value="r") # tl: traffic light

    tr.simulation.setParameter(simulation="time-to-teleport", value=duration)