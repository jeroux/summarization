from bs4 import BeautifulSoup


class BreakDownBook:
    def __init__(self, html_filepath):
        with open(html_filepath, "r", encoding="utf-8") as html:
            self.soup = BeautifulSoup(html, features="html.parser")
        now = self.soup.find("body").findNext()

        while not now.text.startswith("Title"):
            now = now.findNext("div")

        title = now.text.replace("\n", " ").replace("\t", " ")
        self.title = " ".join([l for l in title.split(" ") if l]).split(": ")[-1]

        while not now.text.startswith("Author"):
            now = now.findNext("div")
        author = now.text.replace("\n", " ").replace("\t", " ")
        self.author = " ".join([l for l in author.split(" ") if l]).split(": ")[-1]

        self.chapter_names = list()
        self.chapters = list()
        now = now.findNext("div", class_="chapter")
        while now:
            chapter_name = now.find("h2").text.replace("\n", " ").replace("\t", " ")
            chapter_name = " ".join([x for x in chapter_name.split(" ") if x])
            self.chapter_names.append(chapter_name)
            chapter = "\n".join(
                [
                    x.text.lower().replace("\n", " ").replace("\t", " ")
                    for x in now.findAll("p")
                ]
            )
            chapter = " ".join(x for x in chapter.split(" ") if x).replace(" \n", "\n")
            self.chapters.append(chapter)

            now = now.findNext("div", class_="chapter")
        self.chapters = tuple(self.chapters)
        self.chapter_names = tuple(self.chapter_names)

    @property
    def n_chapters(self):
        return len(self.chapter_names)

    @property
    def text(self):
        return "\n".join(self.chapters)


if __name__ == "__main__":
    b = BreakDownBook("../../app/data/103.html")
    print(len(b.text))
