
# Manage strings for the project


# Auxiliary method

class Strings:

    @staticmethod
    def url_is_an_image(url_image):
        format_list = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif']
        return any(element in url_image for element in format_list)

    @staticmethod
    def check_max_length(cadena, max_length):
        try:
            if len(cadena) <= max_length:
                return True
            else:
                return False
        except:
            return False