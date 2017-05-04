from distributions.Distribution import Distribution


class Uniform(Distribution):
    def next(self):
        return self.random.randint(int(self.params["low_boundary"]), int(self.params["up_boundary"]))
