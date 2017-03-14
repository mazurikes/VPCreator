import inspect


class Logger:

    def info(self, message, show_caller=False):
        if show_caller:
            string = '<I> From "{}()": {}'.format(inspect.stack()[1][3], message)
        else:
            string = '<I> {}'.format(inspect.stack()[1][3], message)
        print(string)

    def error(self, message, show_caller=False):
        if show_caller:
            string = '<E> From "{}()": {}'.format(inspect.stack()[1][3], message)
        else:
            string = '<E> {}'.format(inspect.stack()[1][3], message)
        print(string)

log = Logger()
