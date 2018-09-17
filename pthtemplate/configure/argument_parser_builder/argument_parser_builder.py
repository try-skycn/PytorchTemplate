import argparse


__all__ = ['ParserCreator', 'SubparsersCreator', 'ArgumentAdder', 'SubparserSetter']


class ParserCreator:
    def apply(self, argparse):
        """
        Should be inherited.
        """
        raise NotImplementedError


class DefaultParserCreator(ParserCreator):
    def apply(self, argparse):
        return argparse.ArgumentParser()


class SubparsersCreator:
    def apply(self, parser):
        raise NotImplementedError


class DefaultSubparsersCreator(SubparsersCreator):
    def apply(self, parser):
        return parser.add_subparsers()


class ArgumentAdder:
    def apply(self, parser):
        raise NotImplementedError


class SubparserSetter:
    def apply(self, subparsers):
        subparser = self.build(subparsers)
        self.setup(subparser)

    def build(self, subparsers):
        """
        Should be inherited.
        Build the subparser.
        Usually this function is implemented as subparsers.add_parser(...)
        """
        raise NotImplementedError

    def setup(subparser):
        """
        Should be inherited.
        Add arguments for subparser.
        Usually this function is implemented as several subparser.add_argument(...) (s).
        """
        raise NotImplementedError


class ArgumentParserBuilder:
    def __init__(self):
        """
        Inherit this constructor.
        """
        self._parser_creator = None
        self._subparsers_creator = None
        self._argument_adder_list = []
        self._subparser_setter_list = []

    def register(self, obj):
        if isinstance(obj, ParserCreator):
            self._parser_creator = obj
        elif isinstance(obj, SubparsersCreator):
            self._subparsers_creator = obj
        elif isinstance(obj, ArgumentAdder):
            self._argument_adder_list.append(obj)
        elif isinstance(obj, SubparserSetter):
            self._subparser_setter_list.append(obj)
        else:
            raise Type('Invalid type(obj) for registering, get {}.'.format(type(obj)))

    def _set_default_values(self):
        if self._parser_creator is None:
            self._parser_creator = DefaultParserCreator()
        if self._subparsers_creator is None:
            self._subparsers_creator = DefaultSubparsersCreator()

    def _create_subparsers(self, parser):
        if len(self._subparser_setter_list) == 0:
            return None
        else:
            return self._subparsers_creator.apply(parser)

    def apply(self):
        self._set_default_values()
        parser = ParserCreator.apply(argparse)
        # add arguments
        for argument_adder in self._argument_adder_list:
            argument_adder.apply(parser)
        # setup subparsers
        subparsers = self._create_subparsers(parser)
        if subparsers is not None:
            for subparser_setter in self._subparser_setter_list:
                subparser_setter.apply(subparsers)
        return parser
