import os
import stat
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConfigControllerTests(unittest.TestCase):
    def test_panel_declares_ephemeral_inputs_and_register_button(self):
        panel = tomllib.loads((ROOT / "config_panel.toml").read_text(encoding="utf-8"))
        manifest = tomllib.loads((ROOT / "manifest.toml").read_text(encoding="utf-8"))
        registration = panel["main"]["registration"]
        self.assertEqual(registration["register"]["type"], "button")
        for name, expected_type in {
            "gitlab_url": "url",
            "token": "password",
            "docker_image": "string",
        }.items():
            self.assertEqual(registration[name]["type"], expected_type)
            self.assertEqual(registration[name]["bind"], "null")
        self.assertEqual(registration["docker_image"]["default"], "alpine:3.24.1")
        self.assertEqual(registration["docker_image"]["default"], manifest["install"]["docker_image"]["default"])

    def test_public_controller_delegates_to_shared_helper_without_secret_argv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            runner = path / "runner"
            argv_log = path / "argv.log"
            env_log = path / "env.log"
            runner.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$*\" > \"$ARGV_LOG\"\n"
                "printf 'url=%s\\ntoken=%s\\nmode=%s\\n' \"$CI_SERVER_URL\" \"$CI_SERVER_TOKEN\" \"$REGISTER_NON_INTERACTIVE\" > \"$ENV_LOG\"\n",
                encoding="utf-8",
            )
            runner.chmod(runner.stat().st_mode | stat.S_IXUSR)
            token = "controller-" + "placeholder"
            env = {
                **os.environ,
                "RUNNER_BIN": str(runner),
                "ARGV_LOG": str(argv_log),
                "ENV_LOG": str(env_log),
                "gitlab_url": "https://gitlab.example/",
                "token": token,
                "docker_image": "alpine:3.20",
            }
            result = subprocess.run(
                ["bash", "-c", "source scripts/config; run__register"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(token, argv_log.read_text(encoding="utf-8"))
            self.assertIn("token=" + token, env_log.read_text(encoding="utf-8"))
            self.assertIn("mode=true", env_log.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
