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
   

One can learn more about the regular expressions used in the code from the below youtube link:
https://www.youtube.com/watch?v=K8L6KVGG-7o
