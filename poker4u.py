#!/usr/bin/env python3
"""Poker4U - Game Theory for Everyone.

An educational poker game theory trainer that uses poker as a vehicle
to teach decision-making concepts applicable to real life.

Usage:
    python poker4u.py            # Normal mode
    python poker4u.py --quick    # Skip animations for fast play
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.markdown import Markdown

from engine.cards import Card, Deck, HoleCards
from engine.evaluator import evaluate_hand, hand_strength, hand_percentile
from engine.game import Game, Street
from engine.game_theory import (
    action_recommendation, pot_odds, expected_value_call,
    GLOSSARY, push_fold_nash_ranges,
)
from engine.ai_opponent import create_opponents
from lessons.lesson_manager import LessonManager
from lessons.content import LESSONS
from lessons.scenarios import LESSON_QUIZZES, SCENARIO_CHALLENGES
from ui.display import (
    clear_screen, print_header, show_cards, show_hole_cards,
    show_community_cards, show_game_state, show_analysis,
    show_action_result, show_hand_result, show_decision_tree,
    show_hand_rankings_table, show_ev_calculator_result,
    show_lesson_content, show_real_life_tip, show_quiz_result,
    show_lesson_score, show_stats, prompt_action, get_input,
    console,
)
from ui.menus import (
    show_splash_screen, show_main_menu, show_lesson_select,
    show_scenario_select, show_glossary_menu, show_glossary_entry,
)
from ui.animations import (
    set_quick_mode, dealing_animation, suspense_animation,
    thinking_animation, pause,
)


def run_lesson(lesson_num: int, manager: LessonManager):
    """Run a complete lesson with content and quiz."""
    lesson = LESSONS.get(lesson_num)
    if not lesson:
        console.print("[red]Lesson not found.[/red]")
        return

    clear_screen()
    print_header(f"Lesson {lesson_num}: {lesson['title']}", lesson["subtitle"])

    # Show intro
    show_lesson_content("Introduction", lesson["intro"])
    get_input("[dim]Press Enter to continue...[/dim] ")

    # Show each section
    for section in lesson["sections"]:
        clear_screen()
        print_header(f"Lesson {lesson_num}: {lesson['title']}")
        show_lesson_content(section["title"], section["content"])
        get_input("[dim]Press Enter to continue...[/dim] ")

    # Show real-life application
    clear_screen()
    print_header(f"Lesson {lesson_num}: {lesson['title']}")
    show_real_life_tip(lesson["real_life_tip"])
    get_input("[dim]Press Enter to start the quiz...[/dim] ")

    # Run quiz
    quiz = LESSON_QUIZZES.get(lesson_num, [])
    if not quiz:
        console.print("[yellow]No quiz available for this lesson.[/yellow]")
        return

    correct_count = 0
    total = len(quiz)

    for i, q in enumerate(quiz, 1):
        clear_screen()
        print_header(f"Lesson {lesson_num} Quiz", f"Question {i}/{total}")
        console.print(Panel(q["question"], border_style="cyan", padding=(1, 2)))
        console.print()

        # Show options
        options = q.get("options")
        if options:
            for j, opt in enumerate(options, 1):
                console.print(f"  [bold]{j}.[/bold] {opt}")
            console.print()

            valid = [str(j) for j in range(1, len(options) + 1)]
            answer = get_input("[bold]Your answer: [/bold]", valid)
            if answer == "q":
                return

            selected = options[int(answer) - 1]
            is_correct = selected == q["correct"]
        else:
            # Hand comparison quiz (lesson 1)
            console.print(f"  [bold]A:[/bold] {q['hand_a_name']}")
            console.print(f"  [bold]B:[/bold] {q['hand_b_name']}")
            console.print()
            answer = get_input("[bold]Which wins? (a/b): [/bold]", ["a", "b"])
            if answer == "q":
                return
            is_correct = answer.lower() == q["correct"]

        if is_correct:
            correct_count += 1

        show_quiz_result(is_correct, q["explanation"])
        pause(0.5)
        get_input("[dim]Press Enter to continue...[/dim] ")

    # Show final score
    score = (correct_count / total) * 100
    passed = score >= 60

    clear_screen()
    print_header(f"Lesson {lesson_num} Complete!")
    show_lesson_score(score, passed)
    manager.complete_lesson(lesson_num, score)

    get_input("[dim]Press Enter to return to menu...[/dim] ")


def run_practice_mode(manager: LessonManager):
    """Run practice mode with AI opponents."""
    clear_screen()
    print_header("Practice Mode", "Play Texas Hold'em against AI opponents")

    console.print("[dim]  You'll play against three AI opponents:[/dim]")
    opponents = create_opponents()
    for opp in opponents:
        console.print(f"  [bold]{opp.name}[/bold] - {opp.description}")
    console.print()

    game = Game()
    game.setup_players(num_ai=3)

    hands_played = 0
    total_decisions = 0
    correct_decisions = 0
    total_ev = 0.0

    while True:
        # Check if player has chips
        player = game.players[0]
        if player.chips <= 0:
            console.print("[red]You're out of chips! Game over.[/red]")
            break

        active_with_chips = [p for p in game.players if p.chips > 0]
        if len(active_with_chips) < 2:
            console.print("[green]You've beaten all opponents! Congratulations![/green]")
            break

        # Start new hand
        hand_info = game.start_hand()
        if "error" in hand_info:
            console.print(f"[red]{hand_info['error']}[/red]")
            break

        hands_played += 1
        clear_screen()
        print_header(f"Hand #{hand_info['hand_number']}")
        console.print(f"  [dim]Blinds: {hand_info['small_blind']} ({hand_info['sb_amount']}) / "
                      f"{hand_info['big_blind']} ({hand_info['bb_amount']})[/dim]")

        dealing_animation(2, "Dealing hole cards")
        show_hole_cards(player.hole_cards)

        # Preflop percentile
        pct = hand_percentile(player.hole_cards)
        console.print(f"  [cyan]Hand: {player.hole_cards.short_name()} "
                      f"(Top {100 - pct:.0f}% of hands)[/cyan]")

        # --- Play through streets ---
        hand_over = False

        for street_idx in range(4):  # preflop, flop, turn, river
            if hand_over:
                break

            if street_idx > 0:
                # Deal community cards
                suspense_animation("Dealing")
                new_cards = game.deal_street()
                clear_screen()
                print_header(f"Hand #{hand_info['hand_number']} - {game.street.value}")
                show_hole_cards(player.hole_cards)
                show_community_cards(game.community)

            # Betting round
            action_order = _get_action_order(game, street_idx)

            acted = set()
            last_raiser = None
            round_num = 0

            while True:
                all_acted = True
                for p in action_order:
                    if p.folded or p.chips <= 0:
                        continue

                    # Skip if already acted and no new raise
                    pid = id(p)
                    if pid in acted and (last_raiser is None or pid == last_raiser):
                        continue

                    if p.is_human:
                        # Show game state and analysis
                        console.print()
                        show_game_state(game.pot, game.community, game.players)

                        analysis = game.get_player_analysis(p)
                        show_analysis(analysis)

                        to_call = game.current_bet - p.current_bet
                        can_check = to_call <= 0
                        action, amount = prompt_action(
                            to_call, can_check, game.min_raise, p.chips
                        )

                        # Track EV correctness
                        rec = analysis.get("recommendation", {})
                        best = rec.get("best_action", "")
                        is_correct = (action == best) or (
                            action == "check" and best in ("check", "call")
                        )
                        ev_of_action = rec.get(f"ev_{action}", 0)

                        total_decisions += 1
                        if is_correct:
                            correct_decisions += 1
                            total_ev += abs(ev_of_action)
                        else:
                            total_ev -= abs(ev_of_action) * 0.5

                        result = game.process_action(p, action, amount)
                        show_action_result(p.name, result["action"], result.get("amount", 0), is_correct)

                        if action == "raise":
                            last_raiser = pid
                            acted = {pid}
                            all_acted = False
                        else:
                            acted.add(pid)

                    else:
                        # AI decision
                        thinking_animation(f"{p.name} is thinking")
                        action, amount = game.get_ai_action(p)
                        result = game.process_action(p, action, amount)
                        show_action_result(p.name, result["action"], result.get("amount", 0))

                        if action == "raise":
                            last_raiser = pid
                            acted = {pid}
                            all_acted = False
                        else:
                            acted.add(pid)

                    # Check if hand is over
                    active = game.get_active_players()
                    if len(active) <= 1:
                        hand_over = True
                        break

                if hand_over:
                    break

                # Check if all bets are settled
                active = game.get_active_players()
                bets = set(p.current_bet for p in active if p.chips > 0)
                if len(bets) <= 1 and len(acted) >= len([p for p in active if p.chips > 0]):
                    break

                round_num += 1
                if round_num > 10:
                    break

        # Showdown
        console.print()
        suspense_animation("Revealing cards")

        result = game.showdown()
        show_hand_result(result)

        # Show decision tree
        if game.hand_history.actions:
            console.print()
            show_decision_tree(game.hand_history.actions)

        # Real-life tip
        import random
        tips = [
            "Every decision you make has an expected value. Start calculating!",
            "In life, as in poker, information is power. Seek it before deciding.",
            "Sunk costs are irrelevant. Only future costs and benefits matter.",
            "Variance is real. Judge decisions by process, not outcomes.",
            "Position matters. In negotiations, let the other side go first.",
        ]
        console.print(Panel(
            f"[magenta]{random.choice(tips)}[/magenta]",
            title="[bold magenta]Real Life Tip[/bold magenta]",
            border_style="magenta",
        ))

        console.print()
        choice = get_input("[bold]Play another hand? (y/n): [/bold]", ["y", "n", "q"])
        if choice in ("n", "q"):
            break

    # Update stats
    manager.update_practice_stats(
        hands=hands_played,
        decisions=total_decisions,
        correct=correct_decisions,
        ev=total_ev,
    )

    console.print()
    show_stats(manager.get_practice_stats())
    get_input("[dim]Press Enter to return to menu...[/dim] ")


def _get_action_order(game: Game, street_idx: int):
    """Get the order players should act for a given street."""
    n = len(game.players)
    if street_idx == 0:
        # Preflop: start after BB
        start = (game.dealer_pos + 2) % n
    else:
        # Postflop: start after dealer
        start = (game.dealer_pos) % n

    order = []
    for i in range(n):
        idx = (start + i) % n
        order.append(game.players[idx])
    return order


def run_ev_calculator(manager: LessonManager):
    """Run the interactive EV calculator."""
    while True:
        clear_screen()
        print_header("EV Calculator", "Calculate Expected Value for any situation")

        console.print("[dim]  Enter your hand and the situation to calculate EV.[/dim]")
        console.print("[dim]  Card format: As, Kh, Td, 2c (rank + suit)[/dim]")
        console.print()

        # Get hole cards
        try:
            cards_str = console.input("  [bold]Your hole cards (e.g., 'As Kh'): [/bold]").strip()
        except (EOFError, KeyboardInterrupt):
            return

        if cards_str.lower() == "q":
            return

        try:
            parts = cards_str.split()
            if len(parts) != 2:
                console.print("[red]  Enter exactly 2 cards.[/red]")
                get_input("[dim]Press Enter...[/dim] ")
                continue
            hole_cards = [Card.from_str(p) for p in parts]
        except (KeyError, IndexError, ValueError):
            console.print("[red]  Invalid card format. Use rank+suit like 'As', 'Kh'.[/red]")
            get_input("[dim]Press Enter...[/dim] ")
            continue

        # Get community cards
        try:
            comm_str = console.input("  [bold]Community cards (empty for preflop): [/bold]").strip()
        except (EOFError, KeyboardInterrupt):
            return

        community = []
        if comm_str and comm_str.lower() != "q":
            try:
                community = [Card.from_str(p) for p in comm_str.split()]
            except (KeyError, IndexError, ValueError):
                console.print("[red]  Invalid community cards.[/red]")
                get_input("[dim]Press Enter...[/dim] ")
                continue

        # Get pot and bet
        try:
            pot_str = console.input("  [bold]Pot size (chips): [/bold]").strip()
            pot_size = float(pot_str)
        except (ValueError, EOFError, KeyboardInterrupt):
            console.print("[red]  Enter a number.[/red]")
            get_input("[dim]Press Enter...[/dim] ")
            continue

        try:
            bet_str = console.input("  [bold]Bet to call (0 if no bet): [/bold]").strip()
            bet_size = float(bet_str)
        except (ValueError, EOFError, KeyboardInterrupt):
            console.print("[red]  Enter a number.[/red]")
            get_input("[dim]Press Enter...[/dim] ")
            continue

        # Calculate
        console.print()
        console.print("[dim]  Calculating equity (Monte Carlo simulation)...[/dim]")

        equity = hand_strength(hole_cards, community, num_opponents=1, iterations=1000)

        show_hole_cards(HoleCards(hole_cards))
        if community:
            show_community_cards(community)

        pct = hand_percentile(HoleCards(hole_cards))
        result = action_recommendation(equity, pot_size, bet_size, pct)
        show_ev_calculator_result(result)

        console.print()
        show_real_life_tip(
            "Use this same EV framework for any decision with uncertain outcomes. "
            "Estimate probabilities, calculate payoffs, and choose the highest EV option."
        )

        console.print()
        choice = get_input("[bold]Calculate another? (y/n): [/bold]", ["y", "n", "q"])
        if choice in ("n", "q"):
            return


def run_scenario(scenario_idx: int, manager: LessonManager):
    """Run a single scenario challenge."""
    if scenario_idx < 0 or scenario_idx >= len(SCENARIO_CHALLENGES):
        return

    scenario = SCENARIO_CHALLENGES[scenario_idx]

    clear_screen()
    print_header(scenario["title"], scenario["description"])

    console.print(Panel(
        f"[bold cyan]Concept: {scenario['concept']}[/bold cyan]",
        border_style="cyan",
    ))

    # Setup
    show_lesson_content("Situation", scenario["setup"])

    # Show cards if applicable
    if scenario["hole_cards"]:
        show_cards(scenario["hole_cards"], "Your Hand")
    if scenario.get("opponent_cards"):
        show_cards(scenario["opponent_cards"], "Opponent's Hand")
    if scenario.get("community"):
        show_community_cards(scenario["community"])

    console.print()

    # Question
    console.print(Panel(scenario["question"], border_style="yellow", padding=(1, 2)))
    console.print()

    for i, opt in enumerate(scenario["options"], 1):
        console.print(f"  [bold]{i}.[/bold] {opt}")

    console.print()
    valid = [str(i) for i in range(1, len(scenario["options"]) + 1)]
    answer = get_input("[bold]Your answer: [/bold]", valid + ["q"])
    if answer == "q":
        return

    selected = scenario["options"][int(answer) - 1]
    is_correct = selected == scenario["correct"]

    console.print()
    show_quiz_result(is_correct, scenario["explanation"])

    if scenario.get("real_life"):
        console.print()
        show_real_life_tip(scenario["real_life"])

    if is_correct:
        manager.complete_scenario(scenario["id"])

    get_input("[dim]Press Enter to return...[/dim] ")


def run_scenarios_mode(manager: LessonManager):
    """Run the scenario challenges mode."""
    while True:
        clear_screen()
        choice = show_scenario_select(manager)
        if choice == "q":
            return

        run_scenario(int(choice) - 1, manager)


def run_glossary(manager: LessonManager):
    """Run the glossary browser."""
    while True:
        clear_screen()
        choice = show_glossary_menu()
        if choice == "q":
            return

        terms = list(GLOSSARY.keys())
        idx = int(choice) - 1
        if 0 <= idx < len(terms):
            term = terms[idx]
            clear_screen()
            print_header("Game Theory Glossary")
            show_glossary_entry(term, GLOSSARY[term])
            console.print()
            get_input("[dim]Press Enter to go back...[/dim] ")


def run_stats(manager: LessonManager):
    """Show player stats and progress."""
    clear_screen()
    print_header("Stats & Progress")

    progress = manager.get_overall_progress()

    # Overall progress
    console.print(f"  [bold]Sessions:[/bold] {progress['sessions']}")
    console.print(f"  [bold]Lessons Completed:[/bold] {progress['lessons_done']}/6")
    console.print(f"  [bold]Scenarios Completed:[/bold] {progress['scenarios_done']}/8")
    console.print()

    # Lesson scores
    from lessons.content import LESSONS
    console.print("[bold cyan]  Lesson Scores:[/bold cyan]")
    for num in range(1, 7):
        score = manager.get_lesson_score(num)
        completed = manager.is_lesson_complete(num)
        title = LESSONS[num]["title"]
        if score is not None:
            color = "green" if completed else "yellow"
            console.print(f"    [{color}]Lesson {num}: {title} — {score:.0f}%[/{color}]")
        else:
            console.print(f"    [dim]Lesson {num}: {title} — Not started[/dim]")

    console.print()
    show_stats(manager.get_practice_stats())

    console.print()
    get_input("[dim]Press Enter to return to menu...[/dim] ")


def main():
    """Main entry point."""
    # Check for --quick flag
    quick_mode = "--quick" in sys.argv

    if quick_mode:
        set_quick_mode(True)

    # Splash screen
    show_splash_screen()
    pause(1.0)

    # Load progress
    manager = LessonManager()
    manager.increment_sessions()

    # Main loop
    while True:
        clear_screen()
        choice = show_main_menu(manager)

        if choice == "1":
            # Lessons mode
            while True:
                clear_screen()
                lesson_choice = show_lesson_select(manager)
                if lesson_choice == "q":
                    break
                run_lesson(int(lesson_choice), manager)

        elif choice == "2":
            run_practice_mode(manager)

        elif choice == "3":
            run_ev_calculator(manager)

        elif choice == "4":
            run_scenarios_mode(manager)

        elif choice == "5":
            run_glossary(manager)

        elif choice == "s":
            run_stats(manager)

        elif choice == "q":
            console.print()
            console.print("[bold cyan]  Thanks for learning with Poker4U![/bold cyan]")
            console.print("[dim]  Remember: Great decisions come from great thinking.[/dim]")
            console.print()
            break


if __name__ == "__main__":
    main()
