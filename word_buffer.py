class buf():
    def __init__(self):
        self.words = []
    
    def add(self, word: str) -> None:
        if len(self.words) <= 2:
            self.words.append(word)
        else:
            # [old_word1, old_word2, old_word3] -> [old_word2, old_word3, new_word]
            self.words[0] = self.words[1]
            self.words[1] = self.words[2]
            self.words[2] = word
        
    def get_words(self) -> list:
        return self.words
    

if __name__=="__main__":
    my_buf = buf()
    words = ["1", "2", "3", "4", "5"]
    for word in words:
        my_buf.add(word)
    
    assert(my_buf.get_words() == ["3", "4", "5"])