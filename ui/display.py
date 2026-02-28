"""Rich-based terminal UI rendering for Poker4U."""

from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.markdown import Markdown
from rich.tree import Tree
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

from engine.cards import Card, HoleCards
from engine.evaluator import HandRank, HAND_RANK_NAMES, HAND_PROBABILITIES

console = Console()


def clear_screen():
    console.clear()


def print_header(title: str, subtitle: str = ""):
    """Print a styled header."""
    text = Text()
    text.append(f"  {title}  ", style="bold white on blue")
    if subtitle:
        text.append(f"\n  {subtitle}", style="dim italic")
    console.print()
    console.print(text)
    console.print()


def render_card(card: Card) -> Panel:
    """Render a single card as a Rich Panel."""
    color = card.color
    content = Text()
    content.append(f" {card.rank_str}   \n", style=f"bold {color}")
    content.append(f"  {card.suit_symbol}  \n", style=f"bold {color}")
    content.append(f"   {card.rank_str} ", style=f"bold {color}")
    return Panel(
        content,
        width=7,
        height=5,
        style=f"bold {color}",
        box=box.ROUNDED,
    )


def render_card_back() -> Panel:
    """Render a face-down card."""
    content = Text()
    content.append(" ? ? \n", style="dim blue")
    content.append("  ?  \n", style="dim blue")
    content.append(" ? ? ", style="dim blue")
    return Panel(content, width=7, height=5, style="dim blue", box=box.ROUNDED)


def show_cards(cards: List[Card], title: str = ""):
    """Display a row of cards."""
    if not cards:
        return
    panels = [render_card(c) for c in cards]
    if title:
        console.print(f"  [bold]{title}[/bold]")
    console.print(Columns(panels, padding=(0, 1)))


def show_hole_cards(hole_cards: HoleCards, title: str = "Your Hand"):
    """Display hole cards with title."""
    show_cards(hole_cards.cards, title)


def show_community_cards(cards: List[Card]):
    """Display community cards."""
    if not cards:
        console.print("  [dim]No community cards yet[/dim]")
        return
    show_cards(cards, "Community Cards")


def show_game_state(pot: int, community: List[Card], players: list,
                     current_player_idx: int = -1):
    """Show the full game state: pot, community, player chips."""
    console.print()
    # Pot
    console.print(f"  [bold yellow]Pot: {pot} chips[/bold yellow]")
    console.print()

    # Community cards
    show_community_cards(community)
    console.print()

    # Player status table
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold cyan")
    table.add_column("Player", style="bold")
    table.add_column("Chips", justify="right")
    table.add_column("Status", justify="center")
    table.add_column("Bet", justify="right")

    for i, p in enumerate(players):
        name = p.name
        if i == current_player_idx:
            name = f">> {name} <<"
        status = "[red]Folded[/red]" if p.folded else "[green]Active[/green]"
        if p.chips <= 0 and not p.folded:
            status = "[yellow]All-In[/yellow]"
        style = "bold" if i == current_player_idx else ""
        table.add_row(
            name,
            str(p.chips),
            status,
            str(p.current_bet),
            style=style,
        )

    console.print(table)


