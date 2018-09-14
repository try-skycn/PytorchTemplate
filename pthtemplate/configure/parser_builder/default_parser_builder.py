from .parser_builder import ParserBuilder


class DefaultParserBuilder(ParserBuilder):
    def __init__(self, prog=None):
        self._prog = prog

    def create(self):
        parser = argparse.ArgumentParser(self._prog)
        return parser

    def setup(self, parser):
        # configure randomness
        configure.add_argument('--seed', default=None, help='Random seed.')

        # configure experiment
        configure.add_argument('--expr-name', '--name', default=None, help='Experiment Name.')
        # params, settings, tensorboard, savings
