from utils import clamp
import builtins
import sys
from time import sleep

try:
    from ipywidgets import Output, display

except ImportError:
    pass

# TODO: add stderr progress bar printer


class ProgressBar:
    def __init__(self, prefix='', decimals=1, length=100, fill='█'):
        self.prefix = prefix
        self.decimals = decimals
        self.length = length
        self.fill = fill

        self.progress = 0

    def __str__(self):
        percent = f"{100 * self.progress:.{self.decimals}f}"
        filled = int(self.length * self.progress)
        bar = self.fill * filled + '-' * (self.length - filled)

        return f"\r{self.prefix} |{bar}| {percent}%"

    @staticmethod
    def display(value):
        sys.stdout.write(value)

    def __call__(self, func):
        def decorated(*args, **kwargs):
            global print
            progress_generator = func(*args, **kwargs)
            self.display(self)

            try:
                # monkey patch print to show progress bar neatly
                # with other output
                print = self._print

                while True:
                    progress = clamp(next(progress_generator), 0, 1)
                    self.progress = progress
                    self.display(self)

            except StopIteration as result:
                self.progress = 1
                self.display(self)
                return result.value
            finally:
                # un-patch print
                print = builtins.print

        return decorated

    def _print(self, *args, **kwargs):
        '''
        monkey patch built in print call to clear current line,
        print output, and add progress bar to new line

        :param args:    arguments to print
        :param kwargs:  keyword arguments to print

        :return: None
        '''

        # clear line
        bar = str(self)
        self.display('\r'.ljust(len(bar), ' ')+'\r')

        # show content, using built in print since print is
        # monkey patched with this function
        builtins.print(*args, **kwargs)

        # re print progress bar
        self.display(bar)


class JupyterProgressBar(ProgressBar):
    def __init__(self, *args, **kwargs):
        self.bar = Output()
        self.out = Output()

    def display(self, value):
        self.bar.clear_output(wait=True)
        with self.bar:
           sys.stdout.write(value)

        # show output widgets in notebook
        display(self.bar)
        display(self.out)

    def _print(self, *args, **kwargs):
        # print output to a separate display widget
        with self.out:
            builtins.print(*args, **kwargs)
