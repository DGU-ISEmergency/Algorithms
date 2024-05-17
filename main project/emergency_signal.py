import traci as tr

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