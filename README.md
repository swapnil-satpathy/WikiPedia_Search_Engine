We will be using SAX Parser to parse the XML data

# indexer.py

    Running Format --> python3 indexer.py

    -> All the XML data you need to parse has to be inside a folder named Folder.
    -> Feed the files into XML parser and then text preprocessing is done:

    1. Tokenization
    2. Stop Words Removal
    3. Stemming (Stemming Steps have been commented in the code)
    and after preprocessing, Links,Body,Info,Categories,References,Title are extracted using the appropriate regex expressions.
    
    -> All the files created as a result of running the indexer.py code will be inside the files folder.
    
    -> Files Produced:

        title.txt : It consist of id-title mapping.
        titleOffset.txt : Offset for title.txt
        vocab.txt : It has all the words and the file number in which those words can be found along with the document frequency.
        offset.txt : Offset for vocab.txt
        supu.txt : Offset for various field files.
        inverted_index(file_Number).txt : These are the temporary inverted_indexes files that will be created for every input file
   

One can learn more about the regular expressions used in the code from the below youtube link:
https://www.youtube.com/watch?v=K8L6KVGG-7o
