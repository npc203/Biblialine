# Tasks Done
1. Analysed words that occur exactly once in the bible, ~4k words, astonishingly common words (see one_words_in_bible.txt)
2. Finding most common words, generally and selectively (in certain books)
3. Pick a group of words and find spread both book and chapterwise


# TODO
1. find 90% above similar verses eg: 2 Chronicles 1:16 and 1 Kings 10:28
2. Html server for the app
3. Better fuzzy searches on words
4. Better corpus (include the use of ' and " but ignore those messy punctuations)

# Inferences?
1. Top 6 most common words (look into the ipynb notebook):
   1. Lord
   2. God
   3. Said
   4. King
   5. One
   6. Son
2. 1 Chronicles (probably) has the most number of unique words (421 words)
3. On average, 1 in every 4 (intresting) words occur exactly once in the bible (occur once ~4k words, total words ~16k words)


# Dumps
Most Common words in the bible (50):
[('lord', 7788), ('god', 4160), ('said', 3184), ('king', 2503), ('one', 2478), ('son', 2338), ('people', 2214), ('man', 2209), ('israel', 1858), ('men', 1805), ('like', 1528), ('land', 1451), ('come', 1435), ('us', 1422), ('day', 1419), ('go', 1392), ('jesus', 1274), ('went', 1231), ('father', 1220), ('may', 1219), ('came', 1191), ('made', 1109), ('let', 1071), ('put', 1018), ('david', 1007), ('house', 965), ('say', 916), ('give', 896), ('sons', 865), ('make', 852), ('know', 850), ('take', 847), ('moses', 843), ('hand', 840), ('judah', 834), ('among', 811), ('also', 809), ('see', 804), ('jerusalem', 799), ('away', 797), ('place', 792), ('must', 785), ('time', 768), ('brought', 763), ('name', 762), ('earth', 734), ('says', 727), ('bring', 723), ('city', 710), ('great', 698)]

Amount of single words in the bible with respect to books:
[('1 Chronicles', 421), ('Isaiah', 326), ('Genesis', 258), ('Acts', 237), ('Psalms', 229), ('Joshua', 228), ('Job', 228), ('Numbers', 226), ('Ezekiel', 225), ('Jeremiah', 219), ('Proverbs', 183), ('1 Kings', 148), ('Nehemiah', 147), ('Deuteronomy', 134), ('Exodus', 125), ('2 Samuel', 125), ('1 Samuel', 124), ('Leviticus', 122), ('Luke', 119), ('2 Chronicles', 113), ('2 Kings', 107), ('Ezra', 102), ('Judges', 101), ('Romans', 83), ('Daniel', 75), ('Esther', 67), ('1 Corinthians', 66), ('2 Corinthians', 65), ('Ecclesiastes', 61), ('Revelation', 56), ('Matthew', 53), ('John', 53), ('Hebrews', 49), ('Song of Solomon', 46), ('Mark', 44), ('Amos', 40), ('Hosea', 38), ('2 Timothy', 36), ('Zechariah', 32), ('Ephesians', 32), ('1 Timothy', 31), ('Colossians', 27), ('James', 25), ('Galatians', 23), ('Philippians', 22), ('Ruth', 21), ('Micah', 21), ('2 Peter', 21), ('Habakkuk', 19), ('Lamentations', 18), ('Nahum', 16), ('Titus', 15), ('Joel', 13), ('Malachi', 12), ('1 Peter', 12), ('1 Thessalonians', 10), ('Jonah', 9), ('Zephaniah', 9), ('Jude', 9), ('Haggai', 5), ('2 Thessalonians', 4), ('Philemon', 4), ('1 John', 4), ('Obadiah', 2), ('3 John', 2), ('2 John', 1)]

Number of (intresting) words per book: (removing those stop words)
[('Psalms', 17900), ('Jeremiah', 16633), ('Genesis', 15744), ('Ezekiel', 15383), ('Isaiah', 15067), ('Numbers', 13152), ('Exodus', 12861), ('2 Chronicles', 10981), ('Deuteronomy', 10594), ('Luke', 10333), ('Acts', 10293), ('1 Kings', 10099), ('1 Samuel', 9954), ('2 Kings', 9770), ('Matthew', 9728), ('Leviticus', 9654), ('1 Chronicles', 9217), ('2 Samuel', 8681), ('John', 7610), ('Job', 7420), ('Joshua', 7391), ('Judges', 7376), ('Proverbs', 6751), ('Mark', 6176), ('Revelation', 5024), ('Daniel', 4688), ('Nehemiah', 4423), ('Romans', 4076), ('1 Corinthians', 3858), ('Hebrews', 3074), ('Ezra', 2996), ('2 Corinthians', 2463), ('Zechariah', 2401), ('Esther', 2382), ('Ecclesiastes', 2226), ('Hosea', 2115), ('Amos', 1741), ('Lamentations', 1431), ('Galatians', 1346), ('Ephesians', 1336), ('Micah', 1249), ('Song of Solomon', 1178), ('1 Timothy', 1107), ('1 Peter', 1064), ('James', 1031), ('Ruth', 1021), ('1 John', 1004), ('Philippians', 920), ('Colossians', 873), ('Joel', 857), ('1 Thessalonians', 791), ('2 Timothy', 771), ('Malachi', 713), ('2 Peter', 704), ('Zephaniah', 653), ('Habakkuk', 603), ('Nahum', 542), ('Jonah', 525), ('Haggai', 491), ('Titus', 457), ('2 Thessalonians', 439), ('Jude', 300), ('Obadiah', 241), ('Philemon', 188), ('3 John', 134), ('2 John', 120)]