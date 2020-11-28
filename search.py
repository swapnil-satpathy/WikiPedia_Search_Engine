from collections import defaultdict
import sys
import threading
import math
import re
import timeit

offset = []
stopwords=set(["a", "about", "above", "above", "across", "after", "afterwards", "again", "against",
 "all", "almost", "alone", "along", "already", "also","although","always","am","among",
  "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything",
  "anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", 
  "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond",
   "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de",
    "describe", "detail", "do", "done", "down","due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", 
    "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", 
    "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", 
    "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", 
    "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", 
    "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", 
    "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither",
     "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often",
    "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", 
    "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show",
    "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", 
    "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", 
    "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", 
    "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we",
     "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", 
     "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without",
      "would", "yet", "you", "your", "yours", "yourself", "yourselves"])

no_of_queries=0
titleOffset = []

def StopWords_removal(content):
    content_modified=[]
    for word in content:
        if word not in stopwords:
            content_modified.append(word)
    return content_modified


def tokenize(text):
    text=text.encode("ascii", errors="ignore").decode()
    # removing special characters
    text = re.sub(r'[^A-Za-z0-9]+', r' ', text)
    # removing urls
    text=re.sub(r'http[^\ ]*\ ', r' ', text) 
    # removing html entities
    text = re.sub(r'&nbsp;|&lt;|&gt;|&amp;|&quot;|&apos;', r' ', text) 
    text=text.split()
    return text

def find_File_Number(low, high, offset, word, fpoint, type_of='str'):
    #  Doing Binary Search to find the fileNo
    while low < high:
        mid = int(low + ((high-low)/2))
        fpoint.seek(offset[mid])
        word_pointer = fpoint.readline().strip().split()
        
        if type_of == 'int':
            if int(word) == int(word_pointer[0]):
                return word_pointer[1:], mid
            elif int(word) > int(word_pointer[0]):
                low = mid + 1
            else:
                high = mid
        else:
            if word == word_pointer[0]:
                return word_pointer[1:], mid
            elif word > word_pointer[0]:
                low = mid + 1
            else:
                high = mid
    return [], -1


def find_Documents(filename, file_No, field, token, fieldpointer):
    fieldOffset = []
    document_frequency=[]
    with open('./files/supu'+field + file_No + '.txt') as fil:
        for line in fil:
            offset, delf= line.strip().split()
            fieldOffset.append(int(offset))
            document_frequency.append(int(delf))
    document_List, mid = find_File_Number(0, len(fieldOffset), fieldOffset, token, fieldpointer)
    return document_List, document_frequency[mid]


def field_Query(tokens,vocab_file,fields):
    document_List = defaultdict(dict)
    document_freq = {}
    for i in range(len(tokens)):
        token = tokens[i]
        field=fields[i]
        docs, mid = find_File_Number(0, len(offset), offset, token, vocab_file)
        if len(docs):
            filename = './files/' + field+str(docs[0]) +'.txt'
            fieldpointer = open(filename, 'r')
            new_document_List, something= find_Documents(filename,docs[0], field, token, fieldpointer)
            document_List[token][field]=new_document_List
            document_freq[token] = something
    return document_List, document_freq


def simple_Query(tokens,vocab_file):
    document_list = defaultdict(dict)
    document_freq = {}
    fields = ['t', 'b', 'i', 'c', 'r', 'l']
    for token in tokens:
        documents,mid=find_File_Number(0, len(offset), offset, token, vocab_file)
        if len(documents):
            document_freq[token]=documents[1]
            for field in fields:
                filename = './files/' + field + str(documents[0]) + '.txt'
                fieldpointer= open(filename, 'r')
                returnedList, _ = find_Documents(filename, documents[0], field, token,fieldpointer)
                document_list[token][field] = returnedList
    return document_list,document_freq


