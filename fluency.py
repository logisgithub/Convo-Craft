from textblob import TextBlob
from language_tool_python import LanguageTool
import matplotlib.pyplot as plt
import webbrowser
import time

class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        self.grammar_check = LanguageTool('en-US')

    def correct_spell(self, text):
        words = text.split()
        corrected_words = [str(TextBlob(word).correct()) for word in words]
        corrected_text = " ".join(corrected_words)
        return corrected_text

    def correct_grammar(self, text):
        matches = self.grammar_check.check(text)

        found_mistakes = [mistake.ruleId for mistake in matches]
        found_mistakes_count = len(found_mistakes)
        text=text.split()
        
        mistakes=(found_mistakes_count/len(text))*100
        correct=abs(mistakes-len(text))
        fluency_score=(correct/len(text))*100
        
        return fluency_score

    def classify_fluency_level(self, fluency_score):
        if fluency_score<20:
            return "Need to improve more. Fluency is bad at the moment."
        elif 20 < fluency_score <= 40:
            return "Basic fluency. Improve basic grammar skills like tenses, parts of speech and know where to use past tense and present tense."
        elif 40 < fluency_score <= 80:
            return "Intermediate Fluency. Practice daily atleast for 5 minutes to gain additional speaking fluency"
        else:
            return "Advanced Fluency. You are good at speaking. Keep it up!"
    
def get_sentences(answers):
    obj = SpellCheckerModule()
    corrected_text = obj.correct_spell(answers)
    fluency_score = obj.correct_grammar(corrected_text)
    fluency_level = obj.classify_fluency_level(fluency_score)
    
    print(f"Fluency percentage: {fluency_score:.2f}%")
    print(f"Fluency level: {fluency_level}")
    html=f"<html><body><center><h1>Fluency Analysis Results</h1><h3>Fluency Percentage:  {fluency_score} </span>%</h3><h3>Fluency Level: {fluency_level} </span></h3><center></body></html>"
    with open("report.html","w") as html_file:
        html_file.write(html)
    time.sleep(2)
    webbrowser.open_new_tab("report.html")
    # Plotting
    '''plt.bar(["Fluency Level"], [fluency_score], color=['green' if fluency_score > 80 else 'yellow' if fluency_score > 40 and fluency_score<80 else 'red'])
    plt.ylim(0, 100)
    plt.title('Fluency Level')
    plt.ylabel('Fluency Score (%)')
    plt.show()'''