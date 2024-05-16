import traci as tr

def set_emergency_signal(tls_id, duration):
    # matching_edges = find_matching_edges(emergency_edge)

    if is_green_light(tls_id):
        remain_time = tr.trafficlight.getPhaseDuration(tls_id) - tr.trafficlight.getSpentDuration(tls_id)

        if remain_time < duration:
            tr.trafficlight.setPhaseDuration(tls_id, duration)
        else:
            pass

    else:
        tr.trafficlight.setPhase(tls_id, 0)
        tr.trafficlight.setPhaseDuration(tls_id, duration)

# tls_id = 0으로 고정
def is_green_light(tls_id):
    if tr.trafficlight.getPhase(tls_id) == 0:
            return True

    return False

def set_green_light(tls_id, duration):
    tr.trafficlight.setPhaseDuration(tls_id, duration)

""" def find_matching_edges(emergency_edge):
    matching_edges = []

    all_edges = tr.edge.getIDList()

    for edge_id in all_edges:
        if is_green_light(edge_id) == is_green_light(emergency_edge):
            matching_edges.append(edge_id)

    return matching_edges """