"""
    Main function
"""
from manim import *
from math import cos, sin

import random as rd


WORLD_SIZE : int = 15
DINO_REACH : int = 5

BIGGER_RAD : float = 2.5
SMALLR_RAD : float = BIGGER_RAD * PI / (2 * WORLD_SIZE)

SCORE : int = 0
COST_BR : int = 1
COST_BT : int = 2
MALUS_EGG : int = 4
BONUS_EGG : int = 8

NB_MOVES : int = 0
def show_state():
    dot_state = [s if s in ["R", "T"] else "." for s in STATE]
    print(f"""Step n°{NB_MOVES} | Current state : {"".join(dot_state)} | Score = {SCORE}""")

def get_color_from_state(s):
    if s == "R":
        return GRAY_B
    if s == "T":
        return ORANGE
    return WHITE

STATE = [rd.choice([" ", "R", "T"]) for _ in range(WORLD_SIZE)]
TXT_STATE = [Text(s).set_color(get_color_from_state(s)).scale(0.4).move_to(BIGGER_RAD * cos(TAU * i / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * i / WORLD_SIZE) * UP) for i, s in enumerate(STATE)]
SCORE_TEXT_BASE  = Text("Score: ").scale(0.5).to_corner(DL)
SCORE_TEXT = Text(f"{SCORE}").scale(0.5).next_to(SCORE_TEXT_BASE, RIGHT)

NB_MOVES_TEXT_BASE = Text("Step n°").scale(0.35).to_corner(UL)
NB_MOVES_TEXT = Text("").scale(0.35).next_to(NB_MOVES_TEXT_BASE, RIGHT)

ACTION_TEXT_BASE = Text("Current Action : ").scale(0.35).next_to(NB_MOVES_TEXT_BASE, DOWN)
ACTION_TEXT = Text("").scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)

class BuildBackground(Scene):
    def construct(self):
        animals = []
        for i in range(WORLD_SIZE):
            theta = TAU * i / WORLD_SIZE
            x_pos = BIGGER_RAD * cos(theta)
            y_pos = BIGGER_RAD * sin(theta)
            animals.append(Circle(radius = SMALLR_RAD, color = WHITE, stroke_width = 1).move_to(x_pos * RIGHT + y_pos * UP))

        self.play(Write(SCORE_TEXT_BASE), Write(SCORE_TEXT), Write(ACTION_TEXT_BASE), Write(NB_MOVES_TEXT_BASE))
        self.add(*animals)
        self.wait()

class ActivateRabbits(Scene):
    def construct(self):
        global STATE, TXT_STATE, ACTION_TEXT
        self.remove(ACTION_TEXT)
        ACTION_TEXT = Text("ActivateRabbits", color = GRAY_B).scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)
        self.play(Write(ACTION_TEXT))

        rabbit_pos = [i for i, s in enumerate(STATE) if s == "R"]
        potential_next = []
        for p in rabbit_pos:
            if (p + 1) % WORLD_SIZE not in potential_next:
                potential_next.append((p + 1) % WORLD_SIZE)
            if (WORLD_SIZE + p - 1) % WORLD_SIZE not in potential_next:
                potential_next.append((WORLD_SIZE + p - 1) % WORLD_SIZE)

        
        for p in potential_next:
            if STATE[p] == " ":
                STATE[p] = "R"
                self.remove(TXT_STATE[p])
                TXT_STATE[p] = Text(STATE[p]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * p / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * p / WORLD_SIZE) * UP)
                TXT_STATE[p].set_color(get_color_from_state(STATE[p]))
                self.play(Write(TXT_STATE[p]))
        self.wait()

class ActivateTigers(Scene):
    def construct(self):
        global STATE, TXT_STATE, ACTION_TEXT
        self.remove(ACTION_TEXT)
        ACTION_TEXT = Text("ActivateTigers", color = ORANGE).scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)
        self.play(Write(ACTION_TEXT))
        tigers_pos = [i for i, t in enumerate(STATE) if t == "T"]
        potential_reprod_cells = [(i+1)%WORLD_SIZE for i in tigers_pos] + [(i+2)%WORLD_SIZE for i in tigers_pos]
        potential_reprod_cells = list(set(potential_reprod_cells))

        for t in tigers_pos:
            STATE[t] = " "
            self.remove(TXT_STATE[t])
            TXT_STATE[t] = Text(STATE[t]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * t / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * t / WORLD_SIZE) * UP)
            TXT_STATE[t].set_color(get_color_from_state(STATE[t]))
            
        effective_reprod_cells = [p for p in potential_reprod_cells if STATE[p] == "R"]
        for e in effective_reprod_cells:
            STATE[e] = "T"
            self.wait(DEFAULT_WAIT_TIME / 4)
            self.remove(TXT_STATE[e])
            TXT_STATE[e] = Text(STATE[e]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * e / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * e / WORLD_SIZE) * UP)
            TXT_STATE[e].set_color(get_color_from_state(STATE[e]))

        if len(effective_reprod_cells) > 0:
            self.play(*[Write(TXT_STATE[e]) for e in effective_reprod_cells])

