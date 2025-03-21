
def results():
    lst = ["scar", "Crookshanks","Horcrux", "Pensieve McGonagall", "broom wand cape"]
    for i in range(len(lst)):
        print(moogle(lst[i], r"C:\Users\user\PycharmProjects\week 6\ranking_file.pkl", r"C:\Users\user\PycharmProjects\week 6\rank_word.pkl",4))
        print("**********")
