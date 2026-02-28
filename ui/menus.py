"""Main menu, lesson select, and settings menus for Poker4U."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

from lessons.lesson_manager import LessonManager
from ui.display import get_input

console = Console()


def show_splash_screen():
    """Show the startup splash screen with disclaimer."""
    console.clear()
    splash = Text()
    splash.append("\n")
    splash.append("    ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ ██╗  ██╗██╗   ██╗\n", style="bold blue")
    splash.append("    ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██║  ██║██║   ██║\n", style="bold blue")
    splash.append("    ██████╔╝██║   ██║█████╔╝ █████╗  ██████╔╝███████║██║   ██║\n", style="bold cyan")
    splash.append("    ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗╚════██║██║   ██║\n", style="bold cyan")
    splash.append("    ██║     ╚██████╔╝██║  ██╗███████╗██║  ██║     ██║╚██████╔╝\n", style="bold magenta")
    splash.append("    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═╝ ╚═════╝\n", style="bold magenta")
    splash.append("\n")
    splash.append("         Game Theory for Everyone\n", style="bold white")
    console.print(splash)

    console.print(Panel(
        "[dim]Poker4U is an educational game theory tool.\n"
        "It teaches decision-making concepts using poker as a vehicle.\n"
        "Not affiliated with gambling. Uses educational chips, not real money.[/dim]",
        border_style="dim",
        padding=(0, 2),
    ))
    console.print()


def show_main_menu(manager: LessonManager) -> str:
    """Show the main menu and return user's choice."""
    progress = manager.get_overall_progress()

    menu = Panel(
        "[bold white]  [1]  Lessons Mode[/bold white]\n"
        "[bold white]  [2]  Practice Mode[/bold white]\n"
        "[bold white]  [3]  EV Calculator[/bold white]\n"
        "[bold white]  [4]  Scenario Challenges[/bold white]\n"
        "[bold white]  [5]  Game Theory Glossary[/bold white]\n"
        "[bold white]  [s]  Stats & Progress[/bold white]\n"
        "[bold white]  [q]  Exit[/bold white]",
        title="[bold blue]POKER4U[/bold blue]  [dim]Game Theory for Everyone[/dim]",
        border_style="blue",
        padding=(1, 3),
    )
    console.print(menu)

    # Quick progress line
    console.print(
        f"  [dim]Lessons: {progress['lessons_done']}/6 | "
        f"Scenarios: {progress['scenarios_done']}/8 | "
        f"Hands: {progress['hands_played']}[/dim]"
    )
    console.print()

    return get_input("[bold]Choose an option: [/bold]", ["1", "2", "3", "4", "5", "s", "q"])


def show_lesson_select(manager: LessonManager) -> str:
    """Show lesson selection menu."""
    from lessons.content import LESSONS

    console.print()
    console.print("[bold cyan]  Lessons Mode[/bold cyan]")
    console.print("[dim]  Complete lessons to learn game theory concepts step by step.[/dim]")
    console.print()

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("#", width=3, justify="center")
    table.add_column("Lesson", width=35)
    table.add_column("Status", width=15, justify="center")
    table.add_column("Score", width=10, justify="center")

    for num, lesson in LESSONS.items():
        completed = manager.is_lesson_complete(num)
        score = manager.get_lesson_score(num)

        status = "[green]Completed[/green]" if completed else "[yellow]Available[/yellow]"
        score_str = f"{score:.0f}%" if score is not None else "-"

        table.add_row(str(num), lesson["title"], status, score_str)

    console.print(table)
    console.print()

    return get_input(
        "[bold]Select lesson (1-6) or 'q' to go back: [/bold]",
        ["1", "2", "3", "4", "5", "6", "q"],
    )


def show_scenario_select(manager: LessonManager) -> str:
    """Show scenario challenge selection."""
    from lessons.scenarios import SCENARIO_CHALLENGES

    console.print()
    console.print("[bold cyan]  Scenario Challenges[/bold cyan]")
    console.print("[dim]  Test your game theory knowledge with real scenarios.[/dim]")
    console.print()

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("#", width=3, justify="center")
    table.add_column("Scenario", width=30)
    table.add_column("Concept", width=20)
    table.add_column("Status", width=12, justify="center")

    for i, scenario in enumerate(SCENARIO_CHALLENGES, 1):
        completed = manager.is_scenario_complete(scenario["id"])
        status = "[green]Done[/green]" if completed else "[yellow]New[/yellow]"
        table.add_row(str(i), scenario["title"], scenario["concept"], status)

    console.print(table)
    console.print()

    valid = [str(i) for i in range(1, len(SCENARIO_CHALLENGES) + 1)] + ["q"]
    return get_input(
        f"[bold]Select scenario (1-{len(SCENARIO_CHALLENGES)}) or 'q' to go back: [/bold]",
        valid,
    )


def show_glossary_menu() -> str:
    """Show glossary term selection."""
    from engine.game_theory import GLOSSARY

    console.print()
    console.print("[bold cyan]  Game Theory Glossary[/bold cyan]")
    console.print("[dim]  Key concepts with poker examples and real-life applications.[/dim]")
    console.print()

    terms = list(GLOSSARY.keys())
    for i, term in enumerate(terms, 1):
        console.print(f"  [bold]{i}.[/bold] {term}")

    console.print()
    valid = [str(i) for i in range(1, len(terms) + 1)] + ["q"]
    return get_input(
        f"[bold]Select term (1-{len(terms)}) or 'q' to go back: [/bold]",
        valid,
    )


def show_glossary_entry(term: str, entry: dict):
    """Display a glossary entry."""
    console.print()
    console.print(Panel(
        f"[bold]{entry['definition']}[/bold]",
        title=f"[bold cyan]{term}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    console.print(Panel(
        entry["poker_example"],
        title="[bold yellow]Poker Example[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    ))

    console.print(Panel(
        entry["real_life"],
        title="[bold magenta]Real Life Application[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
    ))
