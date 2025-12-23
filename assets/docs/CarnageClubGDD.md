## Author

Dmytro Tarasenko
- GitHub: https://github.com/Wolfs0ng
- Contact: nemesidik@gmail.com

This project is proprietary. Viewing only.

# 🩸 Carnage Club

> **Carnage Club** is:  
> **a tactical duel combat game where you fight not numbers, but a mind that remembers you.**

---

## 🎮 Core Idea

**Carnage Club** is a single-player mobile game focused on:

- tactical turn-based duels
- adaptive AI that learns from the player
- dark gothic setting
- reading the opponent instead of a DPS race
- DnD-style character progression

Core concept:
> **The world remembers your habits.**

---

## 📱 Platform & Format

- **Mobile first**
- **Singleplayer**
- Campaign with story progression
- After the campaign — a semi-endless mode
- Engine: **Unity 6.x**

---

## 🎨 Visual Style

### Atmosphere
- Dark gothic tone
- Inspirations: Bloodborne, baroque, dark luxury
- A sense of an old world, rituals, and blood

### Color Palette
- ⚫ **Black** — base, atmosphere
- 🟡 **Gold** — ornaments, doors, key elements
- 🔴 **Red** — blood, traces of battle

### UI
- Dark interface with contrast accents
- Health / Guard / Stamina bars
- Popup / Hint / Notification systems with pooling
- Preloader: stairs to a gothic cathedral with open doors

---

## 🗺️ Map & Progression

Before a fight, the player moves across a **top-down node-based map** (similar to *Slay the Spire*).

### Node Types
- ⚔ Fight
- 👑 Boss
- 🔥 Bonfire (rest)
- 🧙‍♂️ Merchant
- ❓ Events (expandable)

### Mechanics
- Only connected and unlocked nodes are visible
- Backtracking is allowed
- Penalty system for extra movement — in design

---

## ⚔️ Combat System

### Directions
- **4 attack directions**
- **4 defense directions**
- Multi-direction support (1–3 simultaneously)
- Action points (skills, quick-access items, etc.)

### Combat Principles
- Turn-based duel combat
- Selected attack directions (player) and defense directions (opponent), and vice versa, are checked; on match, block/parry/etc. triggers
- Each attack direction is resolved separately
- Defense can cover multiple directions
- After each round, a log (and visual elements) explains enemy attack/defense choices so the player can adapt
- The enemy does not attack randomly — it thinks, plans, tests, and remembers

### Possible Outcomes
- Damage HP (deal damage to enemy health)
- Damage Guard (deal damage to enemy Guard Stance)
- Block (block damage and avoid Guard damage)
- Parry (block the attack and respond into the attack zone) — in design

### Attack Effects
- Guard Break (Damage Guard reduced Guard Stance to 0 or below) — in design
- Critical (damage multiplied by a critical modifier) — in design
- Exhaust (stamina reduced to 0 or below) — in design

---

## 🧬 Character Stats

Still in design and may change.

| Stat          | Description                                                    |
|---------------|----------------------------------------------------------------|
| **Strength**  | Hit power, block penetration                                   |
| **Fortitude** | HP, endurance, Guard Stance strength                           |
| **Mastery**   | Stamina, chance of special effects                             |
| **Focus**     | Reading the enemy, AI learning speed, reduced enemy adaptation |

**Focus** is the key unique stat that directly interacts with AI.

---

## 🧩 Skills

In design.  
All skills consume an **Action Point**.  
A skill can be targeted (choose one or multiple directions) or simply activated.

Examples:
- **Piercing Strike** (next attack breaks through block and deals HP damage)
- **Mark** (choose a direction; next turn, a hit in that zone deals increased damage)
- **Disorientation** (next turn, a chosen attack or defense might fail)

---

## ✨ Abilities

In design.  
Can be passive or triggered (on conditions).

Passive examples:
- **Endurance** (increased HP)
- **Ambidexterity** (reduced penalties for a weapon in the off-hand)
- **See Weak Spots** (increased critical chance)

Triggered examples:
- **Cleave** (with a two-handed weapon, if a head hit was not blocked, deal damage for each unblocked direction top-down)
- **Bestial Reaction** (when hit into a parry direction, instead of taking HP damage you block, but take Guard damage)
- **Mighty Blow** (when hitting a block and triggering Guard Break, overflow damage goes to HP)

---

## 🎒 Inventory

In design.  
Equipable item list:

### Weapons
- Left hand (One-handed weapon, Two-handed weapon)
- Right hand (One-handed weapon — with weakened parameters, Shield)

### Armor
- Helmet
- Cloak
- Body armor
- Gloves
- Pants
- Belt
- Boots

### Accessories
- Amulet (one or multiple)
- Rings (2 or more)

### Quick Access Slots
In design.  
Items worn on the belt can be used during combat at the cost of the item and **Action Points**:
- Potions
- Grenades
- Thrown weapons
- Scrolls

### Weapons (Playstyle Impact)
In design.  
Weapon type and combinations (shield + one-handed, dual-wield, two-handed sword) change the playstyle.

Examples:
- Two-handed swords, halberds, axes enable cleave-related mechanics
- Two-handed hammers, maces enable debuffs during attacks
- One-handed weapon + shield grants two defense directions (or more)
- Dual one-handed weapons grant two attack directions

---

## 🧠 AI — Core Feature

AI is built as a **layered knowledge and decision-making system**.

### 0️⃣ Telemetry (foundation)
- Records every turn
- Pre/post states (HP, Guard)
- Player and AI actions
- Per-direction outcomes
- Human-readable debug logs

---

### 1️⃣ Player Battle Behavior Knowledge
**Global persistent memory of player behavior:**

- Attack/defense frequency per direction
- Direction patterns (DirectionMask)
- Bigrams and trigrams between turns
- Rolling window statistics
- Pattern efficiency (hit / block / damage)

> Knowledge persists between game sessions.

---

### 2️⃣ AI Reaction Knowledge (Action–Reaction Matrix)

Reaction matrices:
- AI attack → Player defend
- Player attack → AI defend

Collected stats:
- hit / block / parry
- HP / Guard damage
- critical, guard break

Evaluators:
- Best attack vs a specific defense
- Best defense vs a specific attack
- Cold-start fallback logic

This is a **separate layer** from player knowledge.

---

### 3️⃣ Bandit Tactics *(planned)*
- Thompson Sampling / UCB
- Exploration budget
- Context states (LowHP, AfterHit, Repetition, etc.)

---

### 4️⃣ GOAP + Soft FSM *(planned)*
- High-level goals:
  - Pressure
  - Punish
  - Survive
- FSM for executing concrete actions

---

### 5️⃣ Emotion System *(planned)*
- Aggression
- Fear
- Confidence

Emotions modify risk and AI decision-making.

---

## 👑 Nemesis System

- If an enemy kills the player:
  - it evolves (level increases, class changes/adapts)
  - becomes stronger (stat changes, new/upgraded perks/abilities)
- Each enemy becomes a story of rivalry

---

## 🛠️ Technical Architecture

- Service Locator
- Services are plain C# (no MonoBehaviour)
- Minimal use of Update
- Object Pooling
- ScriptableObjects for data
- Unit tests for services
- Unity-friendly SaveData DTO

---

## 💰 Monetization

- Free-to-play
- Minimal banner ads
- Cosmetic items
- Special currency obtainable through gameplay
- Optional voluntary author support (subscription for cosmetics or similar, enabling ads, etc.)

---
