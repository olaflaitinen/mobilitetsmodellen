"""Minimal directed-acyclic-graph task scheduler."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    """A named unit of work in the pipeline DAG.

    Attributes:
        name: Unique task identifier.
        fn: Callable to execute. Must accept no positional arguments.
        dependencies: Names of tasks that must complete before this one.
        result: Output of ``fn`` after execution, or ``None`` if not yet run.
    """

    name: str
    fn: Callable[[], Any]
    dependencies: list[str] = field(default_factory=list)
    result: Any = field(default=None, init=False, compare=False)


class DAG:
    """Simple directed-acyclic-graph task scheduler with topological execution.

    Args:
        tasks: Optional list of tasks to add at construction time.
    """

    def __init__(self, tasks: list[Task] | None = None) -> None:
        self._tasks: dict[str, Task] = {}
        for task in tasks or []:
            self.add(task)

    def add(self, task: Task) -> None:
        """Register a task in the DAG.

        Args:
            task: Task to register.

        Raises:
            ValueError: If a task with the same name is already registered.
        """
        if task.name in self._tasks:
            raise ValueError(f"Duplicate task name: '{task.name}'")
        self._tasks[task.name] = task

    def topological_order(self) -> list[str]:
        """Return task names in topological execution order (Kahn's algorithm).

        Returns:
            Ordered list of task names.

        Raises:
            ValueError: If the DAG contains a cycle.
        """
        in_degree: dict[str, int] = {name: 0 for name in self._tasks}
        for task in self._tasks.values():
            for _dep in task.dependencies:
                in_degree[task.name] = in_degree.get(task.name, 0) + 1
        queue: deque[str] = deque(n for n, d in in_degree.items() if d == 0)
        order: list[str] = []
        deps_adj: dict[str, list[str]] = {n: [] for n in self._tasks}
        for task in self._tasks.values():
            for _dep in task.dependencies:
                if _dep in deps_adj:
                    deps_adj[_dep].append(task.name)
        while queue:
            name = queue.popleft()
            order.append(name)
            for child in deps_adj.get(name, []):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    queue.append(child)
        if len(order) != len(self._tasks):
            raise ValueError("DAG contains a cycle; cannot determine execution order.")
        return order

    def run(self) -> dict[str, Any]:
        """Execute all tasks in topological order.

        Returns:
            Mapping of task name to its return value.
        """
        order = self.topological_order()
        for name in order:
            task = self._tasks[name]
            task.result = task.fn()
        return {name: self._tasks[name].result for name in order}
