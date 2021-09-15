from bs4 import BeautifulSoup


class BreakDownBook:
    def __init__(self, html_filepath):
        with open(html_filepath, "r") as html:
            self.soup = BeautifulSoup(html, features="html.parser")

        now = self.soup.find("body").findNext("div", attrs=dict(style="display:block; "
                                                                      "margin-top:1em; "
                                                                      "margin-bottom:1em; "
                                                                      "margin-left:2em; "
                                                                      "text-indent:-2em"))
        title = now.text.replace("\n", " ").replace("\t", " ")
        self.title = " ".join([l for l in title.split(" ") if l]).split(": ")[-1]
        now = now.findNext("div", attrs=dict(style="display:block; "
                                                   "margin-top:1em; "
                                                   "margin-bottom:1em; "
                                                   "margin-left:2em; "
                                                   "text-indent:-2em"))
        author = now.text.replace("\n", " ").replace('\t', " ")
        self.author = " ".join([l for l in author.split(" ") if l]).split(": ")[-1]

        now = now.findNext("table", attrs=dict(summary="", style=""))
        table = now.findNext("tbody")
        chapters = [" ".join(x for x in element.text.replace("\n", " ").replace("\t", " ").split(" ")
                             if x).split(". ")[-1]
                    for element in table.find_all("tr")]
        self.chapter_names = tuple(chapters)
        self.chapters = list()
        for chapter in self.chapter_names:
            now = now.findNext("div", class_="chapter")
            chapter = "\n".join([x.text.lower().replace("\n", " ").replace("\t", " ") for x in now.findAll("p")])
            chapter = " ".join(x for x in chapter.split(" ") if x).replace(" \n", "\n")
            self.chapters.append(chapter)
        self.chapters = tuple(self.chapters)

    @property
    def n_chapters(self):
        return len(self.chapter_names)

    @property
    def text(self):
        return "\n".join(self.chapters)

if __name__ == "__main__":
    b = BreakDownBook("../../app/data/103.html")
    print(len(b.text))
