"""Basic sanity tests — no model loading."""
from mmprobe.base import load_probe, list_probes


def test_list_probes():
    probes = list_probes()
    assert "counting" in probes


def test_counting_generates():
    p = load_probe("counting")
    samples = list(p.generate(n=5, seed=0))
    assert len(samples) == 5
    for s in samples:
        assert s.image is not None
        assert s.answer.isdigit()


def test_counting_score():
    p = load_probe("counting")
    samples = list(p.generate(n=10, seed=1))
    # if the model just echoes the answer back, score should be True
    for s in samples:
        assert p.score(s, s.answer) is True
