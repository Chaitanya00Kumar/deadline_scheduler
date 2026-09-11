from datetime import datetime, timedelta
CAP = 120
SPREAD = 2
# 1. Work time blocks (your free time)
work_blocks = [
    (datetime(2026,8,14,16,30), datetime(2026,8,14,19,0)),   # 4:30pm-7pm
    (datetime(2026,8,14,21,0), datetime(2026,8,14,22,0)),   # 9pm-10pm
]

# 2. Tasks: (name, duration_in_minutes, deadline)
tasks = [
    ("Physics homework", 60, datetime(2026,8,15,9,0)),
    ("Essay draft", 120, datetime(2026,8,16,9,0)),
    ("Read chapter 3", 45, datetime(2026,8,14,23,0)),
]

sorted_tasks = sorted(tasks, key= lambda task: task[2])

for i in sorted_tasks:
    print(i[0], i[2])

work_periods = []

for i in work_blocks:
    work_periods.append(((i[0]-i[1]).total_seconds()/60)*(-1))

def considerate_sort(o_tasks, CAP, SPREAD):
    tasks = []
    for i in o_tasks:
        tasks.append(i)
    i = 0
    while i != len(tasks):
        if tasks[i][1] > CAP:
            tasks.insert(i+1, (tasks[i][0], CAP, tasks[i][2]))
            tasks.insert(i+2+SPREAD, (tasks[i][0], tasks[i][1]-120, tasks[i][2]))
            tasks.pop(i)

        else:
            pass

        i += 1

    return tasks

def nest_tasks(work_blocks, tasks):
    dupe_workblocks = []
    overflows = []
    for i in work_blocks:
        dupe_workblocks.append(list(i))
    nest = {}
    j = 0
    i = 0
    while j != len(tasks): 
        while i != len(dupe_workblocks):
            if (((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1)) >= tasks[j][1]:
                nest[(tasks[j][0], tasks[j][1]) ] = (dupe_workblocks[i][0], dupe_workblocks[i][0]+ timedelta(minutes = tasks[j][1]))
                dupe_workblocks[i][0] += timedelta(minutes = tasks[j][1])
                j += 1
                break

            elif (((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1)) == 0 and i == len(dupe_workblocks)-1:
                    overflows.append(tasks[j])
                    j += 1
                    break

            elif (((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1)) < tasks[j][1]:
                if ((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1) != 0:
                    tasks.insert(j+1, (tasks[j][0], ((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1), tasks[j][2]))
                    tasks.insert(j+2, (tasks[j][0], tasks[j][1]-((dupe_workblocks[i][0]-dupe_workblocks[i][1]).total_seconds()/60)*(-1), tasks[j][2]))
                    tasks.pop(j)
                else:
                    i += 1

                break

            

            else:
                pass

            
    return nest, overflows

for key, value in nest_tasks(work_blocks, sorted_tasks):
    print(f"{key}: {value}")

schedule = []


