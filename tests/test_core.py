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

class IntegrityRegressionTests(unittest.TestCase):
    def test_parameter_tampering_and_incomplete_manifest_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            manifest=build_manifest(folder,[],[],{"length_mm":20})
            manifest["parameters"]["length_mm"]=21
            self.assertIn("changed: parameters",verify_manifest(folder,manifest))
            self.assertTrue(verify_manifest(folder,{}))
    def test_nonfinite_parameters_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError): build_manifest(folder,[],[],{"length_mm":float("nan")})
    def test_external_path_is_rejected_even_with_matching_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/"project";root.mkdir()
            external=Path(folder)/"outside.step";external.write_text("solid")
            from hashlib import sha256
            manifest=build_manifest(root,[],[],{})
            manifest["artifacts"]=[{"path":"../outside.step","bytes":5,"sha256":sha256(b"solid").hexdigest()}]
            self.assertIn("out-of-root path: ../outside.step",verify_manifest(root,manifest))
