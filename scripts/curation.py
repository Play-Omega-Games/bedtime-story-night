"""Child-safety curation for Bedtime Story Night.

Each entry: title -> (min_age, flags). min_age is 3, 6 or 9 (the youngest age band the story suits when read aloud by a parent).
Flags:
  peril        a character is in danger (lost, chased, trapped) but comes through
  scary        a frightening figure or scene (witch, wolf, ogre, dark woods)
  villain_dies the wrongdoer comes to a bad end, briefly told
  death        a non-villain dies, or death is described
  violence     cruelty or injury described on the page
  sad          a sad or bittersweet ending
  mature       grown-up themes (drinking, cruelty between spouses)
  dated        old-fashioned wording about people of other lands that many families today would skip
Story levels (the owner's choice):
  gentle   no flags at all
  classic  only peril, scary and villain_dies
  all      every story in the plan
EXCLUDED stories never enter the plan, whatever the setting.
"""

GRIMM = {
    "THE RABBIT'S BRIDE": (6, []),
    "SIX SOLDIERS OF FORTUNE": (6, ["peril"]),
    "CLEVER GRETHEL": (9, ["mature"]),
    "THE DEATH OF THE HEN": (6, ["death", "sad"]),
    "HANS IN LUCK": (3, []),
    "THE GOOSE GIRL": (9, ["violence", "death"]),
    "THE RAVEN": (9, ["peril", "scary"]),
    "THE FROG PRINCE": (3, []),
    "CAT AND MOUSE IN PARTNERSHIP": (6, ["death"]),
    "THE WOLF AND THE SEVEN LITTLE GOATS": (6, ["scary", "peril", "villain_dies"]),
    "FAITHFUL JOHN": (9, ["violence", "death"]),
    "THE WONDERFUL MUSICIAN": (6, ["peril"]),
    "THE TWELVE BROTHERS": (9, ["violence", "death"]),
    "THE VAGABONDS": (6, ["peril"]),
    "THE BROTHER AND SISTER": (9, ["violence", "death", "scary"]),
    "RAPUNZEL": (6, ["peril", "scary"]),
    "THE THREE LITTLE MEN IN THE WOOD": (9, ["violence", "villain_dies"]),
    "THE THREE SPINSTERS": (6, []),
    "HANSEL AND GRETHEL": (6, ["scary", "peril", "villain_dies"]),
    "THE WHITE SNAKE": (9, ["peril", "death"]),
    "THE STRAW, THE COAL, AND THE BEAN": (6, ["death"]),
    "THE FISHERMAN AND HIS WIFE": (3, []),
    "THE GALLANT TAILOR": (6, ["peril", "villain_dies"]),
    "ASCHENPUTTEL": (9, ["violence"]),
    "THE MOUSE, THE BIRD, AND THE SAUSAGE": (6, ["death"]),
    "MOTHER HULDA": (3, []),
    "LITTLE RED-CAP": (6, ["scary", "peril", "villain_dies"]),
    "THE BREMEN TOWN MUSICIANS": (3, []),
    "PRUDENT HANS": (9, ["violence"]),
    "CLEVER ELSE": (6, ["sad"]),
    "THE TABLE, THE ASS, AND THE STICK": (6, ["peril"]),
    "TOM THUMB": (6, ["peril"]),
    "HOW MRS. FOX MARRIED AGAIN": (6, []),
    "THE ELVES": (6, []),
    "MR. KORBES": (9, ["violence", "death"]),
    "TOM THUMB'S TRAVELS": (6, ["peril"]),
    "OLD SULTAN": (6, ["peril"]),
    "THE SIX SWANS": (9, ["violence", "scary", "villain_dies"]),
    "THE SLEEPING BEAUTY": (6, ["peril", "death"]),
    "KING THRUSHBEARD": (6, []),
    "SNOW-WHITE": (9, ["violence", "scary", "villain_dies"]),
    "THE KNAPSACK, THE HAT, AND THE HORN": (9, ["peril", "violence"]),
    "RUMPELSTILTSKIN": (6, ["scary", "violence", "villain_dies"]),
    "ROLAND": (9, ["violence", "death"]),
    "THE GOLDEN BIRD,": (9, ["violence", "peril"]),
    "THE DOG AND THE SPARROW": (9, ["violence", "death"]),
    "FRED AND KATE": (6, ["peril"]),
    "THE LITTLE FARMER": (9, ["violence", "death"]),
    "THE QUEEN BEE": (6, ["peril"]),
    "THE GOLDEN GOOSE": (3, []),
}

