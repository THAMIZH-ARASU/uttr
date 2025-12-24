class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_cut = False
        self.loop_should_skip = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_cut = res.loop_should_cut
        self.loop_should_skip = res.loop_should_skip
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def success_cut(self):
        self.reset()
        self.loop_should_cut = True
        return self

    def success_skip(self):
        self.reset()
        self.loop_should_skip = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return self.error or self.func_return_value or self.loop_should_cut or self.loop_should_skip