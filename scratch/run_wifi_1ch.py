# Import
from datetime import datetime
import subprocess
import csv
import time
import sys

# Options
num_scenarios = 1           # how many scenarios are simulated
num_seeds = 20              # how many times each scenario is simulated
notes = "6-100-2"           # notes to be written in the .csv file
ns3_script = "wifi_1ch"     # ns3 script to be launched

timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
filebase = "/testfile_" + timestamp
csv_file_py = "." + filebase + '.csv'
csv_file_ns3 = "./scratch" + filebase + '.csv'


def main():
    print "Creating file ", csv_file_py
    print "Simulating", num_scenarios, "scenario(s) with", num_seeds, "seed(s) each\n"
    arg_list = []

    # Prepare all simulation arguments
    for i in range(num_scenarios):
        for j in range(num_seeds):
            args = {
                "simulationTime": 15,
                "seed": j + 1,
                "csvFileName": csv_file_ns3,
                "band": "AX_5",
                "phyModel": "spectrum",
                "constantMcs": 1,
                "channelNumber": 50,
                "channelWidth": 160,
                "mcs": 5,
                "gi": 1600,
                "txPower": 20,
                "nStaA": 6,
                "nStaB": 100,
                "nStaC": 2
            }
            arg_list.append(args)

    # Write metadata to CSV
    with open(csv_file_py, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["scenarios", num_scenarios])
        writer.writerow(["seeds per scenario", num_seeds])
        writer.writerow(["notes", ns3_script + ". " + notes])
        writer.writerow(["arg_list[0]", arg_list[0]])
        writer.writerow(["arg_list[" + str(len(arg_list) - 1) + "]", arg_list[-1]])

    # Run simulations
    for i in range(0, len(arg_list)):
        print "Running simulation", i + 1, "of", len(arg_list)
        start_time = time.time()
        simulate(arg_list[i])
        end_time = time.time()
        print "Completed in %.2f seconds\n" % (end_time - start_time)


def get_arguments(arg):
    atribute_names = [
        " --simulationTime=",
        " --seed=",
        " --csvFileName=",
        " --band=",
        " --phyModel=",
        " --constantMcs=",
        " --channelNumber=",
        " --channelWidth=",
        " --mcs=",
        " --gi=",
        " --txPower=",
        " --nStaA=",
        " --nStaB=",
        " --nStaC="
    ]
    atribute_values = [
        str(arg["simulationTime"]),
        str(arg["seed"]),
        str(arg["csvFileName"]),
        str(arg["band"]),
        str(arg["phyModel"]),
        str(arg["constantMcs"]),
        str(arg["channelNumber"]),
        str(arg["channelWidth"]),
        str(arg["mcs"]),
        str(arg["gi"]),
        str(arg["txPower"]),
        str(arg["nStaA"]),
        str(arg["nStaB"]),
        str(arg["nStaC"])
    ]
    arguments = ""
    for s in range(0, len(atribute_names)):
        arguments += atribute_names[s] + atribute_values[s]
    return arguments


def simulate(arg):
    arguments = get_arguments(arg)
    print "Calling the ns3 script '" + ns3_script + ".cc'"
    subprocess.call('(cd ..; ./waf --run "' + ns3_script + arguments + '")', shell=True)


# Catch CTRL+C cleanly
if __name__ == "__main__":
    try:
        start_time = time.time()
        print "Simulation started!  Time:", datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        main()
        total_time = time.time() - start_time
        print "\nAll simulations finished!"
        print "Total simulation time: %.2f seconds" % total_time
    except KeyboardInterrupt:
        print "\nSimulation interrupted by user. Exiting..."
        sys.exit(0)

