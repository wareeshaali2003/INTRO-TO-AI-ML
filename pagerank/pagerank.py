import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 500


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
   

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    n=len(corpus)
    model = dict()
    for i in corpus:
        if len(corpus[page])==0:
            model[i]=1/n
        elif i == page and len(corpus[i])!=0:
            model[i]=(1-0.85)/n

        elif i!=page and i in corpus[page]:
            model[i]=(0.85/len(corpus[page]))+((1-0.85)/n)

        elif i!=page and i not in corpus[page]:
            model[i]=(1-0.85)/n
    return model



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    Page_Rank={}
    for key in corpus:
        Page_Rank[key]=int(0)
    
    current_page=random.choice(list(corpus.keys()))
    for i in range(n):
        Page_Rank[current_page]=Page_Rank[current_page]+1
        model=transition_model(corpus,current_page,damping_factor)
        current_page=random.choice(list(model.keys()))
    
    return {page:rank/n for page,rank in Page_Rank.items()}




if __name__ == "__main__":
    main()