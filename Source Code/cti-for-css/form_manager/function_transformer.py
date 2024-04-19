# noinspection PyMethodMayBeStatic
class FunctionTransformer:
    __RETDEC_TEXT_SECTION_HEADER = "; section: .text"
    __RETDEC_TEXT_SECTION_END_HEADER = ";; Data Segment"

    def prepare_functions_from_dsm_file(self, dsm_file_content):
        text_section = dsm_file_content[
                       dsm_file_content.rfind(self.__RETDEC_TEXT_SECTION_HEADER):dsm_file_content.rfind(
                           self.__RETDEC_TEXT_SECTION_END_HEADER)]
        text_section_line_by_line = text_section.split("\n")

        functions = {}
        current_saving_status = False
        current_function = ""
        for line in text_section_line_by_line:
            if "section" in line or "data inside" in line:
                current_saving_status = False
                continue
            elif "; function" in line:
                current_saving_status = True
                current_function = line.replace("; function: ", "")
                continue

            if not current_saving_status:
                continue

            prepared_function_line = self.__prepare_line(line)

            if current_function in functions:
                functions[current_function].append(prepared_function_line)
            else:
                functions[current_function] = [prepared_function_line]

        return functions

    def __prepare_line(self, line):
        prepared_function_line = ""
        for code in line.split(" "):
            if "x" in code:
                continue

            if len(code) == 0:
                continue

            if "\t" in code:
                break

            try:
                # convert hexadecimal to decimal with int function
                transformed_code = str(int(code, 16))

                if len(prepared_function_line) != 0:
                    if prepared_function_line[-1] == "|":
                        prepared_function_line = prepared_function_line + transformed_code
                    else:
                        prepared_function_line = prepared_function_line + "," + transformed_code
                else:
                    prepared_function_line = transformed_code + "|"
            except:
                continue

        if len(prepared_function_line) > 0 and prepared_function_line[-1] == "|":
            prepared_function_line = prepared_function_line + prepared_function_line[:-1]
        return prepared_function_line

    def prepare_functions_from_string(self, functions_dataset_raw: str) -> list[str]:
        return [function_data for function_data in functions_dataset_raw.replace("\n", " ").split(" ----- ")
                if self.__check_inclusion_of_function_data(function_data)]

    def __check_inclusion_of_function_data(self, function_data: str) -> bool:
        if function_data == "":
            return False
        return True

    def prepare_labels_from_string(self, labels_dataset_raw: str) -> list[str]:
        return labels_dataset_raw.split()
