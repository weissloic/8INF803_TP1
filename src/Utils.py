class Utils:
    def check_upper_name(self, string):
        last_char = string[-1]
        if last_char.isupper():
            string = string[:-1]
            return Utils.check_upper_name(self, string)

        return string
