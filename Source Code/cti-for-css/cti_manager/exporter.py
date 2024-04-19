import datetime

import stix2 as stix
from src.commons.log_manager import LogManager
from src.commons.io_helper import IOHelper
from src.commons.configuration_manager import ConfigurationManager


class Exporter:
    def __init__(self):
        self.__logger = LogManager.get_logger()

    def export(self, stix_dictionary_list: list[dict]) -> None:
        stix_dictionary_list = [dictionary for dictionary in stix_dictionary_list if dictionary is not None and dictionary != {}]
        if len(stix_dictionary_list) == 0:
            self.__logger.debug(f"as there is no vulnerable function(s) in binary(s), "
                                f"cyber threat intelligence has not been created")
        else:
            bundle_elements = self.__prepare_stix_with_common_objects(stix_dictionary_list)
            bundle_object = stix.Bundle(objects=bundle_elements)
            bundle_content = bundle_object.serialize(pretty=True)
            file_name = f"{str(datetime.datetime.now().timestamp()).replace('.', '')}.cti-for-css"
            cti_file_path = f"{ConfigurationManager.CyberThreatIntelligence.save_path}/{file_name}"
            IOHelper.FileOperator.write_content_as_string(cti_file_path, bundle_content)
            self.__logger.debug(f"The cyber threat intelligence file has been created: {cti_file_path}")

    def __prepare_stix_with_common_objects(self, stix_dictionary_list: list[dict]) -> list:

        # creation of common domain objects
        bundle_elements = []

        attack_pattern = stix.AttackPattern(name="attack by reading from or writing to a memory location that is "
                                                 "outside of the intended boundary of the buffer",
                                            description="an attacker might be capable of using any input field in the "
                                                        "application. He/She or an automated tool can provide "
                                                        "information whose length is greater than the buffer")
        bundle_elements.append(attack_pattern)

        campaign = stix.Campaign(name="external harmful groups",
                                 description="groups such as anonymous, dragonfly, etc.")
        bundle_elements.append(campaign)

        course_of_action = stix.CourseOfAction(name="remediation of CWE-119 and CWE-399",
                                               description="Use automatic buffer overflow detection mechanisms that "
                                                           "are offered by certain compilers or compiler extensions. "
                                                           "Examples include: the Microsoft Visual Studio /GS flag, "
                                                           "Fedora/Red Hat FORTIFY_SOURCE GCC flag, StackGuard, "
                                                           "and ProPolice, which provide various mechanisms including "
                                                           "canary-based detection and range/index checking. ")
        bundle_elements.append(course_of_action)

        intrusion_set = stix.IntrusionSet(name="internal employees",
                                          description="who know the vulnerability exists i.e. disgruntled employees, "
                                                      "attackers who acquired an internal asset, etc.")
        bundle_elements.append(intrusion_set)

        malware_analysis = stix.MalwareAnalysis(product="cti-for-css", configuration_version="deep-learning",
                                                result=f"greater than {ConfigurationManager.CyberThreatIntelligence.vulnerability_threshold}")
        bundle_elements.append(malware_analysis)

        note = stix.Note(authors=["programmer of the cti-for-css"],
                         content="The AI driven result(s) are experimental. "
                                 "False positive(s) and/or false negative(s) might be occurred",
                         object_refs=[malware_analysis])
        bundle_elements.append(note)

        threat_actor = stix.ThreatActor(name="internal and external user(s)",
                                        description="any individual(s), group(s) or organization(s) who wants to "
                                                    "see, change and/or destroy data at rest in the system memory",
                                        goals=["confidentiality", "integrity", "availability"])
        bundle_elements.append(threat_actor)

        tool = stix.Tool(name="attack automation tool(s) and/or script(s)",
                         description="tools and scripts can be used to exploit the vulnerability "
                                     "i.e. metasploit, python scripts")
        bundle_elements.append(tool)

        vulnerability_cwe119 = stix.Vulnerability(
            name="CWE-119: Improper Restriction of Operations within the Bounds of a Memory Buffer",
            description="Certain languages allow direct addressing of memory "
                        "locations and do not automatically ensure that these "
                        "locations are valid for the memory buffer that is "
                        "being referenced. This can cause read or write "
                        "operations to be performed on memory locations that "
                        "may be associated with other variables, "
                        "data structures, or internal program data.  As a "
                        "result, an attacker may be able to execute arbitrary "
                        "code, alter the intended control flow, read sensitive "
                        "information, or cause the system to crash. ")
        bundle_elements.append(vulnerability_cwe119)

        vulnerability_cwe399 = stix.Vulnerability(name="CWE-399: Resource Management Errors (Category)",
                                                  description="Weaknesses in the category are related to improper "
                                                              "management of system resources.")
        bundle_elements.append(vulnerability_cwe399)

        grouping = stix.Grouping(context="vulnerabilities", object_refs=[vulnerability_cwe119, vulnerability_cwe399])
        bundle_elements.append(grouping)

        # creation of common relationship objects

        relationship_for_attack_pattern = stix.Relationship(relationship_type="uses",
                                                            source_ref=attack_pattern,
                                                            target_ref=tool)
        bundle_elements.append(relationship_for_attack_pattern)

        relationship_for_campaign1 = stix.Relationship(relationship_type="targets",
                                                       source_ref=campaign,
                                                       target_ref=vulnerability_cwe119)
        relationship_for_campaign2 = stix.Relationship(relationship_type="targets",
                                                       source_ref=campaign,
                                                       target_ref=vulnerability_cwe399)
        bundle_elements.append(relationship_for_campaign1)
        bundle_elements.append(relationship_for_campaign2)

        relationship_for_course_of_action1 = stix.Relationship(relationship_type="remediates",
                                                               source_ref=course_of_action,
                                                               target_ref=vulnerability_cwe119)
        relationship_for_course_of_action2 = stix.Relationship(relationship_type="remediates",
                                                               source_ref=course_of_action,
                                                               target_ref=vulnerability_cwe399)
        bundle_elements.append(relationship_for_course_of_action1)
        bundle_elements.append(relationship_for_course_of_action2)

        relationship_for_intrusion_set1 = stix.Relationship(relationship_type="targets",
                                                            source_ref=intrusion_set,
                                                            target_ref=vulnerability_cwe119)
        relationship_for_intrusion_set2 = stix.Relationship(relationship_type="targets",
                                                            source_ref=intrusion_set,
                                                            target_ref=vulnerability_cwe399)
        bundle_elements.append(relationship_for_intrusion_set1)
        bundle_elements.append(relationship_for_intrusion_set2)

        relationship_for_threat_actor1 = stix.Relationship(relationship_type="targets",
                                                           source_ref=threat_actor,
                                                           target_ref=vulnerability_cwe119)
        relationship_for_threat_actor2 = stix.Relationship(relationship_type="targets",
                                                           source_ref=threat_actor,
                                                           target_ref=vulnerability_cwe399)
        bundle_elements.append(relationship_for_threat_actor1)
        bundle_elements.append(relationship_for_threat_actor2)

        relationship_for_tool1 = stix.Relationship(relationship_type="targets",
                                                   source_ref=tool,
                                                   target_ref=vulnerability_cwe119)
        relationship_for_tool2 = stix.Relationship(relationship_type="targets",
                                                   source_ref=tool,
                                                   target_ref=vulnerability_cwe399)
        bundle_elements.append(relationship_for_tool1)
        bundle_elements.append(relationship_for_tool2)

        function_list = []
        for stix_dictionary in stix_dictionary_list:
            bundle_elements.extend(stix_dictionary["stix_objects"])
            function_list.extend(stix_dictionary["function_identifiers"])

            relationship_for_malware_analysis = stix.Relationship(relationship_type="characterizes",
                                                                  source_ref=malware_analysis,
                                                                  target_ref=stix_dictionary["malware"])
            bundle_elements.append(relationship_for_malware_analysis)

            relationship_for_group = stix.Relationship(relationship_type="contains",
                                                                  source_ref=stix_dictionary["malware"],
                                                                  target_ref=grouping)
            bundle_elements.append(relationship_for_group)

        opinion = stix.Opinion(authors=["cti-for-css"],
                               explanation="The code has CWE-119 and/or CWE-399. "
                                           "Immediately, a further analysis should be performed."
                                           "Before the analysis, the software/software component must not be used",
                               opinion="strongly-agree",
                               object_refs=function_list)
        bundle_elements.append(opinion)

        return bundle_elements
