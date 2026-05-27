class _FillMeIn:
    """Sentinel value students replace with their answer."""

    def __repr__(self):
        return "FILL_ME_IN"

    def __eq__(self, other):
        raise AssertionError(
            "\n\n  Fill in the blank!\n"
            "  Replace FILL_ME_IN with your answer and try again.\n"
        )

    def __ne__(self, other):
        return True   # FILL_ME_IN is not equal to anything

    def __hash__(self):
        return id(self)


FILL_ME_IN = _FillMeIn()
