## Author

Dmytro Tarasenko
- GitHub: https://github.com/Wolfs0ng
- Contact: nemesidik@gmail.com

This project is proprietary. Viewing only.

# 🩸 Carnage Club

> **Carnage Club** is:  
> **a tactical duel-based combat game where you fight not numbers, but a mind that remembers you.**

---

## 🎮 Core Concept

**Carnage Club** is a singleplayer mobile game — a modern reinterpretation of classic browser games  
*“Carnage / Fight Club”*, redesigned with a strong focus on:

- tactical, turn-based dueling combat  
- adaptive AI that learns from the player  
- a dark gothic atmosphere  
- reading and outsmarting the opponent instead of chasing DPS  

Core philosophy of the project:
> **The world remembers your habits.**

---

## 📱 Platform & Format

- **Mobile first**
- **Singleplayer**
- Story-driven campaign
- Post-campaign infinite / replayable mode
- Engine: **Unity 6.x**

---

## 🎨 Visual Style

### Mood
- Dark gothic atmosphere
- Inspirations: Bloodborne, baroque aesthetics, dark luxury
- A sense of an old world filled with rituals, decay, and blood

### Color Palette
- ⚫ **Black** — base tone, atmosphere
- 🟡 **Gold** — ornaments, doors, key elements
- 🔴 **Red** — blood, traces of battle

### UI
- Entire game runs inside a Canvas
- Dark UI with strong contrast accents
- Health / Guard bars
- Popup / Hint / Notification systems with pooling
- Preloader background: stairs leading to a gothic cathedral with open doors

---

## 🗺️ Map & Progression

Before each fight, the player navigates a **top-down node-based map** (similar to *Slay the Spire*).

### Node Types
- ⚔ Combat
- 👑 Boss
- 🔥 Bonfire (rest)
- 🧙‍♂️ Merchant
- ❓ Events (extensible)

### Rules
- Only connected and unlocked nodes are visible
- Backtracking is allowed
- Penalties for excessive movement are still in design

---

## ⚔️ Combat System

### Directions
- **4 attack directions**
- **4 defense directions**
- Support for multi-direction actions (1–3 at once)

### Core Rules
- Turn-based duel combat
- Each attack direction is resolved independently
- Defense may cover multiple directions

### Possible Outcomes
- Damage HP
- Damage Guard
- Block
- Parry
- Guard Break
- Critical Hit

---

## 🧬 Character Stats

| Stat | Description |
|----|----|
| **Strength** | Attack power and guard break potential |
| **Fortitude** | HP, endurance, Guard Stance strength |
| **Mastery** | Stamina and special effect activation chance |
| **Focus** | Enemy reading, AI learning speed, reduced enemy adaptation |

**Focus** is a unique stat that directly interacts with AI systems.

---

## 🧠 AI — Core Feature of the Game

AI is built as a **layered knowledge and decision-making system**.

### 0️⃣ Telemetry (Foundation)
- Records every combat turn
- Captures before/after states (HP, Guard)
- Player and AI actions
- Per-direction combat outcomes
- Human-readable debug logs

---

### 1️⃣ Player Battle Behavior Knowledge
**Persistent global memory of player behavior:**

- Attack and defense direction frequencies
- Direction pattern usage (DirectionMask)
- Bigram and trigram sequences across turns
- Rolling window statistics
- Pattern efficiency (hit / block / damage)

> This knowledge persists between game sessions.

---

### 2️⃣ AI Reaction Knowledge (Action–Reaction Matrix)

Reaction matrices:
- AI attack → Player defense
- Player attack → AI defense

Tracked statistics:
- hit / block / parry
- HP damage / Guard damage
- critical hits, guard breaks

Evaluators:
- Best attack against a given defense mask
- Best defense against a given attack direction
- Cold-start fallback logic

This is a **separate layer** from player behavior knowledge.

---

### 3️⃣ Bandit Tactics *(planned)*
- Thompson Sampling / UCB
- Exploration budget
- Context-aware states (LowHP, AfterHit, Repetition, etc.)

---

### 4️⃣ GOAP + Soft FSM *(planned)*
- High-level goals:
  - Pressure
  - Punish
  - Survive
- FSM for concrete execution

---

### 5️⃣ Emotion System *(planned)*
- Aggression
- Fear
- Confidence

Emotions modify risk-taking and AI decision-making.

---

## 👑 Nemesis System

- When an enemy kills the player:
  - it evolves
  - becomes stronger
  - retains memory of past encounters
- Every enemy represents a personal history of conflict

---

## 🛠️ Technical Architecture

- Service Locator pattern
- Services implemented as plain C# (no MonoBehaviour unless required)
- Minimal use of Update loops
- Object Pooling
- ScriptableObject-based data containers
- Unit tests for services
- Unity-friendly SaveData DTOs

---

## 💰 Monetization

- Free-to-play
- Minimal banner ads
- Cosmetic content
- Special currency earnable through gameplay
- Optional voluntary support for the developer

---