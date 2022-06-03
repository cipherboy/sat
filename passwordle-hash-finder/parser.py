#!/usr/bin/python3

import json
from html.parser import HTMLParser
import sys

class PasswordleParser(HTMLParser):
    STATE_LOOKING = 0
    STATE_IN_GUESS = 1
    STATE_IN_TILE = 2

    def __init__(self):
        self.guesses = []
        self.stack = []
        self.state = PasswordleParser.STATE_LOOKING
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.stack.append((tag, attrs))

        for attr in attrs:
            name, value = attr
            if name == 'id' and 'attempt-' in value:
                self.guesses.append([])
                self.state = PasswordleParser.STATE_IN_GUESS
            elif name == 'class' and 'tile' in value:
                self.state = PasswordleParser.STATE_IN_TILE
            else:
                self.state = PasswordleParser.STATE_LOOKING

    def handle_endtag(self, tag):
        if self.stack[-1][0] != tag:
            assert False, f"expected last seen tag to be {self.stack[-1][0]} but was {tag}"
        self.stack.pop()

        if self.state == PasswordleParser.STATE_IN_GUESS:
            self.state = PasswordleParser.STATE_LOOKING
        elif self.state == PasswordleParser.STATE_IN_TILE:
            self.state = PasswordleParser.STATE_IN_GUESS

    def handle_data(self, data):
        if self.state != PasswordleParser.STATE_IN_TILE:
            return

        last_tag_class = list(filter(lambda x: x[0] == 'class', self.stack[-1][1]))
        assert len(last_tag_class) == 1, f"expected only one tag attribute with class name; got {len(last_tag_class)} for tag {self.stack[-1]}"
        last_tag_class = last_tag_class[0][1]
        last_tag_classes = list(filter(lambda x: x.startswith('tile-'), last_tag_class.split(' ')))
        assert len(last_tag_classes) == 1, f"expected only one class with prefix `tag-`; got {len(last_tag_classes)} for tag {self.stack[-1]}"
        last_tag_classes = last_tag_classes[0][len('tile-'):]

        if last_tag_classes != 'correct' and last_tag_classes != 'present' and last_tag_classes != 'absent' and last_tag_classes != 'empty':
            assert False, f"unexpected tag type: {last_tag_classes} on tag {self.stack[-1]}"

        if last_tag_classes == 'empty':
            return

        self.guesses[-1].append([data.strip(), last_tag_classes])

def main():
    if len(sys.argv) != 2:
        print("Usage: html.py /path/to/guesses.html")
        sys.exit(1)

    document = sys.argv[1]
    contents = open(document, 'r').read()

    parser = PasswordleParser()
    parser.feed(contents)

    parser.guesses.pop()
    print(json.dumps(parser.guesses))

if __name__ == "__main__":
    main()