class BirthRabbit(Scene):
    def construct(self):
        global STATE, SCORE, SCORE_TEXT, ACTION_TEXT
        self.remove(ACTION_TEXT)
        ACTION_TEXT = Text("BirthRabbit", color = GRAY_B).scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)
        self.play(Write(ACTION_TEXT))
        
        empty_cells = [i for i, s in enumerate(STATE) if s == " "]
        if len(empty_cells) == 0:
            return
        SCORE -= COST_BR
        self.remove(SCORE_TEXT)
        SCORE_TEXT = Text(f"{SCORE}").scale(0.5).next_to(SCORE_TEXT_BASE, RIGHT)
        self.play(Write(SCORE_TEXT))

        i = rd.choice(empty_cells)
        self.remove(TXT_STATE[i])
        STATE[i] = "R"
        TXT_STATE[i] = Text(STATE[i]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * i / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * i / WORLD_SIZE) * UP)
        TXT_STATE[i].set_color(get_color_from_state(STATE[i]))
        self.play(Write(TXT_STATE[i]))

class BirthTiger(Scene):
    def construct(self):
        global STATE, SCORE, SCORE_TEXT, ACTION_TEXT
        self.remove(ACTION_TEXT)
        ACTION_TEXT = Text("BirthTiger", color = ORANGE).scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)
        self.play(Write(ACTION_TEXT))
        
        empty_cells = [i for i, s in enumerate(STATE) if s == " "]
        if len(empty_cells) == 0:
            return
        SCORE -= COST_BT
        self.remove(SCORE_TEXT)
        SCORE_TEXT = Text(f"{SCORE}").scale(0.5).next_to(SCORE_TEXT_BASE, RIGHT)
        self.play(Write(SCORE_TEXT))

        i = rd.choice(empty_cells)
        self.remove(TXT_STATE[i])
        STATE[i] = "T"
        TXT_STATE[i] = Text(STATE[i]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * i / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * i / WORLD_SIZE) * UP)
        TXT_STATE[i].set_color(get_color_from_state(STATE[i]))
        self.play(Write(TXT_STATE[i]))

class ActivateDinosaur(Scene):
    def construct(self):
        global STATE, SCORE, SCORE_TEXT, ACTION_TEXT
        self.remove(ACTION_TEXT)
        ACTION_TEXT = Text("ActivateDinosaur", color = GREEN_E).scale(0.35).next_to(ACTION_TEXT_BASE, RIGHT)
        self.play(Write(ACTION_TEXT))

        indexes = list(range(WORLD_SIZE))
        rd.shuffle(indexes)
        dino_indexes = indexes[:DINO_REACH]
        dino_claws = [Circle(SMALLR_RAD, color = RED).move_to(BIGGER_RAD * cos(TAU * di / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * di / WORLD_SIZE) * UP) for di in dino_indexes]
        self.play(*[Create(claw) for claw in dino_claws])
        self.remove(*[TXT_STATE[i] for i in dino_indexes])

        if "T" in [STATE[i] for i in dino_indexes]:
            SCORE += BONUS_EGG
        else:
            SCORE -= MALUS_EGG
        
        for i in dino_indexes:
            STATE[i] = " "
            TXT_STATE[i] = Text(STATE[i]).scale(0.4).move_to(BIGGER_RAD * cos(TAU * i / WORLD_SIZE) * RIGHT + BIGGER_RAD * sin(TAU * i / WORLD_SIZE) * UP)
            TXT_STATE[i].set_color(get_color_from_state(STATE[i]))

        self.remove(SCORE_TEXT)
        SCORE_TEXT = Text(f"{SCORE}").scale(0.5).next_to(SCORE_TEXT_BASE, RIGHT)
        self.play(Write(SCORE_TEXT))
        
        self.play(*[Write(TXT_STATE[i]) for i in dino_indexes])
        self.remove(*dino_claws)
        self.wait()

class MainDinosaur(Scene):
    def construct(self):
        global NB_MOVES, NB_MOVES_TEXT
        BuildBackground.construct(self)
        self.play(*[Write(t) for t in TXT_STATE])
        incoming_action = True
        while incoming_action:
            show_state()
            NB_MOVES += 1
            
            self.remove(NB_MOVES_TEXT)
            NB_MOVES_TEXT = Text(str(NB_MOVES)).scale(0.35).next_to(NB_MOVES_TEXT_BASE, RIGHT)
            self.play(Write(NB_MOVES_TEXT))

            next_action = input("Next Action [AR|AT|BR|BT|AD|.] : ")
            if next_action == "AR":
                ActivateRabbits.construct(self)
            elif next_action == "AT":
                ActivateTigers.construct(self)
            elif next_action == "BR":
                BirthRabbit.construct(self)
            elif next_action == "BT":
                BirthTiger.construct(self)
            elif next_action == "AD":
                ActivateDinosaur.construct(self)
            else:
                incoming_action = False
        show_state()