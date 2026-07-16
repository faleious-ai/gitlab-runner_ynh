from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")


FAKE_HELPERS = r"""#!/usr/bin/env bash
set -Eeuo pipefail

ynh_backup() {
    printf 'backup %s\n' "$*" >> "$FAKE_LOG"
    mkdir -p "$FAKE_ARCHIVE"
    cp -- "$FAKE_SOURCE" "$FAKE_ARCHIVE/config.toml"
}

ynh_restore_file() {
    printf 'restore %s\n' "$*" >> "$FAKE_LOG"
    mkdir -p "$FAKE_TARGET"
    cp -- "$FAKE_ARCHIVE/config.toml" "$FAKE_TARGET/config.toml"
    chmod 600 "$FAKE_TARGET/config.toml"
}

ynh_print_info() { printf 'info %s\n' "$*" >> "$FAKE_LOG"; }
ynh_script_progression() { printf 'progress %s\n' "$*" >> "$FAKE_LOG"; }
ynh_setup_source() { printf 'source %s\n' "$*" >> "$FAKE_LOG"; }
ynh_safe_rm() { printf 'remove %s\n' "$*" >> "$FAKE_LOG"; }
ynh_store_file_checksum() { printf 'checksum %s\n' "$*" >> "$FAKE_LOG"; }
"""


class LifecycleIdentityTests(unittest.TestCase):
    def test_backup_and_restore_declare_the_runner_config_contract(self) -> None:
        backup = (ROOT / "scripts" / "backup").read_text(encoding="utf-8")
        restore = (ROOT / "scripts" / "restore").read_text(encoding="utf-8")
        self.assertIn('ynh_backup --src_path="/etc/$app"', backup)
        self.assertIn('ynh_restore_file --origin_path="/etc/$app"', restore)

    def test_install_is_only_registration_lifecycle_entrypoint(self) -> None:
        install = (ROOT / "scripts" / "install").read_text(encoding="utf-8")
        restore = (ROOT / "scripts" / "restore").read_text(encoding="utf-8")
        upgrade = (ROOT / "scripts" / "upgrade").read_text(encoding="utf-8")
        self.assertIn("register_runner_set", install)
        self.assertNotIn("register_runner_set", restore)
        self.assertNotIn("register_runner_set", upgrade)
        self.assertNotIn("_register.sh", restore)
        self.assertNotIn("token", restore.lower())

    @unittest.skipUnless(BASH, "bash is required for lifecycle harness")
    def test_backup_restore_preserve_identity_without_registration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            helpers = root / "helpers"
            helpers.write_text(FAKE_HELPERS, encoding="utf-8")
            commands = root / "bin"
            commands.mkdir()
            for name in ("dpkg", "yunohost"):
                command = commands / name
                command.write_text(
                    "#!/usr/bin/env bash\nprintf '%s %s\\n' \"$0\" \"$*\" >> \"$FAKE_LOG\"\n",
                    encoding="utf-8",
                )
                os.chmod(command, 0o755)

            runner = commands / "runner"
            runner.write_text(
                "#!/usr/bin/env bash\n"
                "printf 'runner %s token=%s\\n' \"$*\" \"${CI_SERVER_TOKEN:-}\" >> \"$FAKE_RUNNER_LOG\"\n",
                encoding="utf-8",
            )
            os.chmod(runner, 0o755)

            source_config = root / "source-config.toml"
            source_config.write_text(
                '[runners]\nname = "identity-fixture"\nsystem_id = "runner-identity-fixture"\n',
                encoding="utf-8",
            )
            archive = root / "archive"
            target = root / "restored"
            target.mkdir()
            (target / "config.toml").write_text("stale identity\n", encoding="utf-8")
            log = root / "helpers.log"
            runner_log = root / "runner.log"
            env = {
                **os.environ,
                "PATH": f"{commands}{os.pathsep}{os.environ.get('PATH', '')}",
                "YH_HELPERS": str(helpers),
                "FAKE_LOG": str(log),
                "FAKE_RUNNER_LOG": str(runner_log),
                "FAKE_SOURCE": str(source_config),
                "FAKE_ARCHIVE": str(archive),
                "FAKE_TARGET": str(target),
                "RUNNER_BIN": str(runner),
                "app": "gitlab-runner",
                "gitlab_url": "https://gitlab.example",
                "token": "TEST_ONLY_TOKEN_PLACEHOLDER",
                "docker_image": "alpine:3.20",
            }

            backup_result = subprocess.run(
                [BASH, str(ROOT / "scripts" / "backup")],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(backup_result.returncode, 0, backup_result.stderr)
            self.assertIn("backup --src_path=/etc/gitlab-runner", log.read_text(encoding="utf-8"))
            self.assertEqual((archive / "config.toml").read_text(encoding="utf-8"), source_config.read_text(encoding="utf-8"))

            restore_result = subprocess.run(
                [BASH, str(ROOT / "scripts" / "restore")],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(restore_result.returncode, 0, restore_result.stderr)
            self.assertIn("restore --origin_path=/etc/gitlab-runner", log.read_text(encoding="utf-8"))
            self.assertEqual((target / "config.toml").read_text(encoding="utf-8"), source_config.read_text(encoding="utf-8"))
            self.assertEqual((target / "config.toml").stat().st_mode & 0o777, 0o600)
            self.assertFalse(runner_log.exists(), runner_log.read_text(encoding="utf-8") if runner_log.exists() else "")
            self.assertNotIn("TEST_ONLY_TOKEN_PLACEHOLDER", restore_result.stdout + restore_result.stderr)


if __name__ == "__main__":
    unittest.main()
