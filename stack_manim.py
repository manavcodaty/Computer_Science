
from manim import *
import random

"""
A‑Level CIE (Cambridge) Computer Science — Stacks (LIFO)
Manim Community v0.18+

Covers exactly what the spec expects students to know about stacks:
• ADT definition and LIFO property
• Static (array) stack with top index; dynamic (linked) stack overview
• Core operations: push, pop, peek/top, isEmpty, isFull
• Overflow / Underflow, with visual demo
• Typical applications: undo/redo, browser back, parsing/brackets, postfix (RPN) evaluation
• Time complexity notes (O(1) for push/pop/peek)
• CIE‑style pseudocode for push/pop (static + dynamic version)
• Extra: bracket‑matching walk‑through; call‑stack/recursion concept demo

SCENES (render any you need):
1) StackExplainer            — main visual demo (array stack + ops + overflow/underflow + postfix eval)
2) StackPseudocodeScene      — CIE‑style pseudocode cards for static & dynamic stacks
3) BracketMatchingScene      — balanced parentheses using a stack (spec‑friendly application)
4) CallStackScene            — shows the *runtime* call stack via factorial recursion

Usage examples:
    manim -pqh stack_explainer.py StackExplainer
    manim -pqh stack_explainer.py StackPseudocodeScene
    manim -pqh stack_explainer.py BracketMatchingScene
    manim -pqh stack_explainer.py CallStackScene
"""

