
# Manim Community Edition 0.18+
# Professional concept-first animation for Singly Linked Lists
# Save as linked_list_concept.py and run:
#   manim -pqh linked_list_concept.py LinkedListConcept
# or higher quality:
#   manim -p -qh linked_list_concept.py LinkedListConcept

from manim import *
import numpy as np

ACCENT = BLUE_E
MUTED = GREY_B
HILITE = YELLOW
BG_ARROW = GREY_D
TXT_SCALE = 0.48
CAP_SCALE = 0.44
NODE_W, NODE_H = 1.4, 0.8
PTR_W = 0.35  # width of the right "next" compartment

class NodeVisual(VGroup):
    """A node with two compartments: data | next"""
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        # two-rect layout: data box + next box
        data_box = Rectangle(width=NODE_W - PTR_W, height=NODE_H).set_stroke(WHITE,2)
        next_box = Rectangle(width=PTR_W, height=NODE_H).set_stroke(WHITE,2)
        next_box.next_to(data_box, RIGHT, buff=0)
        self.box = VGroup(data_box, next_box)

        self.value = value
        self.val_text = Text(str(value)).scale(0.5).move_to(data_box.get_center())
        self.next_port = next_box.get_center()

        self.add(self.box, self.val_text)

    def data_center(self):
        return self.box[0].get_center()

    def next_center(self):
        return self.box[1].get_center()

class SinglyLinkedList(VGroup):
    def __init__(self, values=None, gap=1.2, **kwargs):
        super().__init__(**kwargs)
        self.gap = gap
        self.nodes: list[NodeVisual] = []
        self.arrows: list[Arrow] = []
        if values:
            for v in values:
                self.nodes.append(NodeVisual(v))
        self.layout()

    def layout(self):
        # remove prior arrows
        for a in self.arrows:
            if a in self.submobjects:
                self.remove(a)
        self.arrows = []
        if self.nodes:
            VGroup(*self.nodes).arrange(RIGHT, buff=self.gap)
        # arrows from next-center to next node's left edge
        for i in range(len(self.nodes)-1):
            start = self.nodes[i].next_center()
            end = self.nodes[i+1].box[0].get_left()
            arr = Arrow(start, end, buff=0.08, max_tip_length_to_length_ratio=0.25, stroke_width=4, color=BG_ARROW)
            self.arrows.append(arr)
        for a in self.arrows:
            self.add(a)
        for n in self.nodes:
            self.add(n)

    # --- Animation helpers ---
    def build_arrows_anim(self):
        return AnimationGroup(*[Create(a) for a in self.arrows], lag_ratio=0.12)

    def move_to_arranged(self):
        arranged = VGroup(*self.nodes).copy().arrange(RIGHT, buff=self.gap)
        return [self.nodes[i].animate.move_to(arranged[i].get_center()) for i in range(len(self.nodes))]

    def insert_head(self, scene: Scene, value, rt=1.0):
        new = NodeVisual(value)
        self.add(new)
        if self.nodes:
            new.move_to(self.nodes[0].get_center() + DOWN*1.4)
        else:
            new.move_to(ORIGIN)
        scene.play(FadeIn(new, shift=UP), run_time=rt*0.5)
        self.nodes.insert(0, new)
        self.layout()
        scene.play(*self.move_to_arranged(), run_time=rt)
        scene.play(self.build_arrows_anim(), run_time=rt*0.8)

    def insert_after_index(self, scene: Scene, index:int, value, rt=1.0):
        if len(self.nodes)==0:
            return self.insert_head(scene, value, rt)
        index = max(0, min(index, len(self.nodes)-1))
        new = NodeVisual(value)
        self.add(new)
        anchor = self.nodes[index]
        new.move_to(anchor.get_center() + DOWN*1.4)
        scene.play(FadeIn(new, shift=UP), run_time=rt*0.5)
        self.nodes.insert(index+1, new)
        self.layout()
        scene.play(*self.move_to_arranged(), run_time=rt)
        scene.play(self.build_arrows_anim(), run_time=rt*0.8)

    def append(self, scene: Scene, value, rt=1.0):
        self.insert_after_index(scene, len(self.nodes)-1 if self.nodes else 0, value, rt)

    def delete_head(self, scene: Scene, rt=1.0):
        if not self.nodes:
            return
        target = self.nodes[0]
        glow = SurroundingRectangle(target, color=HILITE, buff=0.06)
        scene.play(Create(glow), run_time=rt*0.4)
        scene.play(FadeOut(glow), run_time=rt*0.3)
        scene.play(target.animate.shift(DOWN*1.4).fade(1.0), run_time=rt)
        self.remove(target)
        self.nodes.pop(0)
        self.layout()
        scene.play(*self.move_to_arranged(), run_time=rt*0.9)
        scene.play(self.build_arrows_anim(), run_time=rt*0.7)

    def delete_after_index(self, scene: Scene, index:int, rt=1.0):
        if len(self.nodes) <= 1:
            return self.delete_head(scene, rt)
        index = max(0, min(index, len(self.nodes)-2))
        target = self.nodes[index+1]
        glow = SurroundingRectangle(target, color=HILITE, buff=0.06)
        scene.play(Create(glow), run_time=rt*0.4)
        scene.play(FadeOut(glow), run_time=rt*0.3)
        scene.play(target.animate.shift(DOWN*1.4).fade(1.0), run_time=rt)
        self.remove(target)
        self.nodes.pop(index+1)
        self.layout()
        scene.play(*self.move_to_arranged(), run_time=rt*0.9)
        scene.play(self.build_arrows_anim(), run_time=rt*0.7)

