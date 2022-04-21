class FuncProxy:
    def __init__(self, fn):
        self._caller = fn

    def __getattr__(self, attr):
        return getattr(self._caller(), attr)
