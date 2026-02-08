import random
from dataclasses import dataclass
from typing import List


# -----------------------------
# Data Model
# -----------------------------
@dataclass
class Task:
    id: int
    title: str
    story_points: int
    status: str = "To Do"


# -----------------------------
# Sprint Simulator
# -----------------------------
class SprintBoard:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def simulate_progress(self):
        """Randomly move tasks across statuses"""
        for task in self.tasks:
            move = random.choice(["To Do", "In Progress", "Done"])
            task.status = move

    def completion_percentage(self) -> float:
        total_points = sum(t.story_points for t in self.tasks)
        done_points = sum(t.story_points for t in self.tasks if t.status == "Done")

        if total_points == 0:
            return 0.0
        return (done_points / total_points) * 100
    # def linear_completion(self) -> float:
    #     """Calculate linear completion based on task order"""
    #     total_tasks = len(self.tasks)
    #     completed_tasks = sum(1 for t in self.tasks if t.status == "Done")

    #     if total_tasks == 0:
    #         return 0.0
    #     return (completed_tasks / total_tasks) * 100
    

    def sprint_health(self) -> str:
        percent = self.completion_percentage()

        if percent > 75:
            return "🟢 On Track"
        elif percent > 40:
            return "🟡 Risky"
        else:
            return "🔴 Needs Attention"

    def report(self):
        print("\n📋 Sprint Report")
        for t in self.tasks:
            print(f"Task {t.id}: {t.title} | SP: {t.story_points} | {t.status}")

        percent = self.completion_percentage()
        print(f"\nCompletion: {percent:.2f}%")
        print("Health:", self.sprint_health())


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    tasks = [
        Task(1, "Login API", 5),
        Task(2, "Dashboard UI", 8),
        Task(3, "Database schema", 3),
        Task(4, "Auth integration", 5),
        Task(5, "Testing", 2),
    ]

    board = SprintBoard(tasks)

    board.simulate_progress()  # random movement
    board.report()
