from mmprobe.base import load_probe, list_probes


def test_all_probes_generate_something():
    for name in list_probes():
        p = load_probe(name)
        samples = list(p.generate(n=3, seed=0))
        assert len(samples) == 3


def test_size_compare_is_correct():
    p = load_probe("size_compare")
    for s in p.generate(n=20, seed=0):
        assert s.answer in {"red", "blue"}
        if s.meta["r1"] > s.meta["r2"]:
            assert s.answer == "red"
        else:
            assert s.answer == "blue"
