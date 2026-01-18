from schedules.abstract_schedule import AbstractSchedule
from schedules.errors import (
    ScheduleArgumentError,
    ErrorMessages,
    ErrorTemplates,
)
from schedules.staged_task import StagedTask
from schedules.schedule_item import ScheduleItem


class ConveyorSchedule(AbstractSchedule):
    """Класс представляет оптимальное расписание для списка задач, состоящих
     из двух этапов и двух исполнителей. Для построения расписания используется
     алгоритм Джонсона.

    Properties
    ----------
    tasks(self) -> tuple[Task]:
        Возвращает исходный список задач для составления расписания.

    task_count(self) -> int:
        Возвращает количество задач для составления расписания.

    executor_count(self) -> int:
        Возвращает количество исполнителей.

    duration(self) -> float:
        Возвращает общую продолжительность расписания.

    Methods
    -------
    get_schedule_for_executor(self, executor_idx: int) -> tuple[ScheduleRow]:
        Возвращает расписание для указанного исполнителя.
    """

    def __init__(self, tasks: list[StagedTask]):
        """Конструктор для инициализации объекта расписания.

        :param tasks: Список задач для составления расписания.
        :raise ScheduleArgumentError: Если список задач предоставлен в
        некорректном формате или количество этапов для какой-либо задачи не
        равно двум.
        """
        ConveyorSchedule.__validate_params(tasks)
        super().__init__(tasks, 2)

        # Процедура заполняет пустую заготовку расписания для каждого
        # исполнителя объектами ScheduleItem.
        self.__fill_schedule(ConveyorSchedule.__sort_tasks(tasks))

    @property
    def duration(self) -> float:
        """Возвращает общую продолжительность расписания."""
        return self._executor_schedule[0][-1].end

    def __fill_schedule(self, tasks: list[StagedTask]) -> None:
        """Процедура составляет расписание из элементов ScheduleItem для каждого
        исполнителя, согласно алгоритму Джонсона."""

        self._executor_schedule = [[] for _ in range(self.executor_count)]
        
        time1_free = 0
        time2_free = 0
        
        for task in tasks:
            dur1 = task.stage_duration(0)
            dur2 = task.stage_duration(1)
            
            start1 = time1_free
            item1 = ScheduleItem(task, start1, dur1)
            self._executor_schedule[0].append(item1)
            time1_finish = start1 + dur1
            time1_free = time1_finish
            
            start2 = max(time1_finish, time2_free)
            if start2 > time2_free:
                downtime_dur = start2 - time2_free
                self._executor_schedule[1].append(ScheduleItem(None, time2_free, downtime_dur))
            
            item2 = ScheduleItem(task, start2, dur2)
            self._executor_schedule[1].append(item2)
            time2_free = start2 + dur2

        total_duration = time2_free
        exec1_end = self._executor_schedule[0][-1].end if self._executor_schedule[0] else 0
        
        if exec1_end < total_duration:
            self._executor_schedule[0].append(
                ScheduleItem(None, exec1_end, total_duration - exec1_end)
            )
        
    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        
        group1 = []
        group2 = []
        
        for t in tasks:
            if t.stage_duration(0) <= t.stage_duration(1):
                group1.append(t)
            else:
                group2.append(t)
        
        group1.sort(key=lambda x: x.stage_duration(0))
        group2.sort(key=lambda x: x.stage_duration(1), reverse=True)
        
        return group1 + group2

    @staticmethod
    def __validate_params(tasks: list[StagedTask]) -> None:
        """Проводит валидацию входящих параметров для инициализации объекта
        класса ConveyorSchedule."""

        if not isinstance(tasks, list):
            raise ScheduleArgumentError(ErrorMessages.TASKS_NOT_LIST)
        if len(tasks) < 1:
            raise ScheduleArgumentError(ErrorMessages.TASKS_EMPTY_LIST)
        for idx, value in enumerate(tasks):
            if not isinstance(value, StagedTask):
                raise ScheduleArgumentError(ErrorTemplates.INVALID_TASK.format(idx))
            if value.stage_count != 2:
                raise ScheduleArgumentError(
                    ErrorTemplates.INVALID_STAGE_CNT.format(idx)
                )
            
    def add_task(self, task: StagedTask) -> None:
        """Добавляет задачу и пересчитывает расписание."""

        if not isinstance(task, StagedTask):
            raise ScheduleArgumentError("Переданный объект не является StagedTask")
        if task.stage_count != 2:
            raise ScheduleArgumentError(ErrorTemplates.INVALID_STAGE_CNT.format("new_task"))
        
        self._tasks.append(task)
        self.__fill_schedule(self.__sort_tasks(self._tasks))
    
    def remove_task(self, task: StagedTask) -> None:
        """Удаляет задачу и пересчитывает расписание."""

        if task not in self._tasks:
            raise ValueError(f"Задача {task.name} не найдена в расписании.")
        
        self._tasks.remove(task)
        if not self._tasks:
            self._executor_schedule = [[] for _ in range(self.executor_count)]
        else:
            self.__fill_schedule(self.__sort_tasks(self._tasks))
    
    


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
