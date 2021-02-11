from random import shuffle

numberOfAnswers = 5


def create_quiz_from_file(filename):
    """
    Given method, which creates quiz from the text file
    :param filename: name of the file with quiz
    :return: quiz, Class Quiz
    """
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            command, data = line.split(' ', 1)
            data = data.strip()
            if command == 'name':
                quiz = Quiz(data)
            elif command == 'q':
                text = data
                int_q = False
            elif command == 'iq':
                text = data
                int_q = True
            elif command == 'a':
                if int_q:
                    question = IntQuestion(text, int(data.strip()))
                else:
                    question = Question(text, data)
                quiz.add_question(question)
            elif command == 'w':
                question.add_wrong(Wrong_answer(data))
    return quiz


class Wrong_answer:
    """
    Class for wrong answers
    """

    def __init__(self, text):
        """
        :param text: text of a wrong answer read from the file
        """
        self.text = text
        self.chosen = 0
        self.displayed = 0

    def get_text(self):
        """
        :return: text of the question
        """
        return self.text

    def inc_chosen(self):
        """
        Increase counter of answer choices
        :return:
        """
        self.chosen += 1

    def inc_displayed(self):
        """
        Increase counter of answer display times
        :return:
        """
        self.displayed += 1

    def score(self):
        """
        Calculates score due to the instructions
        :return: calculated score
        """
        return (2 * self.chosen + 1) / (self.displayed + 1)


class Question:
    def __init__(self, question, answer):
        """
        Class constructor
        :param question: Text of the question
        :param answer: Right answer on the question
        """
        self.question = question  # variable for question
        self.answer = answer  # variable for right answer
        self.wrong_answers = []  # list of wrong answers

    def add_wrong(self, wrong_answer):
        """
        Adds wrong answers to the question
        :param wrong_answer: wrong answer to add
        :return: None
        """
        self.wrong_answers.append(wrong_answer)

    def ask(self, alternatives=None):
        """
        Print question, list of answers in the console.
        Asks for a number of user's answers
        :param alternatives: number of alternatives to show. Default value is None - show all the alternatives
        :return: Tuple(user's answer, right answer)
        """
        # wrong answers choice
        if alternatives and (len(self.wrong_answers) >= alternatives - 1):
            wrong_answers = self.get_wrong_answers(alternatives - 1)
        else:
            wrong_answers = [item.get_text for item in self.wrong_answers]  # number of alternatives is not defined
                                                                            # or too few wrong answers

        answers = [self.answer] + wrong_answers  # full set of answers
        shuffle(answers)  # shuffles the list of answers
        right_answer = answers.index(self.answer) + 1  # defines the number of right answer

        # +1 for displayed answers
        wa_dict = {item.get_text(): item for item in self.wrong_answers}
        for item in wrong_answers:
            wa_dict[item].inc_displayed()

        print(self.question)  # prints question in the console
        for answer in enumerate(answers):  # prints answers one after another
            print('{:d}. {:s}'.format(answer[0] + 1, answer[1]))
        try:  # asks for users choice
            users_answer = int(input())
        except ValueError:  # handles value error
            return 0, right_answer

        # +1 for chosen answer
        if users_answer != right_answer:
            wa_dict[answers[users_answer - 1]].inc_chosen()

        return users_answer, right_answer

    def get_wrong_answers(self, n):
        """
        Makes a list of wrong answers with maximum frequencies
        :param n: number of returning wrong answers
        :return: a list of wrong answers
        """
        answers = []
        wa_dict = {item: item.score() for item in self.wrong_answers}

        freqs = sorted(set(wa_dict.values()), reverse=True)
        for f in freqs:
            answers_to_add = [item.get_text() for item in wa_dict.keys() if wa_dict[item] == f]
            shuffle(answers_to_add)
            answers.extend(answers_to_add)
            if len(answers) >= n:
                break
        return answers[:n]


class IntQuestion(Question):
    def ask(self, alternatives=None):
        print(self.question)  # prints question in the console
        try:  # asks for users choice
            users_answer = int(input())
        except ValueError:  # handles value error
            return 0, self.answer
        return users_answer, self.answer


class Quiz:
    def __init__(self, name):
        """
        Class constructor
        :param name: Name of the quiz
        """
        self.name = name
        self.questions = []

    def add_question(self, q):
        """
        Adds a question to the quiz
        :param q: question, Class Question
        :return: None
        """
        self.questions.append(q)

    def do(self):
        """
        Makes a quiz
        :return: None
        """
        counters = [0, 0]  # counters of right answers and total questions
        print(self.name)
        print('============')
        for question in self.questions:
            answers = question.ask(numberOfAnswers)  # ask a question by ask() method of Class question
            if answers[0] == answers[1]:  # if the answer is correct
                print('Correct!')
                counters[0] += 1
            else:
                print('Sorry, no. Correct answer: {:d}\n'.format(answers[1]))  # if the answer is incorrect
            counters[1] += 1
        print('\n You answered {:d} of {:d}'.format(counters[0], counters[1]))

    def do_until_right(self):
        """
        Makes you take quiz all over again until you get a correct answer
        :return: None
        """
        print(self.name)
        print('============')
        for question in self.questions:
            while True:
                answers = question.ask()
                if answers[0] == answers[1]:
                    print('Correct!\n')
                    break
                else:
                    print('Sorry, no. Try again!\n')
                    question.add_freq(answers[2][answers[0] - 1])


if __name__ == "__main__":
    create_quiz_from_file('disney.txt').do()
