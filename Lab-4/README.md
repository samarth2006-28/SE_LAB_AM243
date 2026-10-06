# Balloon Pop Lab

This project is a single-topic Balloon Pop game using **Pygame**. It
introduces students to size-aware click detection, entity variety, a
lives/miss system, and round timing, using a small, readable
object-oriented codebase.

---

## What's Provided

A working Balloon Pop game with:

- Balloons that spawn at the top at random sizes and fall toward the
  bottom at random speeds
- Clicking a balloon pops it and awards points; letting one fall past
  the bottom is currently ignored
- A running score display

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left-click a balloon to pop it before it reaches the
bottom.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix the click-detection bug

> A click is supposed to pop a balloon whenever it lands reasonably
> close to that balloon's center - anywhere within its visible circle.
> In the current build, `check_pop` (in `game/click_detection.py`)
> computes the *squared* distance from the click to the balloon's
> center, but compares it directly against the balloon's plain
> (non-squared) `radius`. Squared distance grows much faster than
> linear distance, so this comparison only succeeds when the click
> lands within a few pixels of dead-center - anywhere close to the
> visible edge of the balloon fails to register at all, even though it
> clearly looks like a hit. Fix the check so it compares actual
> distance to the balloon's actual radius.

### Task 2: Implement different balloon types

> Introduce at least three balloon types: a normal balloon (regular
> points), a bonus balloon (more points), and a penalty balloon (which
> reduces the score, or has some other clearly defined negative
> effect). Give each type its own color so they're easy to tell apart,
> and make sure the correct effect happens when each type is popped.

### Task 3: Implement a lives/miss system

> Add 3 lives. Whenever a balloon reaches the bottom of the screen
> without being popped, the player should lose a life. Display the
> remaining lives, and end the game once they reach zero. Popping a
> balloon should never cost a life, no matter its type.

### Task 4: Implement a timed round

> Add a 30-second countdown for the round. Display the remaining time
> on screen. Once it reaches zero (or lives run out, once Task 3 is
> done), stop spawning and accepting balloons, show the final score
> clearly, and provide a way to start a new round with the score,
> lives, and timer all reset.

---

## Expected Behavior

- Clicking on a balloon should reliably pop it - not just when you
  happen to click exactly on its center pixel. Test this by clicking
  normally, the way you would in actual play, not by aiming with
  pixel-perfect precision.
- Balloon types are visually distinguishable and correctly affect the
  score when popped.
- Letting a balloon fall past the bottom costs a life; popping one
  never does, regardless of type.
- The round ends when time runs out or lives reach zero, whichever
  comes first, with the final score shown clearly and a way to start
  again.

---

## Folder Structure

```
balloon-pop/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── balloon.py
│   ├── click_detection.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
