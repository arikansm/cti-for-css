import datetime
import stix2 as stix

from src.commons.log_manager import LogManager
from src.commons.io_helper import IOHelper
from src.commons.configuration_manager import ConfigurationManager


# noinspection PyMethodMayBeStatic
class Builder:
    def __init__(self, function_info: dict):
        self.__logger = LogManager.get_logger()
        self.__binary_path = function_info["binary_path"]
        self.__prepared_binary_path = function_info["prepared_binary_path"]
        self.__vulnerable_functions = function_info["vulnerable_functions"]

    def build(self) -> dict:
        file_info = self.__get_file_info()
        function_info = self.__get_decompiled_vulnerable_functions()
        return self.__build_cti_report(file_info, function_info)

    def __get_file_info(self) -> dict:
        info_file_path = self.__prepared_binary_path + ".file_info"
        info_file_content = IOHelper.FileOperator.read_content(info_file_path).split("\n")

        file_metadata = self.__get_file_metadata(info_file_content)
        file_version_strings = self.__get_file_version(info_file_content)

        merged_dictionary = file_metadata
        merged_dictionary.update(file_version_strings)
        return merged_dictionary

    def __get_file_metadata(self, info_file_content: str) -> dict:
        info_file_content_processed_for_metadata = []
        for line in info_file_content:
            try:
                line_info = line.split(":", 1)  # to split from the first occurrence
                info_file_content_processed_for_metadata.append([line_info[0].strip(), line_info[1].strip()])
            except:
                pass

        return {
            "file_format": self.__get_specific_metadata(info_file_content_processed_for_metadata, "File format"),
            "file_class": self.__get_specific_metadata(info_file_content_processed_for_metadata, "File class"),
            "architecture": self.__get_specific_metadata(info_file_content_processed_for_metadata, "Architecture"),
            "number_of_import": self.__get_specific_metadata(info_file_content_processed_for_metadata,
                                                             "Number of imports"),
            "number_of_resources": self.__get_specific_metadata(info_file_content_processed_for_metadata,
                                                                "Number of resources"),
            "sha256": self.__get_specific_metadata(info_file_content_processed_for_metadata,
                                                   "SHA256")

        }

    def __get_specific_metadata(self, info_file_content_processed: list[list[str]], key) -> str:
        for line_info in info_file_content_processed:
            try:
                if line_info[0] == key:
                    return line_info[1]
            except:
                continue

        return ""

    def __get_file_version(self, info_file_content: str) -> dict:
        info_file_content_filtered = ""
        try:
            info_file_content_filtered = info_file_content[info_file_content.index("Version info strings")
                                                           :info_file_content.index("Version info languages")]
        except ValueError:
            return {}

        info_file_content_processed_for_version = []
        for line in info_file_content_filtered:
            try:
                line_info = [line_info for line_info in line.split(" ") if len(line_info) != 0]
                info_file_content_processed_for_version.append(line_info)
            except:
                pass

        return {
            "company_name": self.__get_specific_version_data(info_file_content_processed_for_version, "CompanyName"),
            "file_description": self.__get_specific_version_data(info_file_content_processed_for_version,
                                                                 "FileDescription"),
            "internal_name": self.__get_specific_version_data(info_file_content_processed_for_version, "InternalName"),
            "legal_copyright": self.__get_specific_version_data(info_file_content_processed_for_version,
                                                                "LegalCopyright"),
            "original_filename": self.__get_specific_version_data(info_file_content_processed_for_version,
                                                                  "OriginalFilename"),
            "product_name": self.__get_specific_version_data(info_file_content_processed_for_version, "ProductName"),
            "product_version": self.__get_specific_version_data(info_file_content_processed_for_version,
                                                                "ProductVersion")
        }

    def __get_specific_version_data(self, info_file_content_processed: list[list[str]], key) -> str:
        for line_info in info_file_content_processed:
            try:
                if line_info[1] == key:
                    return " ".join(line_info[2:])
            except:
                continue

        return ""

    def __get_decompiled_vulnerable_functions(self) -> dict:
        c_file_path = self.__prepared_binary_path + ".c"
        c_file_content = IOHelper.FileOperator.read_content(c_file_path).split("// Address range: ")
        functions = {}
        for vulnerable_function in self.__vulnerable_functions:
            function_info_parsed = [function_info for function_info in vulnerable_function.split(" ")
                                    if any(char.isdigit() for char in function_info)]

            search_term = f"{function_info_parsed[-2]} - {function_info_parsed[-1]}"
            for function_lines in c_file_content:
                if search_term in function_lines:
                    functions[search_term] = function_lines.replace(search_term + "\n", "")

            if not search_term in functions:
                functions[search_term] = "The code could not be decompiled to the representation of C programming language"

        return functions

    def __build_cti_report(self, file_info, function_info) -> dict:
        stix_objects = []

        # creation of domain objects

        identity = stix.Identity(name=self.__get_value_from_file_info(file_info, "company_name"),
                                 description=self.__get_value_from_file_info(file_info, "legal_copyright"),
                                 roles=["producer"])
        stix_objects.append(identity)

        indicator_hash = stix.Indicator(description="hash-sha256",
                                        pattern=self.__get_value_from_file_info(file_info, "sha256"),
                                        pattern_type="hash")
        stix_objects.append(indicator_hash)

        indicator_version = stix.Indicator(description="version",
                                           pattern=self.__get_value_from_file_info(file_info, "product_version"),
                                           pattern_type="version")
        stix_objects.append(indicator_version)

        infrastructure_original_file_name = stix.Infrastructure(name=self.__get_value_from_file_info(file_info, "original_filename"),
                                                                description="original file name",
                                                                infrastructure_types=["binary"])
        stix_objects.append(infrastructure_original_file_name)

        infrastructure_internal_name = stix.Infrastructure(name=self.__get_value_from_file_info(file_info, "internal_name"),
                                                           description="internal name",
                                                           infrastructure_types=["binary"])
        stix_objects.append(infrastructure_internal_name)

        location = stix.Location(description=self.__get_value_from_file_info(file_info, "product_name"), region="unknown")
        stix_objects.append(location)

        malware = stix.Malware(malware_types=["exploitable"],
                               architecture_execution_envs=self.__get_value_from_file_info(file_info, "architecture"), is_family=False)
        stix_objects.append(malware)

        function_info_identifiers = []
        for function_range, function_code in function_info.items():
            identity = stix.Software(name=function_range,
                                     languages=["acquire the related note to see the code in the C programming "
                                                f"language representation, which is between addresses {function_range} "
                                                "when decompiled to assembly"])
            note = stix.Note(authors=[function_range],
                             content=function_code,
                             object_refs=[identity])
            stix_objects.append(identity)
            stix_objects.append(note)
            function_info_identifiers.append(identity)
        observed_data = stix.ObservedData(object_refs=function_info_identifiers,
                                          first_observed=datetime.datetime.now(),
                                          last_observed=datetime.datetime.now(),
                                          number_observed=len(function_info_identifiers))
        stix_objects.append(observed_data)

        # creation of relationship objects

        relationship_for_identity = stix.Relationship(relationship_type="located-at",
                                                      source_ref=identity,
                                                      target_ref=location)
        stix_objects.append(relationship_for_identity)

        relationship_for_indicator_hash = stix.Relationship(relationship_type="indicates",
                                                            source_ref=indicator_hash,
                                                            target_ref=malware)
        stix_objects.append(relationship_for_indicator_hash)

        relationship_for_indicator_version = stix.Relationship(relationship_type="indicates",
                                                               source_ref=indicator_version,
                                                               target_ref=malware)
        stix_objects.append(relationship_for_indicator_version)

        relationship_for_infrastructure_internal_name = stix.Relationship(relationship_type="consists-of",
                                                                          source_ref=infrastructure_internal_name,
                                                                          target_ref=observed_data)
        stix_objects.append(relationship_for_infrastructure_internal_name)

        relationship_for_infrastructure_original_file_name = stix.Relationship(relationship_type="consists-of",
                                                                               source_ref=infrastructure_original_file_name,
                                                                               target_ref=observed_data)
        stix_objects.append(relationship_for_infrastructure_original_file_name)

        relationship_for_malware1 = stix.Relationship(relationship_type="originates-from",
                                                      source_ref=malware,
                                                      target_ref=location)
        relationship_for_malware2 = stix.Relationship(relationship_type="controls",
                                                      source_ref=infrastructure_internal_name,
                                                      target_ref=malware)
        relationship_for_malware3 = stix.Relationship(relationship_type="controls",
                                                      source_ref=infrastructure_original_file_name,
                                                      target_ref=malware)
        stix_objects.append(relationship_for_malware1)
        stix_objects.append(relationship_for_malware2)
        stix_objects.append(relationship_for_malware3)

        for function in function_info_identifiers:
            relationship_for_function = stix.Relationship(relationship_type="consists-of",
                                                          source_ref=function,
                                                          target_ref=malware)
            stix_objects.append(relationship_for_function)

        report = stix.Report(name=self.__binary_path, object_refs=stix_objects, published=datetime.datetime.now())
        stix_objects.append(report)

        return {'stix_objects': stix_objects, 'function_identifiers': function_info_identifiers, 'malware': malware}

    def __get_value_from_file_info(self, file_info: dict, key: str) -> str:
        value = file_info.get(key)
        return "unknown" if value is None else value
