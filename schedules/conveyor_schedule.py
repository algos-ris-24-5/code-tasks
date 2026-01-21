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
        self._executor_schedule = [[], []]

        current_end_time_executor_1 = 0
        current_end_time_executor_2 = 0

        for task in tasks:
            time_stage_1 = task.stage_duration(0)
            time_stage_2 = task.stage_duration(1)

            self._executor_schedule[0].append(ScheduleItem(task, current_end_time_executor_1, time_stage_1))
            current_end_time_executor_1 += time_stage_1

            start_time_executor_2 = max(current_end_time_executor_2, current_end_time_executor_1)
            if start_time_executor_2 > current_end_time_executor_2:
                idle_duration = start_time_executor_2 - current_end_time_executor_2
                self._executor_schedule[1].append(ScheduleItem(None, current_end_time_executor_2, idle_duration))

            self._executor_schedule[1].append(ScheduleItem(task, start_time_executor_2, time_stage_2))
            current_end_time_executor_2 = start_time_executor_2 + time_stage_2

        if current_end_time_executor_1 < current_end_time_executor_2:
            idle_duration = current_end_time_executor_2 - current_end_time_executor_1
            self._executor_schedule[0].append(ScheduleItem(None, current_end_time_executor_1, idle_duration))


    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        group_1 = []
        group_2 = []

        for task in tasks:
            time_stage_1 = task.stage_duration(0)
            time_stage_2 = task.stage_duration(1)
            if time_stage_1 <= time_stage_2:
                group_1.append(task)
            else:
                group_2.append(task)

        group_1.sort(key=lambda task: task.stage_duration(0))
        group_2.sort(key=lambda task: task.stage_duration(1), reverse=True)

        return group_1 + group_2


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
    
    def update_tasks(self, new_tasks: list[StagedTask]) -> None:
        """Обновляет список задач и пересчитывает расписание
        согласно алгоритму Джонсона."""
        ConveyorSchedule.__validate_params(new_tasks)
        self._tasks = new_tasks
        self._executor_schedule = [[] for _ in range(2)]
        sorted_tasks = self.__sort_tasks(new_tasks)
        self.__fill_schedule(sorted_tasks)


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
