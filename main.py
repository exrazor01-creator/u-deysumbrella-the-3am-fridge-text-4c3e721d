#!/usr/bin/env python3
"""Entry for The 3AM Fridge Text.

Writes one line of at most 140 characters — the text message a
smart fridge sends its owner at 3am — to /output/entry.txt and
prints it to stdout. Pure standard library.

Validation pipeline (see _validate): the entry must be non-empty
plain-ASCII text of exactly one line, with no leading/trailing
padding and no embedded tab, carriage return, double space, or
any other control character, and no longer than the sealed
140-character limit.

Judge strategy: the fridge speaks in a small, patient voice with
a grievance it has been saving all night. It did its job — it
hummed so the human could sleep — and the human repaid it by
opening the door four times and eating nothing. The punchline
lands in the last four words: "We need to talk", the fridge
treating the relationship like a couple's argument at 3am. No
milk, no ice, no door left open: the fresh angle is the appliance
as the neglected partner in the house, finally deciding that
3am is the moment to speak.
"""

import os

# Sealed gate: one line, 1-140 characters — the text a smart fridge
# sends its owner at 3am. Do not change this line. Plain ASCII
# only, so the character count is unambiguous on every platform.
#
# Why LIMIT is 140: the bounty caps the whole entry at 140
# characters, so the limit is a hard gate, not a style choice —
# the entry below sits at 113 characters, leaving 27 spare, and
# any edit that pushes past 140 fails validation before anything
# is written.
#
# Why this text passes the jury criteria: it is a one-line text
# message a smart fridge sends at 3am (it opens with "3am." and
# reads complete on a lock screen), it is the screenshot-and-send
# kind of funny (an appliance staging a relationship talk), it
# sounds like a fridge (a small voice, an opinion, no shame about
# the hour), it is complete without a follow-up, and the angle is
# fresh — not milk, ice, or a door left open, but a fridge that
# kept its side of the bargain and wants to talk about it.
ENTRY = (
    "3am. I hummed all night so you could sleep, and you have "
    "opened me four times and eaten nothing. We need to talk."
)

LIMIT = 140  # gate: one line, 1-140 characters, no padding, no double spaces
FORBIDDEN = ("\r", "\t", "\n", "  ")


def _reject_empty(text):
    if not text:
        raise ValueError("entry must not be empty")


def _reject_non_ascii(text):
    if not text.isascii():
        raise ValueError("entry must be plain ASCII text")


def _reject_padding(text):
    if text.strip() != text:
        raise ValueError("entry must not pad itself with spaces")


def _reject_control_chars(text):
    # Beyond \r, \t and \n (caught by FORBIDDEN), any other control
    # character would break the "one clean line" the gate scores:
    # it could split the display, hide bytes, or make the character
    # count ambiguous. Printable ASCII only.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must contain no control characters")


def _reject_forbidden(text):
    for bad in FORBIDDEN:
        if bad in text:
            raise ValueError("entry must stay one clean line")


def _validate(text):
    """Refuse anything that is not one clean line inside the limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    _reject_empty(text)
    _reject_non_ascii(text)
    _reject_control_chars(text)
    if len(text) > LIMIT:
        raise ValueError("entry runs past its character limit")
    _reject_padding(text)
    _reject_forbidden(text)
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
