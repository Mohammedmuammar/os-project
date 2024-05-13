import heapq

class Process:
    def __init__(self, pid, arrival_time, cpu_burst, size):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.remaining_time = cpu_burst
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0
        self.size = size
        self.executed = False

class GanttChart:
    def __init__(self, pid, start_time, end_time):
        self.pid = pid
        self.start_time = start_time
        self.end_time = end_time

def main():
    processes = []
    with open("input.txt", "r") as inputFile:
        context_switch, quantum = map(int, inputFile.readline().split())
        for line in inputFile:
            id, arrivalTime, burstTime, size = map(int, line.split())
            process = Process(id, arrivalTime, burstTime, size)
            processes.append(process)
    numProcesses = len(processes)


    processes.sort(key=lambda x: x.arrival_time)

    # First Come First Serve (FCFS)
    current_time = 0
    fcfs_gantt_chart = []
    for process in processes:
        if process.arrival_time > current_time:
            current_time = process.arrival_time
        process.start_time = current_time
        current_time += process.cpu_burst + context_switch
        process.finish_time = current_time
        process.waiting_time = process.start_time - process.arrival_time
        process.turnaround_time = process.finish_time - process.arrival_time
        fcfs_gantt_chart.append(GanttChart(process.pid, process.start_time, process.finish_time))

    fcfs_average_waiting_time = sum(process.waiting_time for process in processes) / numProcesses
    fcfs_average_turnaround_time = sum(process.turnaround_time for process in processes) / numProcesses
    fcfs_cpu_utilization = sum(process.cpu_burst for process in processes) / current_time

    # Shortest Job First (SJF)
    current_time = 0
    sjf_gantt_chart = []
    sjf_ready_queue = []
    sjf_index = 0
    while sjf_ready_queue or sjf_index < numProcesses:
        if not sjf_ready_queue:
            heapq.heappush(sjf_ready_queue, (processes[sjf_index].cpu_burst, sjf_index))
            current_time = processes[sjf_index].arrival_time
            sjf_index += 1
        else:
            cpu_burst, index = heapq.heappop(sjf_ready_queue)
            process = processes[index]
            process.start_time = current_time
            current_time += process.cpu_burst + context_switch
            process.finish_time = current_time
            process.waiting_time = process.start_time - process.arrival_time
            process.turnaround_time = process.finish_time - process.arrival_time
            sjf_gantt_chart.append(GanttChart(process.pid, process.start_time, process.finish_time))
            while sjf_index < numProcesses and processes[sjf_index].arrival_time <= current_time:
                heapq.heappush(sjf_ready_queue, (processes[sjf_index].cpu_burst, sjf_index))
                sjf_index += 1

    sjf_average_waiting_time = sum(process.waiting_time for process in processes) / numProcesses
    sjf_average_turnaround_time = sum(process.turnaround_time for process in processes) / numProcesses
    sjf_cpu_utilization = sum(process.cpu_burst for process in processes) / current_time

    # Round Robin (RR)
    current_time = 0
    rr_gantt_chart = []
    rr_ready_queue = []
    rr_quantum_counter = 0
    rr_index = 0
    for i in range(numProcesses):
        while rr_ready_queue or rr_index < numProcesses:
            if not rr_ready_queue:
                rr_ready_queue.append(processes[rr_index])
                current_time = rr_ready_queue[0].arrival_time
                rr_index += 1
            else:
                process = rr_ready_queue.pop(0)
                if not process.executed:
                    process.response_time = current_time - process.arrival_time
                    process.executed = True
                process.start_time = current_time
                run_time = min(process.remaining_time, quantum)
                current_time += run_time + context_switch
                process.remaining_time -= run_time
                rr_quantum_counter += run_time
                rr_gantt_chart.append(GanttChart(process.pid, process.start_time, current_time))
                while rr_index < numProcesses and processes[rr_index].arrival_time <= current_time:
                    rr_ready_queue.append(processes[rr_index])
                    rr_index += 1
                if process.remaining_time > 0:
                    rr_ready_queue.append(process)
                else:
                    process.finish_time = current_time
                    process.waiting_time = process.start_time - process.arrival_time
                    process.turnaround_time = process.finish_time - process.arrival_time
                if rr_quantum_counter >= quantum:
                    rr_quantum_counter = 0
                    if rr_ready_queue:
                        rr_ready_queue.append(rr_ready_queue.pop(0))

    rr_average_waiting_time = sum(process.waiting_time for process in processes) / numProcesses
    rr_average_turnaround_time = sum(process.turnaround_time for process in processes) / numProcesses
    rr_average_response_time = sum(process.response_time for process in processes) / numProcesses
    rr_cpu_utilization = sum(process.cpu_burst for process in processes) / current_time

    # Print results
    print("First Come First Serve (FCFS):")
    print("Gantt Chart:")
    for process in fcfs_gantt_chart:
        print(f"PID: {process.pid}, Start Time: {process.start_time}, End Time: {process.end_time}")
    print("Finish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.finish_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    print(f"Average Waiting Time = {fcfs_average_waiting_time}")
    print(f"Average Turnaround Time = {fcfs_average_turnaround_time}")
    print(f"CPU Utilization = {fcfs_cpu_utilization}\n")

    print("Shortest Job First (SJF) (non-preemptive):")
    print("Gantt Chart:")
    for process in sjf_gantt_chart:
        print(f"PID: {process.pid}, Start Time: {process.start_time}, End Time: {process.end_time}")
    print("Finish Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        print(f"{process.finish_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    print(f"Average Waiting Time = {sjf_average_waiting_time}")
    print(f"Average Turnaround Time = {sjf_average_turnaround_time}")
    print(f"CPU Utilization = {sjf_cpu_utilization}\n")

    print(f"Round Robin (RR) with quantum {quantum}:")
    print("Gantt Chart:")
    for process in rr_gantt_chart:
        print(f"PID: {process.pid}, Start Time: {process.start_time}, End Time: {process.end_time}")
    print("Finish Time\tWaiting Time\tTurnaround Time\tResponse Time")
    for process in processes:
        print(f"{process.finish_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}\t\t{process.response_time}")
    print(f"Average Waiting Time = {rr_average_waiting_time}")
    print(f"Average Turnaround Time = {rr_average_turnaround_time}")
    print(f"Average Response Time = {rr_average_response_time}")
    print(f"CPU Utilization = {rr_cpu_utilization}")

if __name__ == "__main__":
    main()
