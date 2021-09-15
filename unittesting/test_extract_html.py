import os
import unittest

from app.core.extract_html import *

DATAPATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "data")


class TestBreakDownBook(unittest.TestCase):
    def test_init(self):
        b = BreakDownBook(os.path.join(DATAPATH, "103.html"))
        self.assertEqual("Around the World in Eighty Days", b.title)
        self.assertEqual("Jules Verne", b.author)
        chapters = (
            "IN WHICH PHILEAS FOGG AND PASSEPARTOUT ACCEPT EACH OTHER, THE ONE AS MASTER, THE OTHER AS MAN",
            "IN WHICH PASSEPARTOUT IS CONVINCED THAT HE HAS AT LAST FOUND HIS IDEAL",
            "IN WHICH A CONVERSATION TAKES PLACE WHICH SEEMS LIKELY TO COST PHILEAS FOGG DEAR",
            "IN WHICH PHILEAS FOGG ASTOUNDS PASSEPARTOUT, HIS SERVANT",
            "IN WHICH A NEW SPECIES OF FUNDS, UNKNOWN TO THE MONEYED MEN, APPEARS ON ’CHANGE",
            "IN WHICH FIX, THE DETECTIVE, BETRAYS A VERY NATURAL IMPATIENCE",
            "WHICH ONCE MORE DEMONSTRATES THE USELESSNESS OF PASSPORTS AS AIDS TO DETECTIVES",
            "IN WHICH PASSEPARTOUT TALKS RATHER MORE, PERHAPS, THAN IS PRUDENT",
            "IN WHICH THE RED SEA AND THE INDIAN OCEAN PROVE PROPITIOUS TO THE DESIGNS OF PHILEAS FOGG",
            "IN WHICH PASSEPARTOUT IS ONLY TOO GLAD TO GET OFF WITH THE LOSS OF HIS SHOES",
            "IN WHICH PHILEAS FOGG SECURES A CURIOUS MEANS OF CONVEYANCE AT A FABULOUS PRICE",
            "IN WHICH PHILEAS FOGG AND HIS COMPANIONS VENTURE ACROSS THE INDIAN FORESTS, AND WHAT ENSUED",
            "IN WHICH PASSEPARTOUT RECEIVES A NEW PROOF THAT FORTUNE FAVORS THE BRAVE",
            "IN WHICH PHILEAS FOGG DESCENDS THE WHOLE LENGTH OF THE BEAUTIFUL VALLEY OF THE GANGES WITHOUT EVER THINKING OF SEEING IT",
            "IN WHICH THE BAG OF BANKNOTES DISGORGES SOME THOUSANDS OF POUNDS MORE",
            "IN WHICH FIX DOES NOT SEEM TO UNDERSTAND IN THE LEAST WHAT IS SAID TO HIM",
            "SHOWING WHAT HAPPENED ON THE VOYAGE FROM SINGAPORE TO HONG KONG",
            "IN WHICH PHILEAS FOGG, PASSEPARTOUT, AND FIX GO EACH ABOUT HIS BUSINESS",
            "IN WHICH PASSEPARTOUT TAKES A TOO GREAT INTEREST IN HIS MASTER, AND WHAT COMES OF IT",
            "IN WHICH FIX COMES FACE TO FACE WITH PHILEAS FOGG",
            "IN WHICH THE MASTER OF THE “TANKADERE” RUNS GREAT RISK OF LOSING A REWARD OF TWO HUNDRED POUNDS",
            "IN WHICH PASSEPARTOUT FINDS OUT THAT, EVEN AT THE ANTIPODES, IT IS CONVENIENT TO HAVE SOME MONEY IN ONE’S POCKET",
            "IN WHICH PASSEPARTOUT’S NOSE BECOMES OUTRAGEOUSLY LONG",
            "FOGG AND PARTY CROSS THE PACIFIC OCEAN",
            "IN WHICH A SLIGHT GLIMPSE IS HAD OF SAN FRANCISCO",
            "IN WHICH PHILEAS FOGG AND PARTY TRAVEL BY THE PACIFIC RAILROAD",
            "IN WHICH PASSEPARTOUT UNDERGOES, AT A SPEED OF TWENTY MILES AN HOUR, A COURSE OF MORMON HISTORY",
            "IN WHICH PASSEPARTOUT DOES NOT SUCCEED IN MAKING ANYBODY LISTEN TO REASON",
            "IN WHICH CERTAIN INCIDENTS ARE NARRATED WHICH ARE ONLY TO BE MET WITH ON AMERICAN RAILROADS",
            "IN WHICH PHILEAS FOGG SIMPLY DOES HIS DUTY",
            "IN WHICH FIX, THE DETECTIVE, CONSIDERABLY FURTHERS THE INTERESTS OF PHILEAS FOGG",
            "IN WHICH PHILEAS FOGG ENGAGES IN A DIRECT STRUGGLE WITH BAD FORTUNE",
            "IN WHICH PHILEAS FOGG SHOWS HIMSELF EQUAL TO THE OCCASION",
            "IN WHICH PHILEAS FOGG AT LAST REACHES LONDON",
            "IN WHICH PHILEAS FOGG DOES NOT HAVE TO REPEAT HIS ORDERS TO PASSEPARTOUT TWICE",
            "IN WHICH PHILEAS FOGG’S NAME IS ONCE MORE AT A PREMIUM ON ’CHANGE",
            "IN WHICH IT IS SHOWN THAT PHILEAS FOGG GAINED NOTHING BY HIS TOUR AROUND THE WORLD, UNLESS IT WERE HAPPINESS",
        )
        self.assertEqual(chapters, b.chapter_names)
        self.assertEqual(len(chapters), b.n_chapters)
        self.assertTrue(
            b.chapters[5].startswith(
                "the circumstances under which this telegraphic dispatch about "
                "phileas fogg was sent were as follows:\n the steamer “mongolia,” "
                "belonging to the peninsular and oriental company, built of iron, of "
                "two thousand eight hundred tons burden, and five hundred"
            )
        )
        self.assertTrue(
            b.chapters[5].endswith(
                " the consulate?”\n “there, on the corner of the square,” said fix, "
                "pointing to a house two hundred steps off.\n “i’ll go and fetch my "
                "master, who won’t be much pleased, however, to be disturbed.”\n the "
                "passenger bowed to fix, and returned to the steamer."
            )
        )

        self.assertEqual(362194, len(b.text))
        if __name__ == "__main__":
            unittest.main()
