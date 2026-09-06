"""Adapter registry. Add your site here."""


def load(name):
    if name == "roblox":
        from . import roblox
        return roblox.make()
    if name == "noblob":
        from . import noblob
        return noblob.make()
    raise SystemExit(f"unknown adapter '{name}'. Available: roblox, noblob")
