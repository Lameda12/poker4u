"""Card dealing animations and suspense effects for Poker4U."""

import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

console = Console()

# Global flag for skipping animations
SKIP_ANIMATIONS = False


def set_quick_mode(quick: bool):
    global SKIP_ANIMATIONS
    SKIP_ANIMATIONS = quick


def pause(seconds: float = 0.5):
    """Pause with animation support."""
    if not SKIP_ANIMATIONS:
        time.sleep(seconds)


def dealing_animation(num_cards: int = 2, label: str = "Dealing"):
    """Show a card dealing animation."""
    if SKIP_ANIMATIONS:
        return

    frames = ["🂠 ", "🂠 🂠 ", "🂠 🂠 🂠 "]
    with Live(console=console, refresh_per_second=8) as live:
        for i in range(min(num_cards, len(frames))):
            text = Text(f"  {label}... {frames[i]}", style="dim")
            live.update(text)
            time.sleep(0.3)
    time.sleep(0.2)


def suspense_animation(message: str = "Revealing"):
    """Show a brief suspense effect."""
    if SKIP_ANIMATIONS:
        return

    dots = [".", "..", "..."]
    with Live(console=console, refresh_per_second=4) as live:
        for dot in dots:
            text = Text(f"  {message}{dot}", style="dim italic")
            live.update(text)
            time.sleep(0.25)
    time.sleep(0.2)


def thinking_animation(message: str = "Thinking"):
    """Show AI thinking animation."""
    if SKIP_ANIMATIONS:
        return

    symbols = ["|", "/", "-", "\\"]
    with Live(console=console, refresh_per_second=6) as live:
        for _ in range(2):
            for s in symbols:
                text = Text(f"  {message} {s}", style="dim")
                live.update(text)
                time.sleep(0.15)
