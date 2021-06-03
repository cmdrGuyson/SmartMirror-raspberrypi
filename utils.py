import itertools
import operator


class StringUtils:

    @staticmethod
    def format_response(list_input):
        # Format news articles to be displayed
        for element in list_input:
            element["description"] = element["description"].replace(
                "\n", " ").replace("\r", "")

            # Reduce charachter count to fit screen
            if len(element["description"]) > 200:
                element["description"] = element["description"][:195]+"..."

        return list_input

    @staticmethod
    def get_suffix(date):
        # Get suffix for date to be displayed
        day = date.day

        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return suffix

    @staticmethod
    def get_event_string(events):
        string = "\n"

        # Only allow 3 events to be displayed to suit spacial needs
        if len(events) > 3:
            events = events[:3]

        for event in events:
            string = f"{string}[b]{event['title']}[/b] at {event['time']}\n"

        # Remove final \n and return string
        return string[:-1]

    @staticmethod
    def string_mode(list_input):
        # Get sorted iterable
        sorted_list = sorted((x, i) for i, x in enumerate(list_input))

        groups = itertools.groupby(sorted_list, key=operator.itemgetter(0))

        # auxiliary function to get "quality" for an item
        def _auxfun(g):
            item, iterable = g
            count = 0
            min_index = len(list_input)
            for _, where in iterable:
                count += 1
                min_index = min(min_index, where)
            return count, -min_index

        # pick the highest-count/earliest item
        return max(groups, key=_auxfun)[0]
