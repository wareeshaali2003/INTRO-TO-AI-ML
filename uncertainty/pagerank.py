import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
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
   
    num_pages = len(corpus)
     # list in which all pages are presented
    linked_pages = corpus[page]
    if len(linked_pages) == 0:
        uniform_probabilities = {}
        for page in corpus:
            uniform_probabilities[page] = 1 / num_pages
    return uniform_probabilities
    transition_model = {}
    for p in corpus:
        transition_model[p] = (1 - damping_factor) / num_pages
        if p in linked_pages:
            transition_model[p] += damping_factor / len(linked_pages)
    return transition_model


def sample_pagerank(corpus, damping_factor, n):
      # initialize dictionary to keep track of count of times each page is visited
    page_count = {}
    for page in corpus:
        page_count[page] = 0
    # choose a page at random to start
    current_page = random.choice(list(corpus.keys()))

    for i in range(n):
        # update count of current page
        page_count[current_page] += 1

        # calculate transition probabilities for current page
        prob_dist = transition_model(corpus, current_page, damping_factor)

        # choose the next page based on transition probabilities
        next_page = random.choices(list(prob_dist.keys()), weights=list(prob_dist.values()))[0]

        # set next page as current page for next iteration
        current_page = next_page
        pagerank = {}
        for page, count in page_count.items():
            pagerank[page] = count/n

    return pagerank

def iterate_pagerank(corpus, damping_factor):
    # initialize all pagerank values to 1/N
    n = len(corpus)
    pagerank = {page: 1/n for page in corpus}

    # perform iterations until convergence
    while True:
        new_pagerank = {}
        for page in corpus:
           incoming_pagerank = 0
           for other_page in corpus:
               if page in corpus[other_page]:
                   incoming_pagerank += pagerank[other_page] / len(corpus[other_page])
        new_pagerank[page] = (1 - damping_factor) / n + damping_factor * incoming_pagerank

        # check for convergence
        if all(abs(new_pagerank[page] - pagerank[page]) < 0.001 for page in corpus):
            return new_pagerank

        pagerank = new_pagerank


if __name__ == "__main__":
    main()
