import os
import re
import shutil

from bs4 import BeautifulSoup


class DocumentProcessor:
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
        Helper method to prepend original path to a given text.
        """
        return path + "\n" + text

    def add_enter_placeholder(self, soup: any) -> any:
        """
        Adds a placeholder for new line character after every paragraph tag. Each accordion (indicated by MCDropDown class) is separated.
        """
        paragraphs = soup.find_all("div", {"class": "MCDropDown"})
        for paragraph in paragraphs:
            paragraph.insert_before("!newline!")
        return soup

    def replace_tables_with_csv(self, soup: any) -> any:
        """
        Replaces HTML tables with CSV formatted text.
        """
        tables = soup.find_all("table")
        bs = BeautifulSoup()
        for table in tables:
            rows = table.find_all("tr")
            csv_data = ""
            canContainYesSymbol = [False] * len(rows[0].find_all(["th", "td"]))
            for row in rows:
                cells = row.find_all(["th", "td"])
                isYesSymbol = [
                    c.get_text(strip=True) == "a"
                    and c.find("span")
                    and c.span.has_attr("style")
                    and "Webdings" in c.span["style"]
                    for c in cells
                ]
                if any(isYesSymbol):
                    canContainYesSymbol = [c or y for c, y in zip(canContainYesSymbol, isYesSymbol)]
                csv_data += (
                    ",".join(
                        [
                            '"yes"'
                            if y
                            else ('"no"' if can else '"' + self.replace_quotation_marks(c.get_text(strip=True)) + '"')
                            for c, can, y in zip(cells, canContainYesSymbol, isYesSymbol)
                        ]
                    )
                    + "\n"
                )
            # Replace the table with paragraph containing the CSV data
            new_p = bs.new_tag("p")
            new_p.string = csv_data
            table.replace_with(new_p)
        return soup

    def replace_blank(self, soup: any) -> any:
        """
        Replaces non-breaking space with empty string.
        """
        paragraphs = soup.find_all("p", string="\xa0")
        for p in paragraphs:
            p.replace_with("")
        return soup

    def replace_images(self, soup: any) -> any:
        """
        Replaces images with their respective resources in Markdown format.
        """
        images = soup.find_all("img")
        for image in images:
            a = image.find_parents("a", limit=1)
            position = re.search(r"Resources|Skins", image["src"])
            if position == None:
                continue
            if len(a) == 1 and "transparent.gif" in image["src"]:  # If image is positioned in a link
                a[0].replace_with(a[0].get_text())
            elif len(a) == 1:
                a[0].replace_with("/static/" + image["src"][position.regs[0][0] :] + ".")
            else:
                image.replace_with("/static/" + image["src"][position.regs[0][0] :] + ".")
        return soup

    def replace_videos(self, soup: any) -> any:
        """
        Replaces video URLs with their respective resources.
        """
        videos = soup.find_all("video")
        for video in videos:
            # Check for the source element within the video tag
            source = video.find("source")
            if not source or "src" not in source.attrs:
                continue  # Skip if no <source> with src attribute is found

            # Find the position of specific keywords in the video src
            position = re.search(r"Resources|Media", source["src"])
            if position is None:
                continue  # Skip if src doesn't match the pattern

            # Replace the video src with the modified path
            modified_url = "/static/" + source["src"][position.regs[0][0] :] + "."
            source["src"] = modified_url  # Update the source's src attribute

            # Replace the video element itself with the updated one
            video.replace_with(str(video))

        return soup

    def replace_links(self, soup: any) -> any:
        """
        Replaces links with their respective text.
        """
        links = soup.find_all("a")
        for link in links:
            link.replace_with(link.get_text())
        return soup

    def remove_newline_before_images(self, text: str) -> str:
        """
        Removes newline characters before images.
        """
        text = re.sub(r"(|\.)( )*\n\/static\/", " /static/", text)
        return text

    def replace_quotation_marks(self, text: any) -> str:
        """
        Replaces quotation marks with their respective text.
        """
        text = re.sub('"', "'", text)
        return text

    def preprocessor(self, text):
        # Convert Markdown to HTML
        soup = BeautifulSoup(text, "html.parser")
        content = soup.findAll("div", {"id": "mc-main-content"})
        content = self.replace_tables_with_csv(content[0] if len(content) > 0 else soup)  # Replace tables with CSV
        content = self.replace_blank(content)  # Replace non-breaking space
        content = self.add_enter_placeholder(content)  # Add newline placeholder to insert new line character later
        content = self.replace_images(content)  # Replace images with their respective resources
        content = self.replace_videos(content)  # Replace videos with their respective resources

        content = self.replace_links(content)  # Replace links with their respective text or image url
        text = str(content)  # Convert soup to string
        text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
        text = re.sub(r"\n(\n| )+", "\n", text)  # Remove extra spaces
        text = re.sub(r"!newline!", "\n\n", text)  # Replace newline placeholder with new line character
        text = self.remove_newline_before_images(text)  # Remove newline characters before images
        text = text.strip()
        return text

    def find_files(self, directory: str = "../../resources/seaborn") -> None:
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

    def preprocess(self, from_directory, to_directory):
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

            processed_content = self.preprocessor(markdown_content)

            # Save the processed content to the destination directory
            to_path = str(to_directory) + file_path.split(str(from_directory))[1]
            directory_part = to_path.split(file_name)[0]
            # Check if directory exists, if not, create it
            if not os.path.exists(directory_part):
                os.makedirs(directory_part)
            to_path = os.path.join(directory_part, file_name)
            with open(to_path, "w", encoding="utf-8") as output_file:
                output_file.write(processed_content)

        return "successful"


# Preprocessor().preprocess('../../../data/external/optano', '../../../data/processed/preprocessed_data/')
