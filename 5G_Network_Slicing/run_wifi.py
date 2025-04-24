

# Import
from datetime import datetime
import subprocess
import csv

# Options
num_scenarios = 1           # how many scenarios are simulated
num_seeds = 20              # how many times each scenario is simulated
notes = "6-100-2"           # notes to be written in the .csv file
simulation_time = 15        # seconds
ns3_script = "wifi"         # ns3 script to be launched
band = "AX_5"               # AC_5, AX_2.4 or AX_5
phy_model = "spectrum"      # "spectrum" or "yans"
constant_mcs = 1            # 0 Minstrel or 1 constant

timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
filebase = "/testfile_" + timestamp
csv_file_py = "." + filebase + '.csv'
csv_file_ns3 = "./scratch" + filebase + '.csv'


def main():
    print("Creating file ", csv_file_py)  # Changed to Python 3 print function
    print("Simulating", num_scenarios, "scenario(s) with", num_seeds, "seed(s) each")
    print()
    arg_list = []
    for i in range(num_scenarios):
        for j in range(num_seeds):
            args = {}
            args["simulationTime"] = simulation_time
            args["seed"] = j + 1
            args["csvFileName"] = csv_file_ns3
            args["band"] = band
            args["phyModel"] = phy_model
            args["constantMcs"] = constant_mcs
            # Add other arguments as needed
            arg_list.append(args)
    
    # Write simulation parameters to CSV
    with open(csv_file_py, 'w', newline='') as file:  # Added newline='' for proper CSV writing
        writer = csv.writer(file)
        writer.writerow(["scenarios", num_scenarios])
        writer.writerow(["seeds per scenario", num_seeds])
        writer.writerow(["notes", ns3_script + ". " + notes])
        writer.writerow(["arg_list[0]", str(arg_list[0])])  # Convert dict to string
        writer.writerow(["arg_list[" + str(len(arg_list)-1) + "]", str(arg_list[len(arg_list)-1])])  # Convert dict to string
    
    # Run simulations
    for i, args in enumerate(arg_list):  # More pythonic iteration
        print(f"Running simulation {i+1} of {len(arg_list)}")  # Added progress indicator
        simulate(args)
        print()


def get_arguments(arg):
    attribute_names = [  # Fixed typo in variable name (was 'atribute_names')
        " --simulationTime=",
        " --seed=",
        " --csvFileName=",
        " --band=",
        " --phyModel=",
        " --constantMcs=",
        # Add other attribute names as needed
    ]
    attribute_values = [  # Fixed typo in variable name (was 'atribute_values')
        str(arg["simulationTime"]),
        str(arg["seed"]),
        str(arg["csvFileName"]),
        str(arg["band"]),
        str(arg["phyModel"]),
        str(arg["constantMcs"]),
        # Add other attribute values as needed
    ]
    
    # Validate equal length of names and values
    if len(attribute_names) != len(attribute_values):
        raise ValueError("Attribute names and values must have the same length")
    
    arguments = ""
    for name, value in zip(attribute_names, attribute_values):  # More pythonic iteration
        arguments += name + value
    return arguments


def simulate(arg):
    arguments = get_arguments(arg)
    print("Calling the ns3 script '" + ns3_script + ".cc'")
    try:
        subprocess.run(['cd ..; ./waf --run "' + ns3_script + arguments + '"'],  # Changed to subprocess.run
                      shell=True, 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running simulation: {e}")


if __name__ == "__main__":
    main()
