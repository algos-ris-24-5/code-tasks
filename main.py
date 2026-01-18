from schedules.conveyor_schedule import ConveyorSchedule
from schedules.staged_task import StagedTask

SCHEDULE_MERMAID_EXECUTOR = "section Исполнитель {0}\n"

SCHEDULE_MERMAID_TASK_FIRST = "{0} :{1}1, 00, {2}h" 

SCHEDULE_MERMAID_TASK = "{0} :{1}{2}, after {3}{4}, {5}h"

if __name__ == "__main__":
    print("Пример использования класса ConveyorSchedule")

    # Инициализируем входные данные для составления расписания
    tasks = [
        StagedTask("a", [7, 2]),
        StagedTask("b", [3, 4]),
        StagedTask("c", [2, 5]),
        StagedTask("d", [4, 1]),
        StagedTask("e", [6, 6]),
        StagedTask("f", [5, 3]),
        StagedTask("g", [4, 5]),
    ]

    # Инициализируем экземпляр класса Schedule
    # при этом будет рассчитано расписание для каждого исполнителя
    schedule = ConveyorSchedule(tasks)

    # Выведем в консоль полученное расписание
    print(schedule)
    for i in range(schedule.executor_count):
        print(f"\nРасписание для исполнителя # {i + 1}:")
        for schedule_item in schedule.get_schedule_for_executor(i):
            print(schedule_item)

    mermaidElementsList = []
    mermaidElementsList.append('```mermaid\ngantt\ntitle Диаграмма Ганта\ndateFormat HH\naxisFormat %H\nНачало выполнения работ : milestone, m1, 00, 0h')
    
    for executor in range(schedule.executor_count):
        # mermaidElementsList.append(SCHEDULE_MERMAID_EXECUTOR.format(executor+1))
        tempExecutorList = [SCHEDULE_MERMAID_EXECUTOR.format(executor+1)]
        count = 2
        previousName = ''
        for scheduleItem in schedule.get_schedule_for_executor(i):
            if scheduleItem.task is None:
                pass
            else:
                taskName = scheduleItem.task.name
                taskDuration = scheduleItem.duration
                taskStart = scheduleItem.start
                if len(tempExecutorList) == 1:
                    tempExecutorList.append(SCHEDULE_MERMAID_TASK_FIRST.format(taskName, taskName, taskDuration))
                    previousName = taskName + '1'
                else:
                    tempExecutorList.append(SCHEDULE_MERMAID_TASK.format(taskName, taskName, count, previousName, taskDuration))
                    previousName = taskName + count
                    count+=1
        tempExecutorString = '\n'.join(tempExecutorList)
        mermaidElementsList.append(tempExecutorString)
        
    mermaidElementsList.append(f'Окончание выполнения работ : milestone, m2, {schedule.duration}, 0h')
    result = ''.join(mermaidElementsList)