from typing import Callable

from src.commons.command_runner import CommandRunner
from src.commons.configuration_manager import ConfigurationManager
from src.commons.io_helper import IOHelper
from src.commons.log_manager import LogManager


class MachineCodeDecompiler:
    __RETDEC_FILE_INFO_HEADER = "##### Gathering file information..."
    __RETDEC_UNPACK_HEADER = "##### Trying to unpack"

    def __init__(self):
        self.__logger = LogManager.get_logger()
        self.__runner = CommandRunner()

        if (ConfigurationManager.CyberThreatIntelligence.build_cti and
                not IOHelper.DirectoryOperator.exists(ConfigurationManager.Reconstruction.retdec_installation_directory)):
            raise Exception(
                f"retdec could not be found at '{ConfigurationManager.Reconstruction.retdec_installation_directory}'"
                + ". You can configure another path with "
                  "'ConfigurationManager.Reconstruction.retdec_installation_directory'")

    def decompile_binary_to_file(self, file_path: str, temp_file_path_generator: Callable[[str], str]) -> str:
        if not IOHelper.FileOperator.exists(file_path):
            self.__logger.error(f"File could not be found: '{file_path}'")
            return ""

        temp_file_path = temp_file_path_generator(file_path)
        IOHelper.DirectoryOperator.create_if_not_exist(temp_file_path[:temp_file_path.rfind('\\')])

        self.__logger.debug(f"The reconstruction process has been started for the file '{file_path}' ")
        retdec_output = self.__decompile_with_retdec(file_path, temp_file_path)
        self.__logger.debug(f"The reconstruction process has been finished successfully for the file: '{file_path}'")

        if retdec_output != "":
            self.__logger.debug(f"Additional information is going to be acquired from the file '{file_path}'")
            decode_result = self.__save_decoded_file_information(retdec_output, temp_file_path)
            if decode_result:
                self.__logger.debug(f"Additional information has been successfully acquired for the file '{file_path}'")
                return temp_file_path
            else:
                self.__logger.debug(f"Additional information could not be acquired from the file '{file_path}'")
                return ""
        else:
            return ""

    def __decompile_with_retdec(self, file_path: str, temp_file_path: str) -> str:
        retdec_output = self.__runner.execute(
            "py -3 " + ConfigurationManager.Reconstruction.retdec_installation_directory
            + r"\bin\retdec-decompiler.py"
            + " --cleanup --fileinfo-verbose --output-format plain"
            + f" --output " + temp_file_path + ".c" + " " + file_path)
        return retdec_output

    def __save_decoded_file_information(self, retdec_output: str, temp_file_path: str) -> bool:
        file_info_position = retdec_output.index(self.__RETDEC_FILE_INFO_HEADER) + len(self.__RETDEC_FILE_INFO_HEADER)
        file_info = retdec_output[
                    file_info_position:retdec_output.index(self.__RETDEC_UNPACK_HEADER, file_info_position)]

        return IOHelper.FileOperator.write_content_as_string(temp_file_path + ".file_info", file_info)