ANDERSEN = {
    "THE FIR TREE": (6, ["sad"]),
    "LITTLE TUK": (6, []),
    "THE UGLY DUCKLING": (3, ["peril"]),
    "LITTLE IDA'S FLOWERS": (3, []),
    "THE STEADFAST TIN SOLDIER": (6, ["sad"]),
    "LITTLE THUMBELINA": (3, ["peril"]),
    "SUNSHINE STORIES": (6, []),
    "THE DARNING-NEEDLE": (3, []),
    "THE LOVING PAIR": (6, []),
    "THE LEAPING MATCH": (3, []),
    "THE HAPPY FAMILY": (3, []),
    "THE GREENIES": (6, []),
    "THE MONEY BOX": (3, []),
    "ELDER-TREE MOTHER": (6, []),
    "THE ROSES AND THE SPARROWS": (6, ["death", "sad"]),
    "THE OLD HOUSE": (6, ["sad"]),
    "THE CONCEITED APPLE BRANCH": (6, []),
    "THE FLAX": (6, []),
    "THE DAISY": (6, ["death", "sad"]),
    "THE PEA BLOSSOM": (3, []),
    "THE STORKS": (6, ["death"]),
    "THE WILD SWANS": (9, ["peril", "scary"]),
    "THE LAST DREAM OF THE OLD OAK": (9, ["sad"]),
    "THE PORTUGUESE DUCK": (6, ["death", "sad"]),
    "THE SNOW MAN": (6, ["sad"]),
    "THE FARMYARD COCK AND THE WEATHERCOCK": (6, []),
    "THE LITTLE MERMAID": (9, ["death", "sad"]),
    "BUCKWHEAT": (6, []),
    "WHAT HAPPENED TO THE THISTLE": (6, []),
    "THE PEN AND THE INKSTAND": (9, []),
    "THE TEAPOT": (3, []),
    "SOUP FROM A SAUSAGE SKEWER": (9, []),
    "WHAT THE GOODMAN DOES IS ALWAYS RIGHT": (3, []),
    "THE OLD STREET LAMP": (6, ["dated"]),
    "THE SHEPHERDESS AND THE CHIMNEY SWEEP": (6, ["dated"]),
    "THE DROP OF WATER": (9, ["dated"]),
    "THE SWINEHERD": (6, []),
    "THE FLYING TRUNK": (6, []),
    "THE BUTTERFLY": (6, ["sad"]),
    "THE GOBLIN AND THE HUCKSTER": (6, []),
    "EVERYTHING IN ITS RIGHT PLACE": (9, []),
    "THE REAL PRINCESS": (3, []),
    "THE EMPEROR'S NEW CLOTHES": (6, []),
    "GREAT CLAUS AND LITTLE CLAUS": (9, ["violence", "death"]),
    "THE NIGHTINGALE": (6, ["scary", "peril", "dated"]),
}
# Series: parts are separate nights, read in order.
ANDERSEN_SERIES = {
    "OLE-LUK-OIE THE DREAM GOD": {
        "parts": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"],
        "tags": {"MONDAY": (3, []), "TUESDAY": (3, []), "WEDNESDAY": (3, []), "THURSDAY": (3, []),
                 "FRIDAY": (3, []), "SATURDAY": (3, ["dated"]), "SUNDAY": (6, ["death"])},
    },
    "THE SNOW QUEEN": {
        "parts": ["STORY THE FIRST", "SECOND STORY", "THIRD STORY", "FOURTH STORY", "FIFTH STORY", "SIXTH STORY", "SEVENTH STORY"],
        "tags": {p: (6, ["peril", "scary"]) for p in ["STORY THE FIRST", "SECOND STORY", "THIRD STORY", "FOURTH STORY", "FIFTH STORY", "SIXTH STORY", "SEVENTH STORY"]},
    },
}

KIPLING = {
    "HOW THE WHALE GOT HIS THROAT": (3, []),
    "HOW THE CAMEL GOT HIS HUMP": (3, []),
    "HOW THE RHINOCEROS GOT HIS SKIN": (3, []),
    "THE ELEPHANT’S CHILD": (3, ["peril"]),
    "THE SING-SONG OF OLD MAN KANGAROO": (3, ["peril"]),
    "THE BEGINNING OF THE ARMADILLOS": (3, []),
    "HOW THE FIRST LETTER WAS WRITTEN": (6, []),
    "HOW THE ALPHABET WAS MADE": (9, []),
    "THE CRAB THAT PLAYED WITH THE SEA": (6, []),
    "THE CAT THAT WALKED BY HIMSELF": (3, []),
    "THE BUTTERFLY THAT STAMPED": (6, []),
}

# Never in the plan, whatever the setting. Reasons are internal.
EXCLUDED = {
    ("grimm", "THE ROBBER BRIDEGROOM"): "murder and cannibalism",
    ("grimm", "THE ALMOND TREE"): "the Juniper Tree: a child is killed and cooked",
    ("andersen", "THE LITTLE MATCH GIRL"): "a child freezes to death",
    ("andersen", "THE RED SHOES"): "a child's feet are cut off",
    ("andersen", "THE METAL PIG"): "dated racial wording",
    ("kipling", "HOW THE LEOPARD GOT HIS SPOTS"): "a racial slur in the original text",
}

