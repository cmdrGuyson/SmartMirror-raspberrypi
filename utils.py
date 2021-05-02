class StringUtils:

    @staticmethod
    def format_response(list_input):
        for element in list_input:
            element["description"] = element["description"].replace("\n", "")

        return list_input

    @staticmethod
    def get_suffix(date):
        day = date.day

        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return suffix
