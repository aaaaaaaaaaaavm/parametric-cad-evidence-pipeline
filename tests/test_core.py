import tempfile
import unittest
from pathlib import Path
from cad_evidence import build_manifest, verify_manifest

class CoreTests(unittest.TestCase):
    def test_manifest_detects_change(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/"source.py").write_text("a=1")
            (root/"part.step").write_text("solid")
            manifest=build_manifest(root,["source.py"],["part.step"],{"length_mm":20})
            self.assertEqual(verify_manifest(root,manifest),[])
            (root/"part.step").write_text("changed")
            self.assertEqual(verify_manifest(root,manifest),["changed: part.step"])

if __name__ == "__main__": unittest.main()
