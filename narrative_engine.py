# ============================================================
# ANI - ADAPTIVE NARRATIVE INTELLIGENCE
# STEP 13: JOURNEY MEMORY
# ============================================================


class NarrativeEngine:

    def __init__(self):

        # ----------------------------------------------------
        # STORY DEFINITIONS
        # ----------------------------------------------------

        self.stories = {

            "Inspired": {
                "opening": (
                    "The morning arrives with an unusual sense of "
                    "possibility. You feel that something meaningful "
                    "is waiting beyond the ordinary path."
                ),
                "tone": "hopeful"
            },

            "Curious": {
                "opening": (
                    "You notice something strange in the distance. "
                    "Most people would ignore it, but your curiosity "
                    "pulls you closer."
                ),
                "tone": "mysterious"
            },

            "Confused": {
                "opening": (
                    "You find yourself standing at a crossroads. "
                    "Every direction appears possible, yet none "
                    "seems obvious."
                ),
                "tone": "reflective"
            },

            "Unmotivated": {
                "opening": (
                    "The day feels heavier than usual. You have goals, "
                    "but taking the first step seems difficult."
                ),
                "tone": "encouraging"
            },

            "Calm": {
                "opening": (
                    "Everything around you becomes quieter. For once, "
                    "there is no need to rush. You simply observe "
                    "the world as it moves around you."
                ),
                "tone": "peaceful"
            },

            "Excited": {
                "opening": (
                    "Your energy rises as the world seems to open "
                    "before you. Something unexpected is about to happen."
                ),
                "tone": "energetic"
            }
        }


    # ========================================================
    # START STORY
    # ========================================================

    def start_story(self, emotion):

        if emotion not in self.stories:
            return None

        story = self.stories[emotion]


        # ----------------------------------------------------
        # INITIAL NARRATIVE STATE
        # ----------------------------------------------------

        state = {
            "confidence": 0,
            "curiosity": 0,
            "momentum": 0,
            "reflection": 0,
            "risk_taking": 0
        }


        # ----------------------------------------------------
        # EMOTIONAL BASELINE
        # ----------------------------------------------------

        if emotion == "Inspired":

            state["confidence"] = 2
            state["momentum"] = 2

        elif emotion == "Curious":

            state["curiosity"] = 3

        elif emotion == "Confused":

            state["reflection"] = 2

        elif emotion == "Unmotivated":

            state["momentum"] = -2
            state["confidence"] = -1

        elif emotion == "Calm":

            state["reflection"] = 3

        elif emotion == "Excited":

            state["momentum"] = 3
            state["risk_taking"] = 2


        # ----------------------------------------------------
        # JOURNEY MEMORY
        # ----------------------------------------------------

        session = {

            "emotion": emotion,

            "tone": story["tone"],

            "stage": 1,

            "choices": [],

            "history": [
                {
                    "type": "opening",
                    "text": story["opening"]
                }
            ],

            "state": state,

            "journey_memory": {

                "starting_emotion": emotion,

                "decisions": [],

                "state_snapshots": [
                    {
                        "stage": 1,
                        "state": state.copy()
                    }
                ],

                "dominant_trait": None,

                "completed": False

            }
        }


        return {

            "session": session,

            "story": story["opening"],

            "tone": story["tone"],

            "choices": self.get_choices(
                emotion,
                stage=1
            )

        }


    # ========================================================
    # CHOICES
    # ========================================================

    def get_choices(
        self,
        emotion,
        stage
    ):

        if stage == 1:

            choices = {

                "Inspired": [
                    "Follow the mysterious path",
                    "Build something new",
                    "Help someone along the way"
                ],

                "Curious": [
                    "Investigate the mystery",
                    "Ask someone for information",
                    "Observe quietly"
                ],

                "Confused": [
                    "Take a moment to think",
                    "Choose the unfamiliar path",
                    "Ask for guidance"
                ],

                "Unmotivated": [
                    "Take one small step",
                    "Remember why you started",
                    "Rest and begin again"
                ],

                "Calm": [
                    "Walk into nature",
                    "Reflect on your journey",
                    "Follow the sound of water"
                ],

                "Excited": [
                    "Run toward the opportunity",
                    "Take the boldest path",
                    "Bring someone with you"
                ]
            }

            return choices.get(
                emotion,
                []
            )


        if stage == 2:

            return [
                "Continue forward",
                "Explore another possibility",
                "Reflect on what happened"
            ]


        if stage == 3:

            return [
                "Take the final step",
                "Look back at the journey",
                "Choose a different direction"
            ]


        return []


    # ========================================================
    # ADAPT STORY
    # ========================================================

    def adapt_story(
        self,
        session,
        choice
    ):

        if not session:
            return None


        emotion = session["emotion"]

        stage = session["stage"]


        # ----------------------------------------------------
        # RECORD DECISION
        # ----------------------------------------------------

        session["choices"].append(choice)


        session["journey_memory"]["decisions"].append({

            "stage": stage,

            "choice": choice

        })


        # ----------------------------------------------------
        # UPDATE STATE
        # ----------------------------------------------------

        self.update_state(
            session,
            choice
        )


        # ----------------------------------------------------
        # STAGE 1 → STAGE 2
        # ----------------------------------------------------

        if stage == 1:

            continuation = self.stage_two_story(
                session
            )

            session["stage"] = 2


            session["history"].append({

                "type": "choice",

                "choice": choice,

                "text": continuation

            })


            self.save_state_snapshot(
                session
            )


            return {

                "session": session,

                "story": continuation,

                "tone": session["tone"],

                "choices": self.get_choices(
                    emotion,
                    stage=2
                )

            }


        # ----------------------------------------------------
        # STAGE 2 → STAGE 3
        # ----------------------------------------------------

        if stage == 2:

            continuation = self.stage_three_story(
                session
            )

            session["stage"] = 3


            session["history"].append({

                "type": "choice",

                "choice": choice,

                "text": continuation

            })


            self.save_state_snapshot(
                session
            )


            return {

                "session": session,

                "story": continuation,

                "tone": session["tone"],

                "choices": self.get_choices(
                    emotion,
                    stage=3
                )

            }


        # ----------------------------------------------------
        # STAGE 3 → ENDING
        # ----------------------------------------------------

        if stage == 3:

            ending = self.generate_ending(
                session
            )


            session["stage"] = 4


            session["journey_memory"]["completed"] = True


            session["history"].append({

                "type": "ending",

                "text": ending

            })


            self.save_state_snapshot(
                session
            )


            dominant_trait = self.get_dominant_trait(
                session["state"]
            )


            session["journey_memory"][
                "dominant_trait"
            ] = dominant_trait


            return {

                "session": session,

                "story": ending,

                "tone": session["tone"],

                "choices": [],

                "completed": True

            }


        return None


    # ========================================================
    # SAVE STATE SNAPSHOT
    # ========================================================

    def save_state_snapshot(
        self,
        session
    ):

        snapshot = {

            "stage": session["stage"],

            "state": session["state"].copy()

        }


        session[
            "journey_memory"
        ][
            "state_snapshots"
        ].append(snapshot)


    # ========================================================
    # UPDATE NARRATIVE STATE
    # ========================================================

    def update_state(
        self,
        session,
        choice
    ):

        state = session["state"]


        # ----------------------------------------------------
        # UNMOTIVATED
        # ----------------------------------------------------

        if choice == "Take one small step":

            state["momentum"] += 2
            state["confidence"] += 1


        elif choice == "Remember why you started":

            state["confidence"] += 2
            state["reflection"] += 1


        elif choice == "Rest and begin again":

            state["reflection"] += 2


        # ----------------------------------------------------
        # CURIOUS
        # ----------------------------------------------------

        elif choice == "Investigate the mystery":

            state["curiosity"] += 2
            state["risk_taking"] += 1


        elif choice == "Ask someone for information":

            state["curiosity"] += 1
            state["confidence"] += 1


        elif choice == "Observe quietly":

            state["curiosity"] += 1
            state["reflection"] += 2


        # ----------------------------------------------------
        # INSPIRED
        # ----------------------------------------------------

        elif choice == "Follow the mysterious path":

            state["risk_taking"] += 2
            state["momentum"] += 2


        elif choice == "Build something new":

            state["confidence"] += 2
            state["momentum"] += 2


        elif choice == "Help someone along the way":

            state["confidence"] += 1
            state["reflection"] += 2


        # ----------------------------------------------------
        # CONFUSED
        # ----------------------------------------------------

        elif choice == "Take a moment to think":

            state["reflection"] += 2


        elif choice == "Choose the unfamiliar path":

            state["risk_taking"] += 2
            state["momentum"] += 1


        elif choice == "Ask for guidance":

            state["confidence"] += 1
            state["reflection"] += 1


        # ----------------------------------------------------
        # CALM
        # ----------------------------------------------------

        elif choice == "Walk into nature":

            state["reflection"] += 2


        elif choice == "Reflect on your journey":

            state["reflection"] += 3


        elif choice == "Follow the sound of water":

            state["curiosity"] += 1
            state["reflection"] += 2


        # ----------------------------------------------------
        # EXCITED
        # ----------------------------------------------------

        elif choice == "Run toward the opportunity":

            state["momentum"] += 2
            state["risk_taking"] += 2


        elif choice == "Take the boldest path":

            state["risk_taking"] += 3
            state["confidence"] += 1


        elif choice == "Bring someone with you":

            state["confidence"] += 1
            state["reflection"] += 1


        # ----------------------------------------------------
        # STAGE 2
        # ----------------------------------------------------

        elif choice == "Continue forward":

            state["momentum"] += 2
            state["confidence"] += 1


        elif choice == "Explore another possibility":

            state["curiosity"] += 2
            state["risk_taking"] += 1


        elif choice == "Reflect on what happened":

            state["reflection"] += 2


        # ----------------------------------------------------
        # STAGE 3
        # ----------------------------------------------------

        elif choice == "Take the final step":

            state["momentum"] += 2
            state["confidence"] += 2


        elif choice == "Look back at the journey":

            state["reflection"] += 3


        elif choice == "Choose a different direction":

            state["curiosity"] += 2
            state["risk_taking"] += 2


    # ========================================================
    # GET DOMINANT TRAIT
    # ========================================================

    def get_dominant_trait(
        self,
        state
    ):

        return max(
            state,
            key=state.get
        )


    # ========================================================
    # STAGE TWO
    # ========================================================

    def stage_two_story(
        self,
        session
    ):

        emotion = session["emotion"]

        state = session["state"]


        if emotion == "Inspired":

            if state["momentum"] >= 4:

                return (
                    "Your inspiration becomes movement. "
                    "The idea that once existed only in your "
                    "imagination now begins taking shape around you."
                )

            return (
                "You hold onto the feeling of possibility and begin "
                "looking for a meaningful direction."
            )


        if emotion == "Curious":

            if state["curiosity"] >= 5:

                return (
                    "Your curiosity pulls you deeper into the mystery. "
                    "The clues are beginning to connect, but the answers "
                    "create even more questions."
                )

            return (
                "You discover a small clue. It is not enough to explain "
                "everything, but it gives you a direction to follow."
            )


        if emotion == "Confused":

            if state["reflection"] >= 4:

                return (
                    "You stop trying to force an immediate answer. "
                    "With a little reflection, the crossroads begins "
                    "to look less frightening."
                )

            return (
                "The uncertainty remains, but you realize that standing "
                "still will not reveal which path is yours."
            )


        if emotion == "Unmotivated":

            if state["momentum"] >= 0:

                return (
                    "Something has changed. The weight has not completely "
                    "disappeared, but you have started moving. "
                    "One small action has created momentum."
                )

            return (
                "You are still struggling to move forward. "
                "Instead of judging yourself, you decide to understand "
                "what is holding you back."
            )


        if emotion == "Calm":

            return (
                "The world remains quiet around you. "
                "The more you slow down, the more clearly you notice "
                "the thoughts that normally disappear beneath the noise."
            )


        if emotion == "Excited":

            if state["risk_taking"] >= 4:

                return (
                    "Your excitement turns into bold action. "
                    "You step beyond what is familiar and discover "
                    "that the opportunity is larger than you imagined."
                )

            return (
                "Your excitement gives you energy, but you realize "
                "that energy needs direction if it is going to become "
                "something meaningful."
            )


        return (
            "The journey continues, shaped by the decision you have made."
        )


    # ========================================================
    # STAGE THREE
    # ========================================================

    def stage_three_story(
        self,
        session
    ):

        state = session["state"]

        emotion = session["emotion"]


        strongest_trait = self.get_dominant_trait(
            state
        )


        descriptions = {

            "confidence": (
                "You begin to trust yourself more than you did "
                "when the journey started."
            ),

            "curiosity": (
                "Your desire to understand the world has become "
                "stronger than your fear of the unknown."
            ),

            "momentum": (
                "The most important change is movement. "
                "You are no longer standing where you started."
            ),

            "reflection": (
                "You have discovered that understanding yourself "
                "can be just as important as reaching the destination."
            ),

            "risk_taking": (
                "You have become willing to step beyond what is familiar "
                "and accept uncertainty."
            )
        }


        return (
            "The journey reaches its final stage. "
            + descriptions[strongest_trait]
            + " "
            "Your original emotional state was "
            + emotion
            + ", but your choices have gradually changed "
            "the direction of the experience."
        )


    # ========================================================
    # ENDING
    # ========================================================

    def generate_ending(
        self,
        session
    ):

        emotion = session["emotion"]

        state = session["state"]


        strongest_trait = self.get_dominant_trait(
            state
        )


        if strongest_trait == "confidence":

            ending = (
                "You reach the end of the journey and realize "
                "that the greatest change was not outside you. "
                "You learned to trust your own ability to move forward."
            )


        elif strongest_trait == "curiosity":

            ending = (
                "The journey ends with more questions than answers. "
                "Instead of feeling disappointed, you smile. "
                "You have discovered that curiosity is not a destination. "
                "It is a way of seeing the world."
            )


        elif strongest_trait == "momentum":

            ending = (
                "You look back at the place where you started. "
                "The distance may not seem enormous, but you remember "
                "how difficult the first step felt. "
                "You kept moving, and that changed everything."
            )


        elif strongest_trait == "reflection":

            ending = (
                "The journey becomes quiet. "
                "You realize that some of life's most important answers "
                "appear only when you give yourself enough space to listen."
            )


        else:

            ending = (
                "You reach the edge of the familiar world and realize "
                "that you crossed it willingly. "
                "The future remains uncertain, but uncertainty no longer "
                "feels like something you need to fear."
            )


        return (
            ending
            + " "
            + "Your journey began while you felt "
            + emotion.lower()
            + ", but your decisions shaped something different."
        )


    # ========================================================
    # JOURNEY SUMMARY
    # ========================================================

    def get_journey_summary(
        self,
        session
    ):

        if not session:
            return None


        memory = session["journey_memory"]

        state = session["state"]


        dominant_trait = (
            memory["dominant_trait"]
            or self.get_dominant_trait(state)
        )


        trait_names = {

            "confidence": "confidence",

            "curiosity": "curiosity",

            "momentum": "momentum",

            "reflection": "reflection",

            "risk_taking": "risk-taking"

        }


        summary = {

            "starting_emotion":
                memory["starting_emotion"],

            "decisions":
                memory["decisions"],

            "final_state":
                state.copy(),

            "dominant_trait":
                trait_names[dominant_trait],

            "stages_completed":
                session["stage"],

            "completed":
                memory["completed"]

        }


        return summary