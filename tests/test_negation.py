from mmprobe.base import load_probe


def test_negation_inverts_answer():
    p = load_probe("negation")
    samples = list(p.generate(n=20, seed=7))
    for s in samples:
        # answer should be "yes" iff object is NOT present
        assert (s.answer == "yes") == (not s.meta["present"])
