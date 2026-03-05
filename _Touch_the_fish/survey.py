
class AnonymousSurvey():
    """收集匿名调查问卷答案"""
    def __init__(self, question):
        self.question = question
        self.responses = []

    def show_question(self, question):
        """显示调调查问卷"""
        print(question)

    def store_response(self, new_response):
        """存储单份调查答卷"""
        self.responses.append(new_response)

    def show_results(self, responses):
        """显示收集到的所有答卷"""
        print("Survey results: ")
        for response in responses:
            print("- " + response)
