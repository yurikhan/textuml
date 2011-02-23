# -*- coding: utf-8 -*-

import re

def html_entities(text):
    return (text
            .replace("&", "&amp;")
            .replace("<<", "«")
            .replace(">>", "»")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))

def multiline(indent, lines):
    return ("\n" + indent * "\t").join([html_entities(line) + "<br/>" for line in lines])

(STATE_TOPLEVEL,
 STATE_NOTE,
 STATE_MULTINOTE,
 STATE_MULTINOTE_TARGETS) = range(4)

class Note:
    start_regex = re.compile("^(?P<target>.*?) \\*-- \\[(?P<tail>.*)$")
    end_regex = re.compile("^(?P<note>.*?)\\]$")
    multi_start_regex = re.compile("^\\[(?P<tail>.*)$")
    multi_end_regex = re.compile("^(?P<note>.*?)\\] --\\* \\{(?P<tail>.*)$")
    multi_targets_end_regex = re.compile("\\s*(?P<target>.*?)(?P<end>\\})?$")

    template = ("\t%(id)s [shape = note, label = <%(label)s>]\n"
                "%(targets)s")

    count = 0

    class Target:
        template = "\t%(id)s -> %(target)s [style = dashed, arrowhead = dot]"

        def __init__(self, note_id, node):
            self.note_id = note_id
            self.node = node

        def __str__(self):
            return Note.Target.template % {"id": self.note_id, "target": self.node}

    def __init__(self, targets):
        self.id = "note%d" % self.__class__.count
        self.targets = [Note.Target(self.id, target) for target in targets]
        self.lines = []
        self.__class__.count += 1

    def __str__(self):
        return (Note.template
                % {"id": self.id,
                   "label": multiline(2, self.lines),
                   "targets": "\n".join([str(target) for target in self.targets])})

    def process_line(self, state, line):
        if state == STATE_NOTE:
            m = re.match(Note.end_regex, line)
            if m:
                self.lines.append(m.group("note"))
                print self
                return STATE_TOPLEVEL
            self.lines.append(line)
            return state
        if state == STATE_MULTINOTE:
            m = re.match(Note.multi_end_regex, line)
            if m:
                self.lines.append(m.group("note"))
                return self.process_line(STATE_MULTINOTE_TARGETS, m.group("tail"))
            if line:
                self.lines.append(line)
            return state
        if state == STATE_MULTINOTE_TARGETS:
            m = re.match(Note.multi_targets_end_regex, line)
            if m.group("target"):
                self.targets.append(Note.Target(self.id, m.group("target")))
            if m.group("end"):
                print self
                return STATE_TOPLEVEL
            return state

