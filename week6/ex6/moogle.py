import copy
import urllib.parse
import pickle
import bs4
import requests
import sys



def get_relatives(relative_file):
   #get a list of indexes from a file
    with open(relative_file,'r') as f:
        lines = f.readlines()
    relative_list = []
    for i in range(len(lines)):
            relative_list.append(lines[i].strip())
    return relative_list
def create_new_dict(list):
    #create an empty nested dictionary from a list
    dict = {}
    for i in range(len(list)):
        dict[list[i]] = {}
    return dict

def crawl(base_url, relative_url, dict_file): #sort the links according to their appearence in the other pages
    list = get_relatives(relative_url) #establish an empty list
    dict = create_new_dict(list) #establish an empty dictionary
    for relative in dict: #run over the pages according to their keys in the dictionary
        full_url = urllib.parse.urljoin(base_url, relative)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for p in soup.find_all("p"): #run over every paragrafh
            for link in p.find_all("a"): #run over every link
                target = link.get("href")
                if target == '':
                    pass
                elif target in dict[relative]:
                    dict[relative][target] += 1 #if the key is already in the dictionary, update to +=1
                else:
                    dict[relative][target] = 1 #if the key isn't in the dictionary, establish it and give the value 1
    with open(dict_file,'wb') as f: #save the file as pickle
        pickle.dump(dict,f)


def create_r(list):
    #create dictionary from a list with values of 1
    r = create_new_dict(list)
    for name in r:
        r[name] = 1
    return r


def create_new_r(list):
    #create dictionary from a list with values of 0
    new_r = create_new_dict(list)
    for name in new_r:
        new_r[name] = 0
    return new_r


def update_r(r, new_r):
    #update the old dictionary to become the new dictionary
    for key in r:
        r[key] = new_r[key]
    return r


def check_query_in_words(query,dict_word):#if a word is out all the keys. it removes it.
    query_list = list(query.split(" "))
    new_query_list = []
    # for key in dict_word.keys(): #run for every word in a dictionary
    for i in range(len(query_list)):
        if query_list[i] in dict_word.keys(): #check if a word in the query is a key in the dictionary
            if query_list[i] in new_query_list:
                continue
            else:
                new_query_list.append(query_list[i]) #if it is, it adds the value to a new list
    return new_query_list




def page_rank(iterations, out_file, ranking_file):  #creates a file that rank the links according to second step
    with open(out_file, 'rb') as f: #open the rated links from step 1
        soup = pickle.load(f)
    lst = list(soup.keys())
    r = {key:1 for key in lst}
    for i in range(iterations): #run for i iterations
        new_r = {key:0 for key in lst}
        for key,dict_of_links in soup.items(): #  # establish new dictionary
            for link, rank in dict_of_links.items():
                 new_r[link] += r[key] * (rank / (sum(dict_of_links.values()))) #calculates the link value
        r = new_r
    with open(ranking_file, 'wb') as f: #save as ranking file
        pickle.dump(r,f)

def words_dict(base_url, index_file, rank_word):
    #finds how many times every word accurs at any link
    #establishing a dictionary with keys as the words and every key-word has the index link names as keys
    #the value for the index keys would be the number of occurens
    res_dict = {}
    with open(index_file, 'rb') as f:
        index_dict = create_new_dict(get_relatives(index_file))
    for pages in index_dict.keys():# run on the pages
        full_url = urllib.parse.urljoin(base_url, pages)
        response = requests.get(full_url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for paragrafh in soup.find_all("p"):#run on paragrafhs in the index file
            content = paragrafh.text
            lst_words = content.split()
            for i in range(len(lst_words)):#run on every word in te paragrafh
                word = copy.deepcopy(lst_words[i])
                if word in res_dict.keys():
                    if pages not in res_dict[word].keys():
                        res_dict[word][pages] = 1 #add the index file as a key in the word dictionary
                    else:
                        res_dict[word][pages] += 1 #update the index file value
                else:
                    res_dict[word] = dict()
                    res_dict[word][pages] = 1
    with open(rank_word, 'wb') as f:
        pickle.dump(res_dict,f)


def check_if_string_in_link(str, dict):#check if a string is a key of a dictionary
        if str not in dict:
            return False
        return True


def create_valids_list(str, dict): #create a valid list with only the names which has all thw words in them
    query_list = check_query_in_words(str, dict)
    valid_lst = list(dict[query_list[0]].keys())
    return valid_lst


def update_dictionary_keys(dict1, dict2): #update keys in a dictionary from another dictionary
    new_dict = {}
    for key in dict1.keys():
        if key in dict2.keys():
           new_dict[key] = dict2[key]
    return new_dict


def max_results(lst1,lst2,max_results): #cut the list lenght according to max result given
    if len(lst1) > max_results:
        lst1 = lst1[:max_results]
        lst2 = lst2[:max_results]
    return (lst1 ,lst2)


def valid_dict(ranking_dict,lst): #establishing a valid dict from the valid list were given
    valid_dict = create_new_dict(lst)
    file = ranking_dict
    filtered_dict = update_dictionary_keys(valid_dict,file )
    return filtered_dict


def sort_dict(weighted_dict,max_results): #sort a dictionary values to be from heighest to lowest
    sorted_dict = dict(sorted(weighted_dict.items(), key=lambda item: item[1],reverse=True))
    keys = list(sorted_dict.keys())
    values = list(sorted_dict.values())
    if len(keys) > max_results:
        keys = keys[:max_results]
    if len(values) > max_results:
        values = values[:max_results]
    new_dict = {}
    for i in range(len(keys)):
        new_dict[keys[i]] = values[i]
    return new_dict

def weighted_values(rank_word_file, dict,query): #calacuate the value of a key from thw valid dictionary according to google formula
    query_list = check_query_in_words(query,rank_word_file)
    for word in range(len(query_list)):
        for key in dict.keys():
            dict[key] = dict[key] * rank_word_file[query_list[word]][key]
    return dict

def print_vertically(dict):
    for key,value in dict.items():
        print(key, ' : ', value)



def search(query,ranking_file,rank_word,max_results):
    with open(ranking_file, 'rb') as f:#load ranking file
        ranking_dict = pickle.load(f)
    with open(rank_word, 'rb') as f:#load words file
        rank_word_dict = pickle.load(f)
    valid_list = create_valids_list(query,rank_word_dict) #get the valid list
    new_dict = valid_dict(ranking_dict,valid_list) #get the valid dictionary
    sorted_dict = sort_dict(new_dict, max_results) #sort the dictionary from heighest to lowest
    weighted_dict = weighted_values(rank_word_dict, sorted_dict, query) #get the weighted value og the dictionary
    w_sorted_dict = sort_dict(weighted_dict, max_results)
    print_vertically(w_sorted_dict) #print the dictionary vertically


if __name__ == "__main__":
    if sys.argv[1] == 'crawl':
        base_url = sys.argv[2]
        relative_url = sys.argv[3]
        dict_file = sys.argv[4]
        crawl(base_url,relative_url,dict_file)
    if sys.argv[1] == 'page_rank':
        iterations = sys.argv[2]
        out_file = sys.argv[3]
        ranking_file = sys.argv[4]
        page_rank(iterations, out_file, ranking_file)
    if sys.argv[1] == 'words_dict':
        base_url = sys.argv[2]
        index_file = sys.argv[3]
        rank_word = sys.argv[4]
        words_dict(base_url, index_file, rank_word)
    if sys.argv[1] == 'search':
        query = sys.argv[2]
        ranking_file = sys.argv[3]
        rank_word = sys.argv[4]
        max_results = sys.argv[5]
        search(query, ranking_file, rank_word, max_results)




