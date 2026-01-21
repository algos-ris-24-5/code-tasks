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
        time_0 = 0
        time_1 = 0
        raw_0 = []
        raw_1 = []

        for task in tasks:
            a, b = task.stage_durations

            start_0 = time_0
            raw_0.append(ScheduleItem(task, start_0, a))
            time_0 = start_0 + a

            start_1 = max(time_0, time_1)
            raw_1.append(ScheduleItem(task, start_1, b))
            time_1 = start_1 + b

        total_duration = max(time_0, time_1)

        filled_0 = []
        current_time = 0
        for item in raw_0:
            if item.start > current_time:
                gap = item.start - current_time
                filled_0.append(ScheduleItem(None, current_time, gap))
            filled_0.append(item)
            current_time = item.end
        if current_time < total_duration:
            gap = total_duration - current_time
            filled_0.append(ScheduleItem(None, current_time, gap))

        filled_1 = []
        current_time = 0
        for item in raw_1:
            if item.start > current_time:
                gap = item.start - current_time
                filled_1.append(ScheduleItem(None, current_time, gap))
            filled_1.append(item)
            current_time = item.end
        if current_time < total_duration:
            gap = total_duration - current_time
            filled_1.append(ScheduleItem(None, current_time, gap))

        self._executor_schedule[0] = filled_0
        self._executor_schedule[1] = filled_1

    @staticmethod
    def __sort_tasks(tasks: list[StagedTask]) -> list[StagedTask]:
        """Возвращает отсортированный список задач для применения
        алгоритма Джонсона."""
        group1 = []
        group2 = []

        for task in tasks:
            a, b = task.stage_durations
            if a <= b:
                group1.append(task)
            else:
                group2.append(task)

        group1.sort(key=lambda t: t.stage_durations[0])
        group2.sort(key=lambda t: t.stage_durations[1], reverse=True)
        
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
