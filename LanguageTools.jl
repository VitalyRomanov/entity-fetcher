module LanguageTools

function load(filepath)
    lemma_dict_file = open(filepath, "r")
    lemma_dict = Dict()
    for line in eachline(lemma_dict_file)
        parts = split(strip(line), "\t")
        lemma_dict[parts[1]] = parts[2]
    end
    return lemma_dict
end

function tokenize(line)
    matches = eachmatch(r"[A-Za-zА-Яа-я][A-Za-zА-Яа-я-]+|[A-Za-zА-Яа-я]|[^\w\s]|[0-9]+", line)
    tokens = [m.match for m in matches]
    return tokens
end
end

# en_lemm = Lemmatizer.load("en_lemma.dict")
# println(en_lemm["it"])
# println(en_lemm["has"])

# println(Lemmatizer.tokenize("a bb cbb"))