from unittest import TestCase, main
from quiz_2 import create_quiz_from_file


class TestQuiz(TestCase):

    def test_1(self):
        qz = create_quiz_from_file('disney.txt')
        question = qz.questions[0]
        question.wrong_answers = {'Answer 1': 2, 'Answer 2': 3, 'Answer 3': 1,
                                  'Answer 4': 4, 'Answer 5': 2, 'Answer 6': 3}
        print(question.get_wrong_answers(4))


if __name__ == '__main__':
    main()