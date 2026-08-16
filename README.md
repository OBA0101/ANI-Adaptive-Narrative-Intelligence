# ANI — Adaptive Narrative Intelligence

> An experimental adaptive storytelling system that explores how narrative experiences can respond to a user's emotional state and decisions.

## Overview

**Adaptive Narrative Intelligence (ANI)** is an interactive storytelling prototype designed to explore a simple question:

> **What if a story could respond to the person experiencing it?**

Instead of presenting every user with exactly the same narrative path, ANI uses an initial emotional state and subsequent user decisions to influence the direction of the story.

The system maintains a narrative state throughout the experience and updates that state as the user makes decisions.

---

## The Idea

Traditional digital stories generally follow a predetermined sequence:

```text
User
 ↓
Story
 ↓
Ending
```

ANI explores a more dynamic model:

```text
User Emotion
      ↓
Narrative State
      ↓
Story
      ↓
User Decision
      ↓
State Changes
      ↓
Adaptive Story
      ↓
New State
      ↓
Ending
```

The objective is to make the narrative feel responsive rather than completely predetermined.

---

## Current Features

### Emotional Starting Point

The user begins by selecting an emotional state:

* Inspired
* Curious
* Confused
* Unmotivated
* Calm
* Excited

The selected emotion establishes the initial narrative state.

### Narrative State

ANI currently tracks several narrative characteristics:

* Confidence
* Curiosity
* Momentum
* Reflection
* Risk-taking

These values can change according to the user's decisions.

### Interactive Decisions

At different stages of the story, the user is presented with choices.

Each choice can influence the narrative state differently.

### Journey Memory

ANI maintains information about the user's journey, including:

* Starting emotional state
* Decisions made
* Narrative state snapshots
* Current story stage
* Dominant narrative trait
* Completion status

### Adaptive Ending

The final narrative is influenced by the state that developed throughout the user's journey.

---

## Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML
* CSS
* JavaScript

### Development

* Visual Studio Code
* Git
* GitHub

---

## Project Structure

```text
ANI-Adaptive-Narrative-Intelligence/
│
├── app.py
├── narrative_engine.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    └── index.html
```

---

## How It Works

### 1. The user selects an emotion

For example:

```text
Unmotivated
```

ANI establishes an initial narrative state based on that emotion.

### 2. The story begins

The Narrative Engine generates an opening narrative appropriate to the selected emotional state.

### 3. The user makes a decision

The user chooses how they want to respond to the situation presented by the story.

### 4. ANI updates the narrative state

Different decisions influence different state variables.

For example:

```text
Take one small step

        ↓

Momentum +2
Confidence +1
```

### 5. The story adapts

The next narrative stage is generated using the updated state.

### 6. The journey is remembered

ANI records decisions and state changes throughout the experience.

### 7. The journey ends

The final narrative is influenced by the dominant state that developed during the experience.

---

## Example Journey

A user begins feeling:

```text
Unmotivated
```

The initial state may contain:

```text
Confidence: -1
Momentum: -2
```

The user chooses:

```text
Take one small step
```

The system updates the state:

```text
Confidence: 0
Momentum: 0
```

The user then continues making decisions.

By the end of the experience, **momentum** may become the dominant narrative characteristic.

The resulting ending therefore reflects the journey rather than simply displaying a fixed ending.

---

## Research Context

ANI is being developed as an experimental prototype exploring the intersection of:

* Artificial Intelligence
* Interactive storytelling
* Human-computer interaction
* Personalization
* Emotional state
* Narrative systems
* Generative and adaptive experiences

The project was conceived in connection with research and presentation work around **Generative AI and the future of storytelling**.

ANI is currently a prototype and is intended to provide a foundation for further experimentation and research.

---

## Current Architecture

The system is currently organized around three main layers:

```text
                ┌─────────────────────┐
                │      User Interface │
                │ HTML / CSS / JS     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Flask Backend    │
                │      app.py         │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Narrative Engine   │
                │ narrative_engine.py │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Narrative State    │
                │ + Journey Memory    │
                └─────────────────────┘
```

---

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/OBA0101/ANI-Adaptive-Narrative-Intelligence.git
```

### 2. Enter the project directory

```bash
cd ANI-Adaptive-Narrative-Intelligence
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## Future Development

ANI is intentionally being developed incrementally.

Planned improvements include:

* More sophisticated narrative-state modeling
* Larger branching story structures
* Persistent user profiles
* More advanced emotional-state modeling
* Natural-language interaction
* AI-generated narrative passages
* More sophisticated personalization
* Narrative analytics
* User journey visualization
* Long-term memory
* Multiple story worlds
* Evaluation of user engagement and narrative satisfaction

---

## Project Status

**Status:** Active Prototype

ANI is currently a working experimental prototype rather than a production-ready storytelling platform.

The current implementation focuses on establishing the foundation for adaptive narrative experiences.

---

## Author

**Obakeng Sithole**

Business Intelligence & Data Analytics

Interests include:

* Data Analytics
* Artificial Intelligence
* Python
* Business Intelligence
* Interactive Systems
* Technology Innovation
* Adaptive Experiences

---

## License

This project currently does not specify an open-source license.

Please contact the author before using the project commercially or redistributing substantial portions of the code.
