from sumolib import checkBinary
import traci

sumoBinary = checkBinary('sumo-gui')

RED = [255, 0, 0]
EDGE_ID = 'closed'
VEHICLES = ['1', '4', '8']


def main():
    startSim()

    while shouldContinueSim():
        for vehId in getOurDeparted(VEHICLES):
            setVehColor(vehId, RED)
            avoidEdge(vehId, EDGE_ID)

        traci.simulationStep()

    traci.close()


def startSim():
    """Starts the simulation."""
    traci.start(
        [
            sumoBinary,
            '--net-file', './config/network.net.xml',
            '--route-files', './config/trips.trips.xml',
            '--delay', '200',
            '--gui-settings-file', './config/viewSettings.xml',
            '--start'

        ])


def shouldContinueSim():
    """Checks that the simulation should continue running.

    Returns:
        bool: `True` if vehicles exist on network. `False` otherwise.
    """
    numVehicles = traci.simulation.getMinExpectedNumber()
    return True if numVehicles > 0 else False


def setVehColor(vehId, color):
    """Changes a vehicle's color.

    Args:
        vehId (String): The vehicle to color.
        color ([Int, Int, Int]): The RGB color to apply.
    """
    traci.vehicle.setColor(vehId, color)


def avoidEdge(vehId, edgeId):
    """Sets an edge's travel time for a vehicle infinitely high, and reroutes the vehicle based on travel time.

    Args:
        vehId (Str): The ID of the vehicle to reroute.
        edgeId (Str): The ID of the edge to avoid.
    """
    traci.vehicle.setAdaptedTraveltime(
        vehId, edgeId, float('inf'))
    traci.vehicle.rerouteTraveltime(vehId)


def getOurDeparted(filterIds=[]):
    """Returns a set of filtered vehicle IDs that departed onto the network during this simulation step.

    Args:
        filterIds ([String]): The set of vehicle IDs to filter for.

    Returns:
        [String]: A set of vehicle IDs.
    """
    newlyDepartedIds = traci.simulation.getDepartedIDList()
    filteredDepartedIds = newlyDepartedIds if len(
        filterIds) == 0 else set(newlyDepartedIds).intersection(filterIds)
    return filteredDepartedIds


if __name__ == "__main__":
    main()