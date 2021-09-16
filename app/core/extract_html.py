from bs4 import BeautifulSoup


class BreakDownBook:
    def __init__(self, html_filepath):
        with open(html_filepath, "r", encoding="utf-8") as html:
            self.soup = BeautifulSoup(html, features="html.parser")
        now = body = self.soup.find("body")
        while not now.text.startswith("Title"):
            now = now.findNext("div")
            if not now:
                break
        if now:
            self._extract_classic(now)
        else:
            self._extract_case_title_h(body)

    @property
    def n_chapters(self):
        return len(self.chapter_names)

    @property
    def text(self):
        return "\n".join(self.chapters)

    def _extract_classic(self, body):
        now = body
        del body

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

    def _extract_case_title_h(self, body):
        raise NotImplementedError("WIP")
        now = body
        del body
        now = now.findNext("h1")
        self.title = now.text
        print(self.title)
        author = now.findNext("h2")
        previous_author = None
        while author:
            print(previous_author, author)
            previous_author = author
            author = author.findNext("h2")

        self.author = self.clean_text(previous_author.text)
        print(self.author)
        text_concat = list()

        self.chapters = list()
        self.chapter_names = list()
        preface_title = now.findNext("h2")
        now = now.findNext("p")

        next_chapter = chapter = now.findNext("h2")
        if chapter != preface_title:
            self.chapter_names.append(self.clean_text(chapter.text))
        else:
            self.chapter_names.append("")
        text = self.clean_text(now.text)
        text_concat.append(text)
        i = 0
        while now:
            print(i, text, chapter, next_chapter)
            i += 1
            next_chapter = now.findNext("h2")
            if chapter != next_chapter:
                now = now.findNext("p")
                text = self.clean_text(now.text)
                text_concat.append(text)
            else:
                self.chapters.append("\n".join(text_concat))
                chapter = now.findNext("h2")
                self.chapter_names.append(self.clean_text(chapter.text))

        print(self.title, self.author, self.chapter_names, len(self.chapters), len(self.chapters_names))
        raise NotImplementedError

    @staticmethod
    def clean_text(text):
        text.replace("\n", " ").replace("\t", " ")
        text = " ".join([x for x in text.split(' ') if x])
        return text


if __name__ == "__main__":
    b = BreakDownBook("../../app/data/103.html")
    print(len(b.text))
