from __future__ import annotations

import datetime as dt
import json
import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / "evidence" / "upstream" / "alpine-support-matrix.json"
EXACT_PATCH_IMAGE = re.compile(r"^alpine:(\d+)\.(\d+)\.(\d+)$")


class SupportedDockerDefaultAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
        self.manifest = tomllib.loads((ROOT / "manifest.toml").read_text(encoding="utf-8"))
        self.panel = tomllib.loads((ROOT / "config_panel.toml").read_text(encoding="utf-8"))

    def test_support_matrix_has_primary_source_and_dated_registry_observation(self) -> None:
        self.assertEqual(self.matrix["artifact_kind"], "upstream-support-matrix")
        self.assertEqual(self.matrix["distribution"], "alpine")
        self.assertEqual(self.matrix["release_source"], "https://www.alpinelinux.org/releases/")
        self.assertEqual(self.matrix["registry_source"], "https://hub.docker.com/_/alpine/tags/")
        self.assertRegex(self.matrix["observed_at"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(
            self.matrix["registry_observation"]["observed_at"],
            self.matrix["observed_at"],
        )

    def test_default_is_exact_supported_patch_observed_in_official_registry(self) -> None:
        install_default = self.manifest["install"]["docker_image"]["default"]
        panel_default = self.panel["main"]["registration"]["docker_image"]["default"]
        self.assertEqual(panel_default, install_default)
        self.assertNotIn("latest", install_default.lower())
        self.assertNotIn("edge", install_default.lower())

        match = EXACT_PATCH_IMAGE.fullmatch(install_default)
        self.assertIsNotNone(
            match,
            "RED: Docker default must use an exact Alpine patch tag such as alpine:3.24.1",
        )
        assert match is not None
        branch = f"{match.group(1)}.{match.group(2)}"
        tag = ".".join(match.groups())

        self.assertIn(branch, self.matrix["branches"])
        observed_at = dt.date.fromisoformat(self.matrix["observed_at"])
        end_of_support = dt.date.fromisoformat(self.matrix["branches"][branch]["end_of_support"])
        self.assertGreater(
            end_of_support,
            observed_at,
            f"RED: Alpine {branch} support ended on {end_of_support}",
        )
        self.assertNotEqual(self.matrix["branches"][branch]["support_level"], "on-request")
        self.assertIn(
            tag,
            self.matrix["registry_observation"]["tags"],
            "RED: exact tag was not observed in the official Docker Alpine registry",
        )


if __name__ == "__main__":
    unittest.main()
