import sys
from collections import deque

def fcfs(processes):
    # TODO: Implement First Come First Serve scheduling algorithm
    pass

def sjf(processes):
    # TODO: Implement Shortest Job First scheduling algorithm
    pass

def round_robin(processes, quantum):
    print("Using Round-Robin")
    active_process = None
    current_q = 0
    finished_processes = []
    queue = deque()

    for i in range(runfor):
        # Handle process arrivals
        while processes and processes[0]['arrival'] == i:
            queue.append(processes.pop(0))
            print(f"Time {i:3d} : {queue[-1]['name']} arrived")

        if queue and not active_process:
            active_process = queue.popleft()
            current_q = quantum
            active_process['has_run'] = True
            print(f"Time {i:3d} : {active_process['name']} selected (burst {active_process['burst']})")

        if not active_process:
            print(f"Time {i:3d} : Idle")
            continue

        active_process['burst'] -= 1
        current_q -= 1

        for process in queue:
            process['wait'] += 1
            if not process['has_run']:
                process['response'] += 1

        if active_process['burst'] == 0:
            turnaround_time = i - active_process['arrival']
            active_process['turnaround'] = turnaround_time
            finished_processes.append(active_process)
            print(f"Time {i:3d} : {active_process['name']} finished")
            active_process = None
        elif current_q == 0:
            queue.append(active_process)
            active_process = None

    print(f"Finished at time {runfor}\n")
    return finished_processes

def print_results(processes):
    for process in processes:
        print(f"{process['name']} wait {process['wait']} turnaround {process['turnaround']} response {process['response']}")

# Read file name from command line argument
if len(sys.argv) != 2:
    print("Error: Please provide the input file name.")
    sys.exit(1)

file_name = sys.argv[1]

# Read and parse input file
with open(file_name, 'r') as file:
    directives = {}
    processes = []

    for line in file:
        line = line.split('#')[0].strip()  # Ignore comments
        if line:
            parts = line.split()
            directive = parts[0]
            if directive == 'end':
                break

            if directive == 'process':
                processes.append({'name': parts[2], 'arrival': int(parts[4]), 'burst': int(parts[6]),
                                  'wait': 0, 'turnaround': 0, 'response': 0, 'has_run': False})
            else:
                directives[directive] = parts[1]

# Check for missing parameters
required_directives = ['processcount', 'runfor', 'use']
if any(directive not in directives for directive in required_directives):
    print("Error: Missing parameter(s)")
    sys.exit(1)

process_count = int(directives['processcount'])
runfor = int(directives['runfor'])
use_algorithm = directives['use']

if use_algorithm == 'rr':
    if 'quantum' not in directives:
        print("Error: Missing quantum parameter when use is 'rr'")
        sys.exit(1)
    quantum = int(directives['quantum'])

print(f"processes: {process_count}")

# Sort processes by arrival time
processes.sort(key=lambda x: x['arrival'])

# Execute scheduling algorithm
if use_algorithm == 'fcfs':
    fcfs(processes)
elif use_algorithm == 'sjf':
    sjf(processes)
elif use_algorithm == 'rr':
    results = round_robin(processes, quantum)
    print_results(results)
else:
    print("Error: Invalid scheduling algorithm")
    sys.exit(1)