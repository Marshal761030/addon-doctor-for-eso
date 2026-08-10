from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from addon_doctor.paths import candidate_addons_directories, detect_addons_directory


class PathTests(unittest.TestCase):
    def test_candidate_paths_use_windows_environment(self) -> None:
        with patch.dict(
            "os.environ",
            {"USERPROFILE": r"C:\\Users\\Tester", "OneDrive": r"D:\\OneDrive"},
            clear=True,
        ):
            candidates = candidate_addons_directories()

        self.assertEqual(len(candidates), 2)
        self.assertIn("Elder Scrolls Online", str(candidates[0]))

    def test_detect_returns_none_when_candidates_do_not_exist(self) -> None:
        with TemporaryDirectory() as temp_dir:
            fake = str(Path(temp_dir) / "User")
            with patch.dict("os.environ", {"USERPROFILE": fake}, clear=True):
                self.assertIsNone(detect_addons_directory())


if __name__ == "__main__":
    unittest.main()