# ---------------------------
# 1) Core visual explainer
# ---------------------------
class StackExplainer(Scene):
    def construct(self):
        title = Text("Stacks (LIFO) — A‑Level CIE CS").scale(0.8).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))
        self.wait(0.4)

        # Definition box
        defn = VGroup(
            Text("Abstract Data Type: Stack").scale(0.6),
            Text("LIFO — Last In, First Out").scale(0.58),
            Text("Ops: push, pop, peek/top, isEmpty, isFull").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(LEFT).shift(DOWN*0.3)
        brace_defn = Brace(defn, direction=RIGHT)
        note = Text("CIE expects ADTs + ops", font_size=28)
        note.next_to(brace_defn, RIGHT, buff=0.2)
        self.play(
            LaggedStart(
                FadeIn(defn[0], shift=RIGHT),
                FadeIn(defn[1], shift=RIGHT),
                FadeIn(defn[2], shift=RIGHT),
                lag_ratio=0.15,
            )
        )
        self.play(GrowFromCenter(brace_defn), FadeIn(note, shift=UP))

        # Array‑based stack visual (fixed capacity)
        max_size = 5
        cell_w, cell_h = 1.1, 0.9
        base = Rectangle(width=cell_w, height=cell_h).set_stroke(WHITE)
        cells = VGroup(*[base.copy() for _ in range(max_size)]).arrange(UP, buff=0)
        cells.to_edge(RIGHT).shift(LEFT*1.5)

        idx_labels = VGroup(*[Text(str(i), font_size=26, color=GRAY) for i in range(max_size)])
        for lab, cell in zip(idx_labels, cells):
            lab.next_to(cell, LEFT, buff=0.2)

        arr_title = Text("Static stack: array + top index").scale(0.55).next_to(cells, UP, buff=0.35)
        self.play(FadeIn(arr_title, shift=UP), Create(cells), FadeIn(idx_labels, shift=LEFT))

        # top pointer (starts at -1 → empty)
        top_idx = -1
        top_arrow = Arrow(start=LEFT, end=RIGHT, buff=0.15, max_tip_length_to_length_ratio=0.1).scale(0.6)
        top_label = Text("top = -1", font_size=28)
        top_group = VGroup(top_label, top_arrow).arrange(RIGHT, buff=0.25)
        top_group.next_to(cells, DOWN, buff=0.4)
        self.play(FadeIn(top_group))

        # value labels per cell
        vals = [None for _ in range(max_size)]
        val_mobjs = [None for _ in range(max_size)]

        def highlight_cell(i, color=YELLOW):
            return [cells[i].animate.set_stroke(color, width=4)]
        def unhighlight_all():
            return [c.animate.set_stroke(WHITE, width=1) for c in cells]
        def move_top_pointer(i):
            nonlocal top_idx, top_group
            top_idx = i
            txt = Text(f"top = {top_idx}", font_size=28)
            new_group = VGroup(txt, top_arrow.copy()).arrange(RIGHT, buff=0.25)
            new_group.next_to(cells, DOWN, buff=0.4)
            self.play(ReplacementTransform(top_group, new_group))
            top_group = new_group

        # Ops panel
        ops_panel = VGroup(
            RoundedRectangle(corner_radius=0.1, width=5.4, height=1.5).set_stroke(BLUE),
            Text("push(x)  pop()  peek()  isEmpty()  isFull()", font_size=26)
        )
        ops_panel[1].move_to(ops_panel[0].get_center())
        ops_panel.to_edge(DOWN)
        self.play(FadeIn(ops_panel[0]), FadeIn(ops_panel[1]))

        # Helper animations
        def push_value(x):
            # isFull?
            if top_idx == max_size - 1:
                warn = Text("Overflow! (isFull) — cannot push", font_size=28, color=RED).next_to(arr_title, DOWN)
                self.play(Flash(arr_title), FadeIn(warn))
                self.wait(0.5)
                self.play(FadeOut(warn))
                return
            new_top = top_idx + 1
            self.play(*highlight_cell(new_top))
            move_top_pointer(new_top)
            val = Text(str(x), font_size=30).move_to(cells[new_top].get_center())
            vals[new_top] = x
            val_mobjs[new_top] = val
            self.play(Write(val))
            self.play(*unhighlight_all())

        def pop_value():
            # isEmpty?
            if top_idx == -1:
                warn = Text("Underflow! (isEmpty) — cannot pop", font_size=28, color=RED).next_to(arr_title, DOWN)
                self.play(Flash(arr_title), FadeIn(warn))
                self.wait(0.5)
                self.play(FadeOut(warn))
                return None
            i = top_idx
            self.play(*highlight_cell(i))
            popped = vals[i]
            if val_mobjs[i]:
                self.play(FadeOut(val_mobjs[i], shift=UP*0.3))
            vals[i] = None
            val_mobjs[i] = None
            move_top_pointer(i - 1)
            self.play(*unhighlight_all())
            return popped

        def peek_value():
            if top_idx == -1:
                warn = Text("Empty stack — peek undefined", font_size=28, color=YELLOW).next_to(arr_title, DOWN)
                self.play(FadeIn(warn))
                self.wait(0.5)
                self.play(FadeOut(warn))
                return None
            self.play(*highlight_cell(top_idx))
            tip = Text(f"peek → {vals[top_idx]}", font_size=28).next_to(arr_title, DOWN)
            self.play(Write(tip))
            self.wait(0.35)
            self.play(FadeOut(tip), *unhighlight_all())
            return vals[top_idx]

        lifo_tag = Text("LIFO: last in, first out", font_size=28, color=GREEN).next_to(arr_title, DOWN)
        self.play(FadeIn(lifo_tag, shift=DOWN))
        self.wait(0.4)
        self.play(FadeOut(lifo_tag))

        # Push a few values
        for v in [3, 7, 9]:
            step = Text(f"push({v})", font_size=28).next_to(ops_panel, UP, buff=0.2)
            self.play(FadeIn(step, shift=UP))
            push_value(v)
            self.play(FadeOut(step, shift=DOWN))

        # Peek
        step = Text("peek()", font_size=28).next_to(ops_panel, UP, buff=0.2)
        self.play(FadeIn(step, shift=UP))
        peek_value()
        self.play(FadeOut(step, shift=DOWN))

        # Pop twice (show LIFO)
        for _ in range(2):
            step = Text("pop()", font_size=28).next_to(ops_panel, UP, buff=0.2)
            self.play(FadeIn(step, shift=UP))
            popped = pop_value()
            if popped is not None:
                msg = Text(f"returned {popped}", font_size=26, color=GREEN).next_to(arr_title, DOWN)
                self.play(FadeIn(msg))
                self.wait(0.2)
                self.play(FadeOut(msg))
            self.play(FadeOut(step, shift=DOWN))

        # Overflow & underflow
        overflow_title = Text("Overflow & Underflow", font_size=28).next_to(arr_title, DOWN)
        self.play(FadeIn(overflow_title, shift=DOWN))
        while top_idx < max_size - 1:
            push_value(random.randint(1, 99))
        push_value(42)  # overflow
        while top_idx >= 0:
            pop_value()
        pop_value()      # underflow
        self.play(FadeOut(overflow_title))

        # Complexity + applications
        comp = VGroup(
            Text("Time Complexity:" , font_size=28),
            Text("push O(1) • pop O(1) • peek O(1) • isEmpty/isFull O(1)", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_edge(LEFT).shift(DOWN*2.2)
        self.play(FadeIn(comp, shift=RIGHT))

        apps = VGroup(
            Text("Applications:", font_size=28),
            Text("Undo/Redo  •  Browser back  •  Bracket parsing  •  Postfix eval", font_size=26)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(comp, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(apps, shift=RIGHT))

        # Mini postfix evaluation trace: tokens "3 4 + 2 *" → 14
        trace_title = Text("Postfix (RPN) evaluation", font_size=28).next_to(arr_title, DOWN)
        self.play(FadeIn(trace_title, shift=DOWN))
        demo_tokens = ["3", "4", "+", "2", "*"]
        token_row = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.7, height=0.6).set_stroke(ORANGE) for _ in demo_tokens])
        token_row.arrange(RIGHT, buff=0.15).next_to(trace_title, DOWN)
        token_texts = VGroup(*[Text(t, font_size=28) for t in demo_tokens])
        for tt, rr in zip(token_texts, token_row):
            tt.move_to(rr.get_center())
        self.play(Create(token_row), FadeIn(token_texts))

        # Small eval stack (left side)
        aux_cells = VGroup(*[base.copy() for _ in range(4)]).arrange(UP, buff=0).next_to(token_row, LEFT, buff=1.6)
        aux_title = Text("Eval Stack", font_size=26).next_to(aux_cells, UP, buff=0.2)
        self.play(FadeIn(aux_title), Create(aux_cells))
        aux_vals = [None]*4
        aux_m = [None]*4
        aux_top = -1

        def aux_push(v):
            nonlocal aux_top
            aux_top += 1
            if aux_top >= 4:
                aux_top = 3
                return
            m = Text(str(v), font_size=28).move_to(aux_cells[aux_top])
            aux_vals[aux_top] = v
            aux_m[aux_top] = m
            self.play(Write(m))
        def aux_pop():
            nonlocal aux_top
            if aux_top == -1:
                return None
            m = aux_m[aux_top]
            val = aux_vals[aux_top]
            if m:
                self.play(FadeOut(m, shift=UP*0.2))
            aux_m[aux_top] = None
            aux_vals[aux_top] = None
            aux_top -= 1
            return val

        explain = Text("Scan L→R. Push numbers. On operator: pop 2, apply, push result.", font_size=24, color=GRAY)
        explain.next_to(token_row, DOWN, buff=0.25)
        self.play(FadeIn(explain))

        for i, t in enumerate(demo_tokens):
            hl = SurroundingRectangle(token_row[i], color=YELLOW)
            self.play(Create(hl))
            if t.isdigit():
                aux_push(int(t))
            else:
                b = aux_pop(); a = aux_pop()
                if t == "+": res = a + b
                elif t == "-": res = a - b
                elif t == "*": res = a * b
                elif t == "/": res = a / b
                else: res = 0
                show = Text(f"{a} {t} {b} = {res}", font_size=26, color=GREEN).next_to(explain, DOWN, buff=0.15)
                self.play(FadeIn(show))
                aux_push(res)
                self.wait(0.2)
                self.play(FadeOut(show))
            self.play(FadeOut(hl))

        result = aux_vals[aux_top]
        res_note = Text(f"Result = {result}", font_size=28, color=GREEN).next_to(explain, DOWN, buff=0.45)
        self.play(Write(res_note))
        self.wait(0.8)

        # Outro notes
        close_box = VGroup(
            Text("Implementation notes:", font_size=28),
            Text("Static: array + top; need isFull (overflow)", font_size=26),
            Text("Dynamic: linked nodes + top ref; no fixed capacity", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_edge(RIGHT).shift(DOWN*1.1)
        self.play(FadeIn(close_box, shift=LEFT))
        outro = Text("Key idea: LIFO with O(1) push/pop/peek", font_size=30, color=YELLOW).to_edge(DOWN)
        self.play(Write(outro))
        self.wait(1.0)


# -------------------------------------
# 2) Pseudocode cards (CIE‑style ops)
# -------------------------------------
class StackPseudocodeScene(Scene):
    def construct(self):
        title = Text("CIE‑Style Pseudocode: Stack Ops").scale(0.8).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        # Static (array) version
        static_title = Text("Static stack (array) — top, maxSize").scale(0.55)
        static_code = """
PROCEDURE push(x)
    IF top = maxSize - 1 THEN
        OUTPUT "Overflow"
    ELSE
        top ← top + 1
        stack[top] ← x
    ENDIF
ENDPROCEDURE

FUNCTION pop() RETURNS INTEGER
    IF top = -1 THEN
        OUTPUT "Underflow"
        RETURN -1   // or ERROR
    ELSE
        item ← stack[top]
        top ← top - 1
        RETURN item
    ENDIF
ENDFUNCTION

FUNCTION peek() RETURNS INTEGER
    IF top = -1 THEN
        RETURN -1  // or ERROR
    ELSE
        RETURN stack[top]
    ENDIF
ENDFUNCTION

FUNCTION isEmpty() RETURNS BOOLEAN
    RETURN top = -1
ENDFUNCTION

FUNCTION isFull() RETURNS BOOLEAN
    RETURN top = maxSize - 1
ENDFUNCTION
"""
        static_box = RoundedRectangle(corner_radius=0.12, width=7.6, height=5.4).set_stroke(BLUE)
        static_group = VGroup(
            static_title,
            Text(static_code, font_size=24).
                scale_to_fit_width(7.2)
        ).arrange(DOWN, buff=0.2)
        static_group.move_to(static_box.get_center())
        left = VGroup(static_box, static_group).to_edge(LEFT).shift(RIGHT*0.1)

        # Dynamic (linked) version
        dynamic_title = Text("Dynamic stack (linked nodes) — top points to Node").scale(0.55)
        dynamic_code = """
TYPE Node
    data : INTEGER
    next : Node
ENDTYPE

top : Node ← NULL

PROCEDURE push(x)
    newNode : Node
    newNode.data ← x
    newNode.next ← top
    top ← newNode
ENDPROCEDURE

FUNCTION pop() RETURNS INTEGER
    IF top = NULL THEN
        OUTPUT "Underflow"
        RETURN -1  // or ERROR
    ELSE
        item ← top.data
        top ← top.next
        RETURN item
    ENDIF
ENDFUNCTION

FUNCTION peek() RETURNS INTEGER
    IF top = NULL THEN RETURN -1 ELSE RETURN top.data ENDIF
ENDFUNCTION

FUNCTION isEmpty() RETURNS BOOLEAN
    RETURN top = NULL
ENDFUNCTION
"""
        dynamic_box = RoundedRectangle(corner_radius=0.12, width=7.6, height=5.4).set_stroke(GREEN)
        dynamic_group = VGroup(
            dynamic_title,
            Text(dynamic_code, font_size=24).
                scale_to_fit_width(7.2)
        ).arrange(DOWN, buff=0.2)
        dynamic_group.move_to(dynamic_box.get_center())
        right = VGroup(dynamic_box, dynamic_group).to_edge(RIGHT).shift(LEFT*0.1)

        hint = Text("These match the style used in the CIE syllabus & past papers.", font_size=26, color=GRAY).next_to(title, DOWN)
        self.play(Create(left), Create(right), FadeIn(hint))
        self.wait(2)


# -------------------------------------
# 3) Bracket matching (balanced?)
# -------------------------------------
class BracketMatchingScene(Scene):
    def construct(self):
        title = Text("Bracket Matching with a Stack").scale(0.8).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        expr = "A * (B + C) - { D / [ E - F ] }"
        expr_text = Text(expr, font_size=32)
        expr_box = RoundedRectangle(corner_radius=0.1, width=10.5, height=1.1).set_stroke(ORANGE)
        expr_group = VGroup(expr_box, expr_text)
        expr_text.move_to(expr_box.get_center())
        expr_group.to_edge(UP).shift(DOWN*1.6)
        self.play(Create(expr_box), FadeIn(expr_text))

        # Stack on the side
        cell = Rectangle(width=1.0, height=0.8).set_stroke(WHITE)
        stack_cells = VGroup(*[cell.copy() for _ in range(6)]).arrange(UP, buff=0)
        stack_label = Text("Stack", font_size=26).next_to(stack_cells, UP, buff=0.2)
        stack_group = VGroup(stack_label, stack_cells).to_edge(LEFT).shift(RIGHT*1.0, DOWN*0.2)
        self.play(FadeIn(stack_label), Create(stack_cells))

        vals = [None]*6
        mobs = [None]*6
        top = -1

        def s_push(ch):
            nonlocal top
            if top < 5:
                top += 1
                txt = Text(ch, font_size=28)
                txt.move_to(stack_cells[top])
                mobs[top] = txt
                vals[top] = ch
                self.play(Write(txt))
        def s_pop():
            nonlocal top
            if top == -1: return None
            ch = vals[top]
            if mobs[top]:
                self.play(FadeOut(mobs[top], shift=UP*0.2))
            vals[top] = None
            mobs[top] = None
            top -= 1
            return ch

        legend = Text("Openers push. On closer: check top matches, then pop.", font_size=24, color=GRAY)
        legend.next_to(expr_group, DOWN)
        self.play(FadeIn(legend))

        # Walk through characters: only animate brackets
        pairs = {')':'(', ']':'[', '}':'{'}
        openers = set(pairs.values())
        closers = set(pairs.keys())
        x = expr

        # Create a row of little boxes highlighting bracket positions
        boxes = []
        for i, ch in enumerate(x):
            if ch in openers | closers:
                b = SurroundingRectangle(Text(ch, font_size=32), color=YELLOW)
                # Fake position: place over the same layout as expr_text by using measure
                # Simpler approach: show a small floating label for each step
                step = Text(ch, font_size=28).next_to(legend, DOWN)
                self.play(FadeIn(step))
                if ch in openers:
                    s_push(ch)
                else:
                    topch = s_pop()
                    verdict = "OK" if topch == pairs[ch] else "Mismatch!"
                    v = Text(verdict, font_size=26, color=GREEN if verdict=="OK" else RED).next_to(step, RIGHT)
                    self.play(FadeIn(v))
                    self.wait(0.2)
                    self.play(FadeOut(v))
                self.play(FadeOut(step))

        final = Text("Balanced if stack empty at end", font_size=28, color=GREEN if top==-1 else RED).next_to(legend, DOWN)
        self.play(Write(final))
        self.wait(1)


# -------------------------------------
# 4) Call‑stack (runtime) demo
# -------------------------------------
class CallStackScene(Scene):
    def construct(self):
        title = Text("The *Runtime* Stack (Call Stack)").scale(0.8).to_edge(UP)
        self.play(FadeIn(title, shift=DOWN))

        # Show factorial recursion to illustrate frames pushing/popping
        code = """
FUNCTION fact(n) RETURNS INTEGER
    IF n = 0 THEN RETURN 1
    ELSE RETURN n * fact(n-1)
ENDFUNCTION
"""
        code_box = RoundedRectangle(corner_radius=0.12, width=6.5, height=2.2).set_stroke(BLUE)
        code_text = Text(code, font_size=26).scale_to_fit_width(6.1).move_to(code_box.get_center())
        left = VGroup(code_box, code_text).to_edge(LEFT).shift(RIGHT*0.4, DOWN*0.2)
        self.play(Create(code_box), FadeIn(code_text))

        # Call stack frames on the right
        cell = Rectangle(width=2.2, height=0.9).set_stroke(WHITE)
        frames = VGroup(*[cell.copy() for _ in range(6)]).arrange(UP, buff=0)
        label = Text("Call Stack", font_size=26).next_to(frames, UP, buff=0.2)
        right = VGroup(label, frames).to_edge(RIGHT).shift(LEFT*0.8, DOWN*0.2)
        self.play(FadeIn(label), Create(frames))

        vals = [None]*6
        mobs = [None]*6
        top = -1
        def push_frame(txt):
            nonlocal top
            top += 1
            t = Text(txt, font_size=26).move_to(frames[top])
            mobs[top] = t
            self.play(Write(t))
        def pop_frame():
            nonlocal top
            if top == -1: return
            self.play(FadeOut(mobs[top], shift=UP*0.2))
            mobs[top] = None
            top -= 1

        trace = Text("Evaluate fact(4)", font_size=28).next_to(left, DOWN, buff=0.3)
        self.play(FadeIn(trace))

        # Push calls
        for n in [4,3,2,1,0]:
            push_frame(f"fact({n}) call")
            self.wait(0.1)
        # Base case return
        ret = 1
        self.play(FadeIn(Text("return 1", font_size=26, color=GREEN).next_to(trace, DOWN)))
        pop_frame()  # fact(0)

        # Unwind with returns: 1*1, 2*1, 3*2, 4*6
        steps = [(1,1),(2,1),(3,2),(4,6)]
        acc = ret
        for n, mul in steps:
            show = Text(f"return {n} * {acc} = {n*acc}", font_size=26, color=GREEN).next_to(trace, DOWN)
            self.play(FadeIn(show))
            acc = n*acc
            pop_frame()
            self.play(FadeOut(show))

        final = Text(f"fact(4) = {acc}", font_size=30, color=YELLOW).to_edge(DOWN)
        self.play(Write(final))
        self.wait(1.0)


# End of file — no build helper kept here to avoid syntax issues.
