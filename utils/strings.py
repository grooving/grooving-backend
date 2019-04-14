
# Manage strings for the project


# Auxiliary method

class Strings:

    @staticmethod
    def url_is_an_image(url_image):
        format_list = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif']
        return any(element in url_image for element in format_list)
