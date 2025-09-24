from mmprobe.base import load_probe


def test_color_binding_generates():
    p = load_probe("color_binding")
    samples = list(p.generate(n=8, seed=2))
    assert len(samples) == 8
    for s in samples:
        assert s.answer in {"circle", "square", "triangle"}
