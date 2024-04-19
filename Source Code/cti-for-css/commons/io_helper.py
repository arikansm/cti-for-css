import os
import numpy
from src.commons.log_manager import LogManager


class IOHelper:
    @staticmethod
    def _exists(path: str) -> bool:
        return os.path.exists(path)

    class DirectoryOperator:
        @staticmethod
        def exists(directory: str) -> bool:
            return IOHelper._exists(directory)

        @staticmethod
        def create(directory: str) -> None:
            try:
                os.makedirs(directory)
                LogManager.get_logger().debug(f"directory has been created: '{directory}'")
            except Exception as e:
                LogManager.get_logger().error(f"directory could not be created: '{directory}' > " + str(e))

        @staticmethod
        def create_if_not_exist(directory: str) -> None:
            if not IOHelper.DirectoryOperator.exists(directory):
                IOHelper.DirectoryOperator.create(directory)
            else:
                LogManager.get_logger().debug(f"directory could not be created because it exists: '{directory}'")

    class FileOperator:
        def __init__(self):
            pass

        @staticmethod
        def exists(file: str) -> bool:
            return IOHelper._exists(file)

        @staticmethod
        def read_content(file_path: str) -> str:
            file = open(file_path, "r")
            content = file.read()
            file.close()
            return content

        @staticmethod
        def read_bytes_as_bit(file_path: str) -> numpy.ndarray:
            try:
                LogManager.get_logger().debug(f"file content (bytes) is going to be read: '{file_path}'")
                bytes_as_number = numpy.fromfile(open(file_path, "rb"), dtype=numpy.uint8)
                content_as_bits = numpy.unpackbits(bytes_as_number)
                LogManager.get_logger().debug(f"{len(bytes_as_number):,} bytes"
                                              + f" ({len(content_as_bits):,} bits) of the file have been read"
                                              + f": '{file_path}'")
                return content_as_bits
            except Exception as e:
                LogManager.get_logger().error(f"file content could not be read: '{file_path}' > " + str(e))
                return numpy.empty(0, dtype=int)

        @staticmethod
        def get_file_name_from_path(file_path: str) -> str:
            head, tail = os.path.split(file_path)
            return tail

        @staticmethod
        def write_content_as_string(file_path: str, file_content: str) -> bool:
            try:
                file = open(file_path, "w")
                file.write(file_content)
                file.close()
                return True
            except Exception as e:
                LogManager.get_logger().error(f"content could not be written for the file: '{file_path}' > " + str(e))
                return False

        @staticmethod
        def write_content_as_ndarray(file_path: str, numpy_ndarray: numpy.ndarray) -> bool:
            try:
                numpy_ndarray.tofile(file_path)
                return True
            except Exception as e:
                LogManager.get_logger().error(f"content could not be written for the file: '{file_path}' > " + str(e))
                return False
