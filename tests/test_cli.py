import unittest
import subprocess
import sys

class TestCLI(unittest.TestCase):

    def test_cli_version(self):
        command = [sys.executable, "/home/elizabeth/voxunity-ai/cli/main.py", "--version"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertIn("0.1.0", result.stdout)

    def test_cli_voice_command(self):
        command = [sys.executable, "/home/elizabeth/voxunity-ai/cli/main.py", "voice", "start", "--preset", "robot"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertIn("Voice command: start with preset robot", result.stdout)

    def test_cli_streaming_command(self):
        command = [sys.executable, "/home/elizabeth/voxunity-ai/cli/main.py", "streaming", "start", "--overlay", "alert"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertIn("Streaming command: start with overlay alert", result.stdout)

if __name__ == '__main__':
    unittest.main()
