import unittest
from schedules.task import Task
from schedules.staged_task import StagedTask
from schedules.conveyor_schedule import ConveyorSchedule


class TestDowntimeMethods(unittest.TestCase):
    def test_downtime_calculation(self):
        """Проверяет, что простой рассчитывается как сумма простоев по исполнителям."""
        tasks = [StagedTask("a", [1, 1]), StagedTask("b", [1, 1])]
        schedule = ConveyorSchedule(tasks)
        d0 = schedule.get_downtime_for_executor(0)
        d1 = schedule.get_downtime_for_executor(1)
        self.assertEqual(2, schedule.total_downtime())
        self.assertEqual(2, d0 + d1)

    def test_with_downtime_single_task(self):
        task = StagedTask("x", [1, 2])
        schedule = ConveyorSchedule([task])

        self.assertEqual(2, schedule.get_downtime_for_executor(0))
        self.assertEqual(1, schedule.get_downtime_for_executor(1))
        self.assertEqual(3, schedule.total_downtime())

    def test_total_downtime_two_executors(self):
        tasks = [StagedTask("a", [2, 1]), StagedTask("b", [1, 3])]
        schedule = ConveyorSchedule(tasks)
        d0 = schedule.get_downtime_for_executor(0)
        d1 = schedule.get_downtime_for_executor(1)
        total = schedule.total_downtime()

        self.assertEqual(total, d0 + d1)