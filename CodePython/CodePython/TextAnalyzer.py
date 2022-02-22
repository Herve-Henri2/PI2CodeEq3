import TextAnalysis
from datetime import datetime

class TextAnalyzer(object):
    """
    The TextAnalyser object is meant to read a block of text and determine whether the specified company is in a state of danger, attack or neither.

    Instance attributes
    -------------
    company: str
        The company name of which we are trying to check the security status.
    text: str
        The block of text that needs to be analyzed, it can be an article or a tweet.
    link: str
        The link from which the text was extracted.
    text_date: date
        The date on which the text was written.
    status: int
        A number that indicates the company security status.
        For example, a company that is safe will have a status equal to 0, whereas one where the occurence of an attack
        is certain will have a status equal to 3.
    result: str
        The status description after analysis.
    date: datetime
        Date and time of analysis.   
    crit_sents: list[str]
        List of sentences that led to raising an alert. If the status is > 0, this variable cannot be empty.
    
    Class attributes
    -------------
    Id: int
        The indentifier of the created TextAnalyzer object.
    """

    #Class attributes
    Id=0

    #Constructor
    def __init__(self, company, text, link, text_date):
        TextAnalyzer.Id+=1
        self.id=TextAnalyzer.Id
        if company[0].islower():
            company.capitalize()
        self.company=company
        self.text=text
        self.link=link 
        self.text_date=text_date 
        self.status=-1 
        self.result=""  
        self.date="" 
        self.crit_sents=[] 

    #Instance Method
    def __str__(self):
        if((self.link).startswith("https://twitter.com")):
            return "Id: "+str(self.id)+"\nCompany: "+self.company+"\nText: "+self.text+"\n\nFound on:"+self.link+"\nTweet date: "+str(self.text_date)+"\nAnalysis date: "+str(self.date)+ \
            "\nStatus: "+str(self.status)+"\nAnalysis result: "+self.result+"\nCritical sentences:\n "+str(self.crit_sents)
        else:
            return "Id: "+str(self.id)+"\nCompany: "+self.company+"\nText: "+self.text+"\n\nFound on:"+self.link+"\nArctile date: "+str(self.text_date)+"\nAnalysis date: "+str(self.date)+ \
            "\nStatus: "+str(self.status)+"\nAnalysis result: "+self.result+"\nCritical sentences:\n "+str(self.crit_sents)

    def toString(self):
        return "Company: "+self.company+" Analysis result: "+self.result

    def FindCompanyMentions(self):
        """
        Searches for the sentences mentionning the company in the text.
        Returns them in a list.
        """
        sentences=TextAnalysis.DetectSentences(self.text, [self.company])
        #print sentences
        return sentences

    def RunAnalysis(self, wordDic, sentDic):
        """
        Analyzes the text variable to update the status, result, date and crit_sents variables.

        Parameters
        -------------
        wordDic: list[str]
            List of keywords from which we will search specific sentences.
            (These keywords belong to the cyber attack lexical field.)

        sentDic: list[str]
            List of sentences we will use to compare the text sentences and raise an alert based on the similarity.
            (The sentences in this variable are typically the ones that would make us raise a level 3 alert.)
        """
        max_rate=0.9 #If this similarity score is reached or exceeded, a level 3 alert is raised.
        med_rate=0.6
        lvl2_rate_nb=7 #If 7 scores are located between the med_rate and max_rate, a level 2 alert is raised.
        lvl1_rate_nb=3 #If 3 scores are located between the med_rate and max_rate, a level 1 alert is raised.
        verif_max_rate=False
        self.date=datetime.now()
        self.status=0 #Default status
        self.result="Nothing to report." #Default result
        similarityScores={}
        keysentences=TextAnalysis.DetectSentences(self.text, wordDic) #First, we start by extracting the sentences that contain our keywords.
        for text_sentence in keysentences: #Then, we compare each of these sentences with the example phrases from our sentDic variable.
            similarityScores[text_sentence]=[]
            for example_sentence in sentDic:
                score=TextAnalysis.CompareSimilarity(str(text_sentence),str(example_sentence)) #We evaluate the similarity between the extracted sentence and the example sentence.
                similarityScores[text_sentence].append(score) #And save the score
        for key in similarityScores: #We then browse for each extracted sentence the corresponding scores. Key is the extracted sentence, value is the list of scores after comparison.
            scores=similarityScores[key]
            count_med_rate=0
            for score in scores: #We browse the score list for a given sentence.
                if score>=max_rate:  #We verify whether the maximum score is reached or exceeded, if so we raise a level 3 alert.
                    verif_max_rate=True 
                    self.status=3
                    self.result="/!\\ A level 3 alert has been raised /!\\"
                    print("This sentence is very critical: "+str(key))
                    break #We move on to the next phrase as it will never be higher.
                if score>med_rate and score<max_rate:
                    count_med_rate+=1
                    if count_med_rate >= lvl2_rate_nb:
                        if self.status < 3: #A lower status cannot overwrite a higher one.
                            self.status=2
                            self.result="/!\\ A level 2 alert has been raised /!\\"
                            #We do not move on to the next phrase here because there is a possibility that the next score will be > max_rate 
                            #and thus overwrite this assignment.
                    if count_med_rate >= lvl1_rate_nb:
                        if self.status < 2:
                            self.status=1
                            self.result="/!\\ A level 1 alert has been raised /!\\"
                            #We do not move on to the next phrase here because there is a possibility that the next score is > max_rate or that
                            #count_med_rate will become >= lvl2_rate_nb and thus overwrite this assignment.
            if self.status>0: #If the sentence raised an alert, we save it in our crit_sents variable.
                self.crit_sents.append(key)
        #print("Number of critical sentences :"+str(len(self.crit_sents)))
        

        

    if __name__=="__main__":
        #Test()
        print("")