# Aesop fables are tagged by a keyword scan (see build.py), then these overrides apply.
AESOP_EXCLUDED = {
    'The Æthiop': 'a fable about scrubbing a servant to change his skin color',
    'The Bitch and Her Whelps': 'title word parents would not want to read aloud',
}
AESOP_OVERRIDES = {
    'The Man and His Two Sweethearts': ['mature'],
    'The Man and His Wife': ['mature'],
    'The Goat and the Goatherd': ['violence'],
    'The Brother and the Sister': ['mature'],
}

# Stories that open the plan, in order (well-loved and gentle), by (source, title).
OPENERS = [
    ("grimm", "THE BREMEN TOWN MUSICIANS"),
    ("andersen", "THE REAL PRINCESS"),
    ("kipling", "HOW THE CAMEL GOT HIS HUMP"),
    ("grimm", "THE GOLDEN GOOSE"),
    ("andersen", "THE UGLY DUCKLING"),
    ("kipling", "THE ELEPHANT’S CHILD"),
    ("grimm", "HANS IN LUCK"),
    ("andersen", "THE EMPEROR'S NEW CLOTHES"),
    ("kipling", "HOW THE WHALE GOT HIS THROAT"),
    ("grimm", "THE FROG PRINCE"),
    ("andersen", "LITTLE THUMBELINA"),
    ("grimm", "LITTLE RED-CAP"),
]

# Gentle stories whose text mentions a strong word in passing. Each was read in context on Nov 3, 2026.
REVIEWED_GENTLE = {
    "grimm-the-bremen-town-musicians": "old animals run away from masters; robbers are scared off, a comic scene",
    "kipling-how-the-camel-got-his-hump": "'bit' as in a little bit",
    "grimm-the-golden-goose": "'die of hunger' figure of speech; the old king's death in the last line",
    "grimm-hans-in-luck": "a knife-grinder; talk of beef",
    "kipling-how-the-whale-got-his-throat": "the whale's throat; a jack-knife",
    "grimm-the-frog-prince": "the frog in her throat; a heart beating",
    "grimm-the-rabbits-bride": "the rabbit knocks over a straw doll and thinks he hurt her",
    "kipling-how-the-rhinoceros-got-his-skin": "the rhino eats a cake; a knife for cutting it",
    "andersen-little-tuk": "a grave mentioned in a history lesson",
    "andersen-little-idas-flowers": "faded flowers are buried in the garden, tenderly",
    "andersen-sunshine-stories": "a heart beating; teeth",
    "kipling-the-beginning-of-the-armadillos": "a joke about drowning; 'bit'",
    "andersen-the-darning-needle": "the needle's eye breaks off",
    "andersen-the-loving-pair": "a whipping top (a toy)",
    "kipling-how-the-first-letter-was-written": "a misunderstanding about spears; nobody is hurt",
    "andersen-the-leaping-match": "'good blood' (good family)",
    "andersen-the-happy-family": "snails died out long ago",
    "kipling-how-the-alphabet-was-made": "a spear and a carp in a picture game",
    "andersen-the-greenies": "aphids describe their short lives",
    "andersen-ole-luk-oie-the-dream-god-4": "mice crowd a wedding",
    "andersen-ole-luk-oie-the-dream-god-5": "pictures hang on the wall",
    "kipling-the-crab-that-played-with-the-sea": "the tides; a crab worried about sharks",
    "andersen-the-money-box": "a toy whip; a buried coin",
    "andersen-elder-tree-mother": "an old couple remembers worrying at sea",
    "kipling-the-cat-that-walked-by-himself": "the cat will kill mice",
    "kipling-the-butterfly-that-stamped": "'slay me with mirth'; a joke",
    "grimm-the-three-spinsters": "a mother beating her lazy daughter, one line at the start",
    "andersen-the-conceited-apple-branch": "a knife cuts the branch",
    "andersen-the-flax": "flax is soaked, spun and made into paper",
    "grimm-the-fisherman-and-his-wife": "the sea turns dark; heart beating",
    "andersen-the-pea-blossom": "a sick girl gets well",
    "grimm-mother-hulda": "a pricked finger",
    "andersen-the-farmyard-cock-and-the-weathercock": "a cock eats a worm",
    "andersen-buckwheat": "buckwheat struck by lightning",
    "grimm-how-mrs-fox-married-again": "the fox pretends to be dead as a joke",
    "andersen-what-happened-to-the-thistle": "a donkey would eat the thistle",
    "grimm-the-elves": "years pass in elf land",
    "andersen-the-teapot": "a teapot buried in a garden as a flowerpot",
    "andersen-soup-from-a-sausage-skewer": "mouse travel tales",
    "grimm-king-thrushbeard": "a proud princess learns to work; sore hands",
    "andersen-the-swineherd": "a rose on a grave mentioned once",
    "andersen-the-flying-trunk": "a toy sword in a story",
    "andersen-the-goblin-and-the-huckster": "the music died away",
    "andersen-everything-in-its-right-place": "an old estate story",
}