def find_the_factor(field):
    switcher={
        't': 0.25,
        'b':0.25,
        'i': 0.20,
        'c': 0.1,
        'r': 0.05,
        'l': 0.05

    }
    return switcher.get(field,0.0)

def find_the_factor2(field):
    switcher={
        't': 0.25,
        'b':0.25,
        'i': 0.4,
        'c': 0.1,
        'r': 0.05,
        'l': 0.1

    }
    return switcher.get(field,0.0)
    

def rank(results, document_freq, no_of_files, query_type):
    Idf = {}  # Inverted Document Frequency
    documents= defaultdict(float)
    

    for key in document_freq:
        Idf[key] = math.log((float(no_of_files) - float(document_freq[key]) + 0.5) / ( float(document_freq[key]) + 0.5))
        document_freq[key] = math.log(float(no_of_files) / float(document_freq[key]))

    for word in results:
        posting= results[word]
        for field in posting:
            if len(field):
                postingList = posting[field]
                
                if query_type==0:
                    factor=find_the_factor(field)
                else:
                    factor=find_the_factor2(field)

                for i in range(0, len(postingList), 2):
                    documents[postingList[i]] += float( factor * (1+math.log(float(postingList[i+1]))) * document_freq[word])
    
    return documents





def search():
    with open('./files/offset.txt', 'r') as fil:
        for line in fil:
            offset.append(int(line.strip()))
    
    with open('./files/titleOffset.txt', 'r') as fil:
        for line in fil:
            titleOffset.append(int(line.strip()))

    
    title_File=open('./files/title.txt', 'r')
    vocab_file=open('./files/vocab.txt', 'r')

    
    
    fil=open('./files/fileNumbers.txt', 'r')
    no_of_files = int(fil.read().strip())
    fil.close()

    the_queries_file=sys.argv[1]

    fil=open(the_queries_file,'r')
    queries=fil.readlines()
    queries_result=open('queries_op.txt','a')

    global no_of_queries
    # Reading each query from the queries input file
    global_start=timeit.default_timer()
    for query in queries:
        start=timeit.default_timer()
        no_of_queries+=1
        query = query.lower()
        splitted=query.split(',')
        no_of_results=splitted[0].strip()
        query=splitted[1].strip()
        # Searching if the query is a field query....
        if re.match(r'[t|b|i|c|r|l]:', query):
            words=re.findall(r'[t|b|c|i|l|r]:([^:]*)(?!\S)', query)
            all_Fields=re.findall(r'([t|b|c|i|l|r]):', query)
            tokens=[]
            fields=[]

            for i in range(len(words)):
                for word in words[i].split():
                    fields.append(all_Fields[i])
                    tokens.append(word)

            tokens = StopWords_removal(tokens)
            results, document_freq=field_Query(tokens,vocab_file,fields) 
            #ranking all the results with the help of tfidf score and giving the results in decreasing order of importance
            results=rank(results, document_freq, no_of_files, 1) 
        else:
            tokens = tokenize(query)
            tokens = StopWords_removal(tokens)
            results, document_freq=simple_Query(tokens,vocab_file) # 0 means simple query
            results=rank(results, document_freq, no_of_files, 0)


        if len(results):
            results = sorted(results, key=results.get, reverse=True)
            try:
                results = results[:int(no_of_results)]
            except:
                results=results[:10]
            for key in results:
                title, _ = find_File_Number(0, len(titleOffset), titleOffset, key, title_File, 'int')
                queries_result.write(' '.join(title))
                queries_result.write('\n')
        else:
            queries_result.write('Sorry Unable to find the Query \n')
        end= timeit.default_timer()
        queries_result.write(str(end-start))
        queries_result.write('\n\n')

    global_end=timeit.default_timer()
    avg_timing=(global_end-global_start)/no_of_queries
    queries_result.write("The average time taken for all the queries is \n")
    queries_result.write(str(avg_timing))
    queries_result.write('\n\n')



if __name__ == '__main__':
    search()

    