from datetime import datetime, timedelta
import tasks_db_manager as dm
import workblocks_db_manager as wbdm
CAP = 120
SPREAD = 2
#Work time blocks

dm.insert_task("grp1", "NIE", "Read chapter 3", datetime(2026,8,14,23,0), 20  )
dm.insert_task("grp2", "PHY in SC", "Physics homework", datetime(2026,8,15,9,0), 60  )
dm.insert_task("grp1", "NIE", "Essay draft", datetime(2026,8,16,9,0), 120  )
dm.insert_task("grp4", "PSAT", "Extra reading", datetime(2026,8,16,12,0), 90  )
wbdm.insert_workblock(datetime(2026,8,14,16,30), datetime(2026,8,14,19,0))   # 4:30pm-7pm
wbdm.insert_workblock(datetime(2026,8,14,21,0), datetime(2026,8,14,22,0))   # 9pm-10pm

work_blocks = wbdm.load_wbs()
#wb_id(0), start_time(1), end_time(2), mins(3)

#Load and Update Tasks(And sort them by deadline)

tasks = dm.load_tasks()
sorted_tasks = sorted(tasks, key= lambda task: task[2])


#(task_name, min_dedicated, deadline, task_id, higher_id)


# to get the work periods in minutes to process easily
work_periods = wbdm.load_wbs()

#for i in work_blocks:
    #work_periods.append(((i[0]-i[1]).total_seconds()/60)*(-1))

# a considerate sort to space same tasks for user (prevent fatigue)
def considerate_sort(o_tasks, CAP, SPREAD):
    tasks = []
    for i in o_tasks:
        tasks.append(i)
    i = 0
    #(task_name(0), min_dedicated(1), deadline(2), task_id(3), higher_id(4))
    while i != len(tasks):
        if tasks[i][1] > CAP:
            tasks.insert(i+1, (tasks[i][0], CAP, tasks[i][2], tasks[i][3], tasks[i][4]))
            tasks.insert(i+2+SPREAD, (tasks[i][0], tasks[i][1]-120, tasks[i][2], tasks[i][3], tasks[i][4]))
            tasks.pop(i)

        else:
            pass

        i += 1

    return tasks


#The meat of the program, the function which assigns tasks to specific work blocks
def nest_tasks(work_blocks, tasks):
    dupe_workblocks = []
    for i in work_blocks:
        dupe_workblocks.append(list(i))
    nest = {}
    j = 0
    i = 0
    while j != len(tasks): 
        while i != len(dupe_workblocks):
            

            #If the task fits the workblock, we nest it and then update the work block's new timings
            if (dupe_workblocks[i][3]) >= tasks[j][1]:
                nest[(tasks[j][0], tasks[j][1]) ] = (dupe_workblocks[i][1], dupe_workblocks[i][1]+ timedelta(minutes = tasks[j][1]))
                dupe_workblocks[i][1] += timedelta(minutes = tasks[j][1])
                dupe_workblocks[i][3] -= tasks[j][1]
                dm.assign_workblock(tasks[j][3], dupe_workblocks[i][0])
                j += 1
                break
            #wb_id(0), start_time(1), end_time(2), mins(3)  
            #If very task ends up not fitting in any workblock despite being divided in to smaller part, marked overflow
            elif (((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1)) == 0 and i == len(dupe_workblocks)-1:
                    dm.mark_overflow(tasks[j][3])
                    j += 1
                    break

            #(task_name(0), min_dedicated(1), deadline(2), task_id(3), higher_id(4))

            #If the task fits workblock partially, we split it into parts: the one which occupies work block, the task with remaining time
            elif (((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1)) < tasks[j][1]:
                if ((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1) != 0:
                    id_split_one = dm.insert_task(tasks[j][4], tasks[j][5], tasks[j][0], tasks[j][2], ((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1))
                    tasks.insert(j+1, (tasks[j][0], ((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1), tasks[j][2], id_split_one, tasks[j][4], tasks[j][5]))
                    id_split_two = dm.insert_task(tasks[j][4], tasks[j][5], tasks[j][0], tasks[j][2], tasks[j][1]-((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1))
                    tasks.insert(j+2, (tasks[j][0], tasks[j][1]-((dupe_workblocks[i][1]-dupe_workblocks[i][2]).total_seconds()/60)*(-1), tasks[j][2], id_split_two, tasks[j][4], tasks[j][5]))

                    dm.remove_task(tasks[j][3])
                    tasks.pop(j)
                else:
                    i += 1            
                break

            

            else:
                pass



            
    return nest

nest_tasks(work_blocks, considerate_sort(sorted_tasks, CAP, SPREAD))
dm.close_base()
wbdm.close_base()


