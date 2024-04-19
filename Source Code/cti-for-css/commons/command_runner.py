import subprocess
import platform
from abc import abstractmethod
from src.commons.log_manager import LogManager


class CommandRunner:
    def __init__(self):
        self.__logger = LogManager.get_logger()

        match platform.system():
            case "Windows":
                self.__os_dependent_runner: CommandRunner._IOsDependentRunner = CommandRunner._Windows()
            case "Linux":
                self.__os_dependent_runner: CommandRunner._IOsDependentRunner = CommandRunner._Linux()
            case "Darwin":
                self.__os_dependent_runner: CommandRunner._IOsDependentRunner = CommandRunner._Macos()
            case _:
                raise Exception("unsupported operating system")

    def execute(self, command: str) -> str:
        return self.__os_dependent_runner.execute(command)

    def execute_custom(self, binary: str, command: str, parameter: str) -> str:
        self.__logger.debug(f"Custom command is going to be run with '{parameter}' via '{binary}': '{command}'")
        try:
            completed_process = subprocess.run([binary, command, parameter],
                                               check=True, capture_output=True, encoding="utf-8")
            self.__logger.debug(f"Custom command has been successfully run with '{parameter}' via '{binary}': '{command}'")
            return completed_process.stdout
        except Exception as e:
            self.__logger.error(
                f"Custom command could not be run with '{parameter}' via '{binary}': '{command}' > " + str(e))
            return ""

    class _IOsDependentRunner:
        def __init__(self):
            self._logger = LogManager.get_logger()

        @abstractmethod
        def execute(self, parameter: str) -> str:
            pass

    class _Windows(_IOsDependentRunner):
        def __init__(self):
            super().__init__()

        def execute(self, parameter: str) -> str:
            self._logger.debug(f"Windows command is going to be run via 'cmd.exe': '{parameter}'")
            try:
                completed_process = subprocess.run(["cmd", "/c", parameter],
                                                   check=True, capture_output=True, encoding="utf-8")
                self._logger.debug(f"Windows command has been successfully run via 'cmd.exe': '{parameter}'")
                return completed_process.stdout
            except Exception as e:
                self._logger.error(f"Windows command could not be run via 'cmd.exe': '{parameter}' > " + str(e))
                return ""

    class _Linux(_IOsDependentRunner):
        def __init__(self):
            super().__init__()

        def execute(self, parameter: str) -> str:
            self._logger.debug(f"Linux command is going to be run via 'bash': '{parameter}'")
            try:
                completed_process = subprocess.run(["bash", "-c", parameter],
                                                   check=True, capture_output=True, encoding="utf-8")
                self._logger.debug(f"Linux command has been successfully run via 'bash': '{parameter}'")
                return completed_process.stdout
            except Exception as e:
                self._logger.error(f"Linux command could not be run via 'bash': '{parameter}' > " + str(e))
                return ""

    class _Macos(_IOsDependentRunner):
        def __init__(self):
            super().__init__()

        def execute(self, parameter: str) -> str:
            self._logger.debug(f"Macos command is going to be run via 'zsh': '{parameter}'")
            try:
                completed_process = subprocess.run(["zsh", "-c", parameter],
                                                   check=True, capture_output=True, encoding="utf-8")
                self._logger.debug(f"Macos command has been successfully run via 'zsh': '{parameter}'")
                return completed_process.stdout
            except Exception as e:
                self._logger.error(f"Macos command could not be run via 'zsh': '{parameter}' > " + str(e))
                return ""
