# 🃏 Poker4U — *Game Theory for Everyone*

> **Poker is the vehicle. Decision-making is the destination.**  
> Learn to think in expected value, pot odds, and Nash-style logic — with zero real money and a whole lot of fun.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 What is this?

**Poker4U** is an **educational** Texas Hold'em game that uses poker as a teaching tool for **game theory** and **rational decision-making**. You get:

- **6 structured lessons** — Hand rankings, EV, pot odds, position, ranges, Nash basics  
- **Practice mode** — Play full hands vs 3 AI opponents (Tight, Loose, GTO) with live EV feedback  
- **EV calculator** — Plug in your hand, pot, and bet; get fold/call/raise recommendations  
- **8 scenario challenges** — Situational quizzes with explanations  
- **Glossary** — Every concept with a poker example + real-life application  

No gambling. No real money. Just chips, math, and “*why did I call that?*” moments that actually teach you something.

---

## ✨ Why should I care?

| In poker you learn…        | In life you use it for…              |
|---------------------------|--------------------------------------|
| Expected value (EV)       | Any decision with uncertain outcomes |
| Pot odds & equity         | When to commit vs when to walk away  |
| Position & information    | Negotiations, timing, who acts last   |
| Sunk costs don’t matter   | Quitting bad jobs, projects, habits  |
| Variance vs skill          | Judging process, not single outcomes |

So yeah — it’s a **poker game** that makes you better at **life decisions**. 🧠

---

## 🚀 Quick start

### 1. Clone & enter

```bash
git clone https://github.com/Lameda12/poker4u.git
cd poker4u
```

### 2. Install (one dependency!)

```bash
pip install -r requirements.txt
```

*(Uses [Rich](https://github.com/Textualize/rich) for a pretty terminal UI.)*

### 3. Run

```bash
python poker4u.py
```

**Want to skip animations and play faster?**

```bash
python poker4u.py --quick
```

Then pick from the main menu: Lessons, Practice, EV Calculator, Scenarios, or Glossary.

---

## 📂 Project layout

```
poker4u/
├── poker4u.py          # Entry point — menus, modes, game loop
├── requirements.txt    # rich
├── engine/             # Game logic
│   ├── cards.py        # Card, Deck, HoleCards
│   ├── evaluator.py    # Hand ranking, equity, outs
│   ├── game.py         # Texas Hold'em flow (streets, betting, showdown)
│   ├── game_theory.py  # EV, pot odds, action recommendation, glossary
│   └── ai_opponent.py   # Tight / Loose / GTO AI
├── lessons/
│   ├── content.py      # All 6 lesson texts
│   ├── lesson_manager.py  # Progress & stats (JSON)
│   └── scenarios.py    # Quizzes + 8 scenario challenges
└── ui/
    ├── menus.py        # Main menu, lesson/scenario/glossary menus
    ├── display.py      # Cards, tables, analysis, prompts
    └── animations.py   # Dealing, thinking, suspense (optional with --quick)
```

---

## 🎮 What you can do

| Mode              | What it does |
|-------------------|---------------|
| **Lessons**       | 6 lessons with intro → sections → real-life tip → quiz. Pass at 60% to “complete” it. |
| **Practice**      | Full ring vs 3 AIs. You see equity, pot odds, and EV for each decision; the game tells you if your choice was +EV. |
| **EV Calculator** | Enter hole cards, (optional) board, pot size, bet to call → get equity and fold/call/raise recommendation. |
| **Scenarios**      | 8 situational puzzles (e.g. “Do you call?”) with correct answer and explanation. |
| **Glossary**      | Browse terms (EV, pot odds, GTO, etc.) with definition, poker example, and real-life application. |
| **Stats**         | Sessions, lessons completed, scenario progress, and practice stats (hands, decision accuracy). |

---

## 🧩 Lessons at a glance

1. **Hand Rankings & Probability** — Base rates and “what beats what”.  
2. **Expected Value (EV)** — The single most important concept.  
3. **Pot Odds & Implied Odds** — When to call; rule of 2 and 4.  
4. **Position & Information** — Why acting last is an advantage.  
5. **Reading & Ranges** — Thinking in ranges and updating with evidence.  
6. **Nash Equilibrium & GTO Basics** — Push/fold and GTO vs exploitative play.

---

## 📜 Disclaimer

Poker4U is for **education and entertainment** only. It uses virtual chips, not real money, and is not affiliated with any gambling product. The goal is to teach game-theoretic and probabilistic thinking, not to encourage gambling.

---

## 🤝 Contributing

Found a bug or have an idea? Open an [issue](https://github.com/Lameda12/poker4u/issues) or a [pull request](https://github.com/Lameda12/poker4u/pulls). New lessons, scenarios, or glossary entries are especially welcome.

---

**Play. Learn. Make better decisions.**  
— [Poker4U](https://github.com/Lameda12/poker4u) ♠️♥️♣️♦️

##LICENSE

MIT

