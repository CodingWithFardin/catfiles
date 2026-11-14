import os
import tempfile
import unittest

from catfiles import collect, render


class CatTest(unittest.TestCase):
    def test_render_fence(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "a.py")
            open(p, "w").write("print(1)\n")
            out = render([p], tmp)
            self.assertIn("### a.py", out)
            self.assertIn("\`\`\`python", out)

    def test_collect_skips_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            open(os.path.join(tmp, ".hidden"), "w").write("x")
            self.assertEqual(collect(tmp), [])


if __name__ == "__main__":
    unittest.main()