class Caption(VGroup):
    def __init__(self, text:str):
        super().__init__()
        self.txt = Text(text).scale(CAP_SCALE)
        self.add(self.txt)
        self.to_edge(DOWN)

class LinkedListConcept(Scene):
    def show_caption(self, text, rt=0.6):
        cap = Caption(text)
        self.play(FadeIn(cap, shift=UP), run_time=rt)
        return cap

    def section_title(self, title):
        t = Text(title, weight=BOLD).scale(0.7).to_edge(UP)
        box = Underline(t, color=ACCENT)
        self.play(Write(t), Create(box))
        return VGroup(t, box)

    def construct(self):
        # Title
        title = Text("Linked Lists: Structure, Traversal, Insert, Delete", weight=BOLD).scale(0.6).to_edge(UP)
        subtitle = Text("Singly Linked List (Concept)").scale(0.42).next_to(title, DOWN, buff=0.18).set_color(MUTED)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))

        # 1) Anatomy of a Node
        cap = self.show_caption("A node stores data and a pointer to the next node.")
        node = NodeVisual(7)
        node.move_to(ORIGIN)
        self.play(FadeIn(node, shift=UP))
        # labels
        data_label = Text("data").scale(TXT_SCALE).next_to(node.box[0], UP, buff=0.12)
        next_label = Text("next").scale(TXT_SCALE).next_to(node.box[1], UP, buff=0.12)
        self.play(FadeIn(data_label), FadeIn(next_label))
        # faint outgoing pointer
        ghost = Arrow(node.next_center(), node.next_center()+RIGHT*1.0, buff=0.05, stroke_opacity=0.4, color=BG_ARROW)
        self.play(Create(ghost))
        self.play(FadeOut(cap))

        # 2) Whole structure
        cap = self.show_caption("Nodes link in sequence; the last points to None.")
        ll = SinglyLinkedList([3,7,12,18])
        ll.move_to(DOWN*0.6)
        self.play(ReplacementTransform(node, ll.nodes[1]))  # morph single node into part of list
        # ensure layout + arrows visible
        ll.layout()
        self.play(ll.build_arrows_anim())
        head_tag = Text("head", slant=ITALIC).scale(0.42).set_color(ACCENT).next_to(ll.nodes[0], UP, buff=0.12)
        self.play(FadeIn(head_tag, shift=UP))
        none_text = Text("None", slant=ITALIC).scale(0.42).set_color(MUTED)
        none_text.next_to(ll.nodes[-1], RIGHT, buff=0.8)
        none_dash = DashedLine(ll.nodes[-1].box[1].get_right(), none_text.get_left()).set_stroke(BG_ARROW,3)
        self.play(Create(none_dash), FadeIn(none_text, shift=RIGHT))
        self.play(FadeOut(cap))

        # 3) Traversal
        cap = self.show_caption("Traversal follows next pointers: access is linear in position.")
        tracer = SurroundingRectangle(ll.nodes[0], color=HILITE, buff=0.06)
        self.play(Create(tracer))
        for i in range(1,len(ll.nodes)):
            self.play(tracer.animate.move_to(ll.nodes[i]), run_time=0.6)
        self.play(FadeOut(tracer))
        cost = Text("Traversal cost: O(n)").scale(0.42).set_color(MUTED).to_corner(UR).shift(LEFT*0.3+DOWN*0.3)
        self.play(FadeIn(cost))
        self.play(FadeOut(cap))

        # 4) Insert at head
        cap = self.show_caption("Insert at head: create, point to old head, move head. O(1)")
        ll.insert_head(self, 1, rt=0.8)
        self.play(FadeOut(head_tag))
        head_tag = Text("head", slant=ITALIC).scale(0.42).set_color(ACCENT).next_to(ll.nodes[0], UP, buff=0.12)
        self.play(FadeIn(head_tag))
        self.play(FadeOut(cap))

        # 5) Insert after a given node (middle)
        cap = self.show_caption("Insert in middle: link new → successor, then prev → new. O(1) given prev")
        # traverse to position 2 to simulate known prev
        tracer = SurroundingRectangle(ll.nodes[1], color=ACCENT, buff=0.06)
        self.play(Create(tracer))
        self.play(tracer.animate.move_to(ll.nodes[2]))
        self.play(FadeOut(tracer))
        ll.insert_after_index(self, 2, 5, rt=0.8)
        self.play(FadeOut(cap))

        # 6) Append at tail
        cap = self.show_caption("Append: reach tail then link. With tail pointer, O(1); otherwise O(n).")
        ll.append(self, 20, rt=0.8)
        # refresh None marker to new tail
        self.play(FadeOut(none_dash), FadeOut(none_text))
        none_text = Text("None", slant=ITALIC).scale(0.42).set_color(MUTED)
        none_text.next_to(ll.nodes[-1], RIGHT, buff=0.8)
        none_dash = DashedLine(ll.nodes[-1].box[1].get_right(), none_text.get_left()).set_stroke(BG_ARROW,3)
        self.play(Create(none_dash), FadeIn(none_text))
        self.play(FadeOut(cap))

        # 7) Delete head
        cap = self.show_caption("Delete head: move head to next. O(1)")
        ll.delete_head(self, rt=0.8)
        self.play(FadeOut(head_tag))
        head_tag = Text("head", slant=ITALIC).scale(0.42).set_color(ACCENT).next_to(ll.nodes[0], UP, buff=0.12)
        self.play(FadeIn(head_tag))
        self.play(FadeOut(cap))

        # 8) Delete in the middle (after prev)
        cap = self.show_caption("Delete in middle: bypass target (prev.next = target.next). O(1) given prev")
        # visually choose a prev in the middle
        tracer = SurroundingRectangle(ll.nodes[2], color=ACCENT, buff=0.06)
        self.play(Create(tracer))
        self.play(FadeOut(tracer))
        ll.delete_after_index(self, 2, rt=0.8)
        # refresh None marker in case tail changed
        self.play(FadeOut(none_dash), FadeOut(none_text))
        none_text = Text("None", slant=ITALIC).scale(0.42).set_color(MUTED)
        none_text.next_to(ll.nodes[-1], RIGHT, buff=0.8)
        none_dash = DashedLine(ll.nodes[-1].box[1].get_right(), none_text.get_left()).set_stroke(BG_ARROW,3)
        self.play(Create(none_dash), FadeIn(none_text))
        self.play(FadeOut(cap))

        # 9) Performance table (quick)
        panel = Rectangle(width=5.8, height=2.7, fill_opacity=0.08, stroke_opacity=0.4).set_color(MUTED)
        panel.to_corner(UL).shift(DOWN*0.3+RIGHT*0.3)
        hdr = Text("Operations & Costs").scale(0.46).set_color(ACCENT).next_to(panel.get_top(), DOWN, buff=0.18)
        rows = VGroup(
            Text("Access k-th element  –  O(n)").scale(0.42),
            Text("Insert/Delete at head –  O(1)").scale(0.42),
            Text("Insert/Delete after known prev – O(1)").scale(0.42),
            Text("Find prev by search – O(n)").scale(0.42),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(hdr, DOWN, aligned_edge=LEFT)
        box = VGroup(panel, hdr, rows)
        self.play(FadeIn(panel), FadeIn(hdr), FadeIn(rows, lag_ratio=0.1))

        # 10) Closing
        closing = Text("Linked lists: a chain of nodes; edits are pointer rewires.").scale(0.5).to_edge(DOWN)
        self.play(Write(closing))
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects])
        thanks = Text("End").scale(0.7)
        self.play(FadeIn(thanks))
        self.wait(0.8)
