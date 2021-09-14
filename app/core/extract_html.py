from bs4 import BeautifulSoup


class BreakDownBook:
    def __init__(self, html_filepath):
        with open(html_filepath, "r") as html:
            self.soup = BeautifulSoup(html, features="html.parser").find("body")

        now = self.soup.findNext("div", attrs=dict(style="display:block; "
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
        self.chapters = tuple(chapters)

    @property
    def n_chapters(self):
        return len(self.chapters)


if __name__ == "__main__":
    b = BreakDownBook("../../app/data/103.html")
    print(b.chapters)
