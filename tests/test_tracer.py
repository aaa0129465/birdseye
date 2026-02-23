import sys
import unittest

from tests.utils import requires_python_version


class TestTreeTrace(unittest.TestCase):
    maxDiff = None

    @requires_python_version(3.5)
    def test_async_supported(self):
        import asyncio
        import inspect
        from birdseye.tracer import TreeTracerBase
        tracer = TreeTracerBase()

        namespace = {"tracer": tracer}
        exec("""
@tracer
async def f(x):
    y = x + 1
    return y
""", namespace)
        f = namespace["f"]
        self.assertTrue(inspect.iscoroutinefunction(f))

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(f(1))
        finally:
            loop.close()
            asyncio.set_event_loop(None)
        self.assertEqual(result, 2)

        if sys.version_info >= (3, 6):
            with self.assertRaises(ValueError):
                exec("""
@tracer
async def f(): yield 1""")
