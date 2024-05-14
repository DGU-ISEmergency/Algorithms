import traci as tr

def set_emergency_signal(emergency_edge, duration):
    matching_edges = find_matching_edges(emergency_edge)

    # matching_edges의 신호를 초록불로 변경
    for edge_id in matching_edges:
        set_green_light(edge_id, duration)

    all_edges = tr.edge.getIDList()

    for edge_id in all_edges:
        # matching_edges에 속하지 않는 엣지 빨간불로 변경
        if edge_id not in matching_edges:
            set_red_light(edge_id, duration)

    """ # emergency_edge가 빨간 불인 경우
    if is_red_light(emergency_edge):
        
        # matching_edges의 신호를 초록불로 변경
        for edge_id in matching_edges:
            set_green_light(edge_id, duration)

        all_edges = tr.edge.getIDList()

        for edge_id in all_edges:
            # matching_edges에 속하지 않는 엣지 빨간불로 변경
            if edge_id not in matching_edges:
                set_red_light(edge_id, duration)

    # emergency_edge가 초록불인 경우
    elif is_green_light(emergency_edge):
        for edge_id in matching_edges:
            set_green_light(edge_id, duration)

        all_edges = tr.edge.getIDList()

        for edge_id in all_edges:
            # matching_edges에 속하지 않는 엣지 빨간불로 변경
            if edge_id not in matching_edges:
                set_red_light(edge_id, duration) """


def is_red_light(edge_id):
    # 해당 엣지의 신호등 id
    traffic_light_id = tr.edge.getTrafficLightID(edge_id)

    # 교차로의 신호 상태
    connected_junctions = tr.edge.getConnectedJunctions(edge_id)

    for junction_id in connected_junctions:
        current_state = tr.junction.getRedYellowGreenState(junction_id)

        # 해당 엣지의 신호등 상태가 빨간불인지 확인
        if current_state[traffic_light_id] == "r":
            return True

    return False

def is_green_light(edge_id):
    # 해당 엣지의 신호등 id
    traffic_light_id = tr.edge.getTrafficLightID(edge_id)

    # 교차로의 신호 상태
    connected_junctions = tr.edge.getConnectedJunctions(edge_id)

    for junction_id in connected_junctions:
        current_state = tr.junction.getRedYellowGreenState(junction_id)

        # 해당 엣지의 신호등 상태가 초록불인지 확인
        if current_state[traffic_light_id] == "g":
            return True

    return False

# setPhase로 해보기
def set_green_light(edge_id, duration):
    tr.edge.setParameter(edgeID=edge_id, param="tl", value="G" * duration) # tl: traffic light
    tr.simulation.setParameter(simulation="time-to-teleport", value=duration)

def set_red_light(edge_id, duration):
    tr.edge.setParameter(edgeID=edge_id, param="tl", value="r" * duration)
    tr.simulation.setParameter(simulation="time-to-teleport", value=duration)

def find_matching_edges(emergency_edge):
    matching_edges = []

    all_edges = tr.edge.getIDList()

    for edge_id in all_edges:
        if is_green_light(edge_id) == is_green_light(emergency_edge):
            matching_edges.append(edge_id)

    return matching_edges