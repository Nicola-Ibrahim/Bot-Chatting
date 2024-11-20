import os
import re
import shutil

import markdown2
import marko


class Preprocessor:
    def __init__(self):
        # Dictionary to store file paths and their respective names
        self.file_names = {}

    def _remove_html_tags(self, text: str) -> str:
        """
        Helper method to remove HTML tags from a given text.
        """
        return re.sub(r"<.*?>", "", text)

    def _add_path(self, text: str, path) -> str:
        """
        Helper method to prepend orignial path to a given text.
        """
        return path + "\n" + text

    def preprocessor1(self, markdown_text: str, path: str) -> str:
        """
        Converts markdown text to HTML using 'marko', then removes HTML tags
        to return plain text.
        """
        html_content = marko.convert(markdown_text)
        plain_text = self._remove_html_tags(html_content)
        plain_text = re.sub(r'^\s*$', '', plain_text, flags=re.MULTILINE)
        return plain_text

    def preprocessor2(self, markdown_text):
        # Convert Markdown to HTML
        plain_text_with_html = markdown2.markdown(markdown_text)
        img_pattern = r'<img\s+[^>]*src="([^"]+)"(?:[^>]*alt="([^"]*)")?[^>]*>'

        def replace_img_tag(match):
            img_src = match.group(1)
            img_alt = match.group(2) if match.group(2) else "No alt attribute"
            if "Resources" in img_src:
                # Find the position of "resources"
                position = img_src.find("Resources")
                if position != -1:
                    img_src = "/static/" + img_src[position:]
            elif "Skins" in img_src:
                position = img_src.find("Skins")
                if position != -1:
                    img_src = "/static/" + img_src[position:]
            return f"{img_src}"

        processed_text = re.sub(img_pattern, replace_img_tag, plain_text_with_html)
        plain_text = re.sub(r"<.*?>", "", processed_text)
        no_blank_lines = re.sub(r" +\n", "", plain_text)
        no_leading_spaces = re.sub(r"  +", "", no_blank_lines)
        no_next_line_images = re.sub(r"\.*\n\/static\/", " /static/", no_leading_spaces)
        return no_next_line_images

    def find_files(self, directory: str = '../../resources/seaborn') -> None:
        """
        Recursively finds all files in a given directory and stores their
        full paths and file names in a dictionary.
        """
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            # If it's a file, store its path and file name
            if os.path.isfile(full_path):
                self.file_names[full_path] = os.path.basename(full_path)
            # If it's a directory, recurse into it
            elif os.path.isdir(full_path):
                self.find_files(full_path)

    def preprocess(self, from_directory, to_directory, method=2):
        if not os.path.exists(to_directory):
            os.makedirs(to_directory)

        # Clear the output directory if it contains any files
        for file_name in os.listdir(to_directory):
            file_path = os.path.join(to_directory, file_name)
            # Check if path is a file or a directory
            if os.path.isfile(file_path):
                os.remove(file_path)  # Deletes a file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Recursively deletes a directory

        # Populate file_names with markdown files from the source directory
        self.find_files(from_directory)

        # Process each file
        for file_path, file_name in self.file_names.items():
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    markdown_content = file.read()
                except:
                    pass

            # Choose the appropriate preprocessor method
            if method == 1:
                processed_content = self.preprocessor2(markdown_content)
            elif method == 2:
                processed_content = self.preprocessor2(markdown_content)
            else:
                return "Error: Incorrect method input! Choose 1 or 2."

            # Save the processed content to the destination directory
            to_path = str(to_directory) + file_path.split(str(from_directory))[1]
            directory_part = to_path.split(file_name)[0]
            # Check if directory exists, if not, create it
            if not os.path.exists(directory_part):
                os.makedirs(directory_part)
            to_path = os.path.join(directory_part, file_name)
            with open(to_path, 'w', encoding="utf-8") as output_file:
                output_file.write(processed_content)

        return 'successful'