def show_analysis(analysis: Dict):
    """Show educational analysis overlay after each decision point."""
    console.print()
    rec = analysis.get("recommendation", {})

    # Main analysis panel
    lines = []
    lines.append(f"[bold cyan]Hand Strength:[/bold cyan] {rec.get('equity_pct', 'N/A')}")
    if "current_hand" in analysis:
        lines.append(f"[bold cyan]Current Hand:[/bold cyan] {analysis['current_hand']}")
    lines.append(f"[bold cyan]Hand Percentile:[/bold cyan] {analysis.get('hand_percentile', 0):.0f}th")

    if analysis.get("outs"):
        lines.append(f"[bold cyan]Outs:[/bold cyan] {analysis['outs']}")

    lines.append("")
    lines.append(f"[bold]Pot Odds:[/bold] {rec.get('pot_odds_pct', 'N/A')} ({rec.get('pot_odds_ratio', '')})")

    # EV for each action
    lines.append("")
    lines.append("[bold]Expected Value of Each Action:[/bold]")

    ev_fold = rec.get("ev_fold", 0)
    ev_call = rec.get("ev_call", 0)
    ev_raise = rec.get("ev_raise", 0)

    fold_color = rec.get("ev_fold_color", "yellow")
    call_color = rec.get("ev_call_color", "yellow")
    raise_color = rec.get("ev_raise_color", "yellow")

    lines.append(f"  [{fold_color}]Fold:  {ev_fold:+.1f} chips[/{fold_color}]")
    lines.append(f"  [{call_color}]Call:  {ev_call:+.1f} chips[/{call_color}]")
    lines.append(f"  [{raise_color}]Raise: {ev_raise:+.1f} chips[/{raise_color}]")

    best = rec.get("best_action", "")
    lines.append("")
    lines.append(f"[bold green]GTO Recommendation: {best.upper()}[/bold green]")

    panel = Panel(
        "\n".join(lines),
        title="[bold cyan]Analysis[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)


def show_action_result(player_name: str, action: str, amount: int,
                        is_correct: Optional[bool] = None):
    """Display a player's action."""
    action_text = action.capitalize()
    if amount > 0:
        action_text += f" {amount} chips"

    if is_correct is True:
        marker = "[green]+EV[/green]"
    elif is_correct is False:
        marker = "[red]-EV[/red]"
    else:
        marker = ""

    console.print(f"  [bold]{player_name}[/bold]: {action_text} {marker}")


def show_hand_result(result: Dict):
    """Show the result of a completed hand."""
    console.print()
    winners = result.get("winners", [])
    pot = result.get("pot", 0)
    method = result.get("method", "")

    if method == "fold":
        console.print(Panel(
            f"[bold green]{winners[0]}[/bold green] wins [bold yellow]{pot} chips[/bold yellow] (everyone else folded)",
            border_style="green",
        ))
    else:
        # Show all hands at showdown
        results = result.get("results", {})
        lines = ["[bold]Showdown![/bold]\n"]
        for name, info in results.items():
            if info and info.get("hand"):
                hand = info["hand"]
                hc = info["hole_cards"]
                is_winner = name in winners
                style = "bold green" if is_winner else "dim"
                marker = " ** WINNER **" if is_winner else ""
                lines.append(f"[{style}]{name}: {hc} → {hand.name}{marker}[/{style}]")

        lines.append(f"\n[bold yellow]Pot: {pot} chips[/bold yellow]")

        console.print(Panel("\n".join(lines), border_style="green", title="Results"))


def show_decision_tree(actions: list):
    """Show a decision tree for hand analysis."""
    tree = Tree("[bold]Hand Analysis[/bold]")
    current_street = None

    for action in actions:
        street_name = action.street.value if hasattr(action.street, 'value') else str(action.street)
        if street_name != current_street:
            current_street = street_name
            street_branch = tree.add(f"[bold cyan]{street_name}[/bold cyan]")

        ev_text = ""
        if action.ev is not None:
            color = "green" if action.ev >= 0 else "red"
            ev_text = f" [{color}]({action.ev:+.1f} EV)[/{color}]"

        amount_text = f" {action.amount}" if action.amount > 0 else ""
        street_branch.add(f"{action.player_name}: {action.action}{amount_text}{ev_text}")

    console.print(tree)


def show_hand_rankings_table():
    """Display the hand rankings table."""
    table = Table(
        title="[bold]Poker Hand Rankings[/bold]",
        box=box.DOUBLE_EDGE,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Rank", style="bold", justify="center", width=4)
    table.add_column("Hand", style="bold cyan", width=20)
    table.add_column("Example", width=20)
    table.add_column("Probability", justify="right", width=12)

    examples = {
        HandRank.ROYAL_FLUSH: "A K Q J T (same suit)",
        HandRank.STRAIGHT_FLUSH: "9 8 7 6 5 (same suit)",
        HandRank.FOUR_OF_A_KIND: "K K K K 3",
        HandRank.FULL_HOUSE: "Q Q Q 7 7",
        HandRank.FLUSH: "A J 8 4 2 (same suit)",
        HandRank.STRAIGHT: "T 9 8 7 6",
        HandRank.THREE_OF_A_KIND: "8 8 8 K 4",
        HandRank.TWO_PAIR: "J J 5 5 A",
        HandRank.ONE_PAIR: "9 9 A K 7",
        HandRank.HIGH_CARD: "A K J 8 3",
    }

    for i, rank in enumerate(reversed(list(HandRank)), 1):
        prob = HAND_PROBABILITIES[rank]
        prob_str = f"{prob:.4f}%" if prob < 0.01 else f"{prob:.2f}%"
        rarity = "[green]" if prob < 1 else "[yellow]" if prob < 10 else "[red]"
        table.add_row(
            str(i),
            HAND_RANK_NAMES[rank],
            examples.get(rank, ""),
            f"{rarity}{prob_str}[/{rarity[1:]}",
        )

    console.print(table)


def show_ev_calculator_result(result: Dict):
    """Display EV calculator results."""
    console.print()
    lines = []

    for step in result.get("math_breakdown", []):
        lines.append(step)

    console.print(Panel(
        "\n".join(lines),
        title="[bold cyan]EV Calculation[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))

    # Action comparison
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Action", style="bold")
    table.add_column("EV", justify="right")
    table.add_column("", justify="center")

    for action, ev_key, color_key in [
        ("Fold", "ev_fold", "ev_fold_color"),
        ("Call", "ev_call", "ev_call_color"),
        ("Raise", "ev_raise", "ev_raise_color"),
    ]:
        ev = result.get(ev_key, 0)
        color = result.get(color_key, "white")
        marker = " << BEST" if action.lower() == result.get("best_action", "") else ""
        table.add_row(action, f"[{color}]{ev:+.1f}[/{color}]", f"[bold green]{marker}[/bold green]")

    console.print(table)


def show_progress_bar(completed: int, total: int, label: str = "Progress"):
    """Show a progress bar."""
    with Progress(
        TextColumn(f"[bold]{label}"),
        BarColumn(bar_width=30),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(label, total=total, completed=completed)
        # Just display it
    console.print(f"  [bold]{label}:[/bold] {completed}/{total}")


def show_lesson_content(title: str, content: str):
    """Display lesson content using markdown."""
    console.print(Panel(
        Markdown(content),
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    ))


def show_real_life_tip(tip: str):
    """Show a real-life application tip."""
    console.print(Panel(
        Markdown(tip),
        title="[bold magenta]Real Life Application[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
    ))


def show_quiz_result(is_correct: bool, explanation: str):
    """Show quiz answer feedback."""
    if is_correct:
        console.print(Panel(
            f"[bold green]Correct![/bold green]\n\n{explanation}",
            border_style="green",
            padding=(1, 2),
        ))
    else:
        console.print(Panel(
            f"[bold red]Not quite.[/bold red]\n\n{explanation}",
            border_style="red",
            padding=(1, 2),
        ))


def show_lesson_score(score: float, passed: bool):
    """Show lesson completion score."""
    color = "green" if passed else "red"
    status = "PASSED" if passed else "NEEDS REVIEW"
    console.print(Panel(
        f"[bold {color}]Score: {score:.0f}% — {status}[/bold {color}]\n\n"
        f"{'Great job! You understand this concept.' if passed else 'You need 60% to pass. Try the lesson again!'}",
        border_style=color,
    ))


def show_stats(stats: Dict):
    """Display player statistics."""
    table = Table(
        title="[bold]Your Statistics[/bold]",
        box=box.DOUBLE_EDGE,
        show_header=False,
        padding=(0, 2),
    )
    table.add_column("Stat", style="bold cyan")
    table.add_column("Value", justify="right", style="bold")

    table.add_row("Hands Played", str(stats.get("hands_played", 0)))
    table.add_row("Decisions Made", str(stats.get("decisions_made", 0)))
    table.add_row("Correct Decisions", str(stats.get("correct_decisions", 0)))

    accuracy = stats.get("accuracy", 0)
    acc_color = "green" if accuracy >= 70 else "yellow" if accuracy >= 50 else "red"
    table.add_row("Accuracy", f"[{acc_color}]{accuracy:.1f}%[/{acc_color}]")

    ev = stats.get("total_ev_earned", 0)
    ev_color = "green" if ev >= 0 else "red"
    table.add_row("Total EV Earned", f"[{ev_color}]{ev:+.1f} chips[/{ev_color}]")

    console.print(table)


def prompt_action(to_call: int, can_check: bool, min_raise: int, player_chips: int) -> tuple:
    """Prompt the player for an action. Returns (action, amount)."""
    console.print()
    options = []
    if can_check:
        options.append("[bold]c[/bold])heck")
    else:
        options.append(f"[bold]c[/bold])all {to_call}")
    options.append(f"[bold]r[/bold])aise (min: {min_raise})")
    options.append("[bold]f[/bold])old")

    console.print(f"  Actions: {' | '.join(options)}")

    while True:
        try:
            choice = console.input("  [bold]Your action: [/bold]").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return "fold", 0

        if choice in ("f", "fold"):
            return "fold", 0
        elif choice in ("c", "check") and can_check:
            return "check", 0
        elif choice in ("c", "call") and not can_check:
            return "call", min(to_call, player_chips)
        elif choice.startswith("r") or choice.startswith("raise"):
            parts = choice.split()
            if len(parts) > 1:
                try:
                    amount = int(parts[1])
                except ValueError:
                    console.print("  [red]Enter a number for raise amount.[/red]")
                    continue
            else:
                try:
                    amount_str = console.input(f"  [bold]Raise amount ({min_raise}-{player_chips}): [/bold]")
                    amount = int(amount_str.strip())
                except (ValueError, EOFError, KeyboardInterrupt):
                    console.print("  [red]Enter a valid number.[/red]")
                    continue

            if amount < min_raise:
                console.print(f"  [red]Minimum raise is {min_raise}.[/red]")
                continue
            if amount > player_chips:
                amount = player_chips
                console.print(f"  [yellow]All-in: {amount} chips[/yellow]")
            return "raise", amount
        else:
            console.print("  [red]Invalid choice. Use c/r/f.[/red]")


def get_input(prompt_text: str, valid_options: Optional[list] = None) -> str:
    """Get user input with optional validation."""
    while True:
        try:
            choice = console.input(f"  {prompt_text}").strip()
        except (EOFError, KeyboardInterrupt):
            return "q"
        if valid_options is None or choice.lower() in [v.lower() for v in valid_options]:
            return choice
        console.print(f"  [red]Please choose from: {', '.join(valid_options)}[/red]")
