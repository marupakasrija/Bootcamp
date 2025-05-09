from typing import Callable, Iterator

ProcessorFn = Callable[[str], str]

#level4 prestep(just in case)
StreamProcessorFn = Callable[[Iterator[str]], Iterator[str]]