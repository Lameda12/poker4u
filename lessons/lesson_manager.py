"""Lesson progression system for Poker4U."""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path

PROGRESS_FILE = os.path.join(os.path.expanduser("~"), ".poker4u_progress.json")


class LessonManager:
    """Manages lesson progression and player stats."""

    def __init__(self):
        self.progress = self._load_progress()

    def _load_progress(self) -> Dict:
        """Load player progress from file."""
        if os.path.exists(PROGRESS_FILE):
            try:
                with open(PROGRESS_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_progress()

    def _default_progress(self) -> Dict:
        return {
            "lessons_completed": [],
            "lesson_scores": {},
            "practice_stats": {
                "hands_played": 0,
                "decisions_made": 0,
                "correct_decisions": 0,
                "total_ev_earned": 0.0,
            },
            "scenarios_completed": [],
            "total_sessions": 0,
        }

    def save_progress(self):
        """Save player progress to file."""
        try:
            with open(PROGRESS_FILE, "w") as f:
                json.dump(self.progress, f, indent=2)
        except IOError:
            pass  # Silently fail on write errors

    def is_lesson_complete(self, lesson_num: int) -> bool:
        return lesson_num in self.progress["lessons_completed"]

    def complete_lesson(self, lesson_num: int, score: float):
        """Mark a lesson as complete with a score."""
        if lesson_num not in self.progress["lessons_completed"]:
            if score >= 60:
                self.progress["lessons_completed"].append(lesson_num)
        self.progress["lesson_scores"][str(lesson_num)] = max(
            self.progress["lesson_scores"].get(str(lesson_num), 0),
            score,
        )
        self.save_progress()

    def get_lesson_score(self, lesson_num: int) -> Optional[float]:
        return self.progress["lesson_scores"].get(str(lesson_num))

    def get_next_lesson(self) -> int:
        """Get the next uncompleted lesson number."""
        for i in range(1, 7):
            if i not in self.progress["lessons_completed"]:
                return i
        return 1  # All complete, start over

    def lessons_completed_count(self) -> int:
        return len(self.progress["lessons_completed"])

    def update_practice_stats(self, hands: int = 0, decisions: int = 0,
                               correct: int = 0, ev: float = 0.0):
        stats = self.progress["practice_stats"]
        stats["hands_played"] += hands
        stats["decisions_made"] += decisions
        stats["correct_decisions"] += correct
        stats["total_ev_earned"] += ev
        self.save_progress()

    def get_practice_stats(self) -> Dict:
        stats = self.progress["practice_stats"]
        accuracy = 0.0
        if stats["decisions_made"] > 0:
            accuracy = (stats["correct_decisions"] / stats["decisions_made"]) * 100
        return {
            **stats,
            "accuracy": accuracy,
        }

    def complete_scenario(self, scenario_id: str):
        if scenario_id not in self.progress["scenarios_completed"]:
            self.progress["scenarios_completed"].append(scenario_id)
            self.save_progress()

    def is_scenario_complete(self, scenario_id: str) -> bool:
        return scenario_id in self.progress["scenarios_completed"]

    def increment_sessions(self):
        self.progress["total_sessions"] += 1
        self.save_progress()

    def get_overall_progress(self) -> Dict:
        """Get an overview of all progress."""
        stats = self.get_practice_stats()
        return {
            "lessons_done": self.lessons_completed_count(),
            "lessons_total": 6,
            "scenarios_done": len(self.progress["scenarios_completed"]),
            "scenarios_total": 8,
            "hands_played": stats["hands_played"],
            "accuracy": stats["accuracy"],
            "total_ev": stats["total_ev_earned"],
            "sessions": self.progress["total_sessions"],
        }
