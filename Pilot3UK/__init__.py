from otree.api import *
import itertools
import random

doc = """
Pilot3 on efficacy and memory (online)
"""


# FILLER TASK
ROWS = ['A','B','C','D','E','F','G']
COLS = [1,2,3,4,5,6]
GRID_COUNTS = {
    "A1": 8,  "A2": 10, "A3": 9,  "A4": 11, "A5": 18, "A6": 20,
    "B1": 12, "B2": 9,  "B3": 13, "B4": 7,  "B5": 14, "B6": 9,
    "C1": 7,  "C2": 15, "C3": 3,  "C4": 16, "C5": 6,  "C6": 17,
    "D1": 17, "D2": 6,  "D3": 19, "D4": 4,  "D5": 18, "D6": 9,
    "E1": 4,  "E2": 21, "E3": 12, "E4": 22, "E5": 13, "E6": 10,
    "F1": 18, "F2": 8,  "F3": 20, "F4": 18, "F5": 25, "F6": 14,
    "G1": 9,  "G2": 12, "G3": 9,  "G4": 22, "G5": 15, "G6": 10,
}


# CRIME RATE
RATE20 = {
    'North East (England)': 16.22,
    'North West (England)': 12.76,
    'Yorkshire and The Humber (England)': 18.83,
    'East Midlands (England)': 10.88,
    'West Midlands (England)': 14.75,
    'East (England)': 9.539,
    'London (England)': 18.73,
    'South East (England)': 9.696,
    'South West (England)': 8.8108,
    'Wales': 8.2235,
}


# FUNCTION
def creating_session(subsession):
    import itertools
    efficacy_cycle = itertools.cycle(['high', 'low'])
    for player in subsession.get_players():
        player.efficacy = next(efficacy_cycle)


def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)


def random_cell():
    return random.choice([r + str(c) for r in ROWS for c in COLS])


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt3uk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Exclude bots
    AIuse = models.BooleanField(
        label='If you have used any AI tool in completing this study, please tick "Yes". '
              'You will receive the study reward independent of your answer.'
    )

    # Treatment assignment
    efficacy = models.StringField()

    # Baseline crime expectation
    region = models.StringField(
        label='Please tell us your region of residence.',
        choices=['North East (England)', 'North West (England)', 'Yorkshire and The Humber (England)',
                 'East Midlands (England)', 'West Midlands (England)', 'East (England)', 'London (England)',
                 'South East (England)', 'South West (England)', 'Wales']
    )
    propburglary = models.FloatField(label='You or your family experience a burglary?', min=0, max=100)
    prophealth = models.FloatField(label='You or your family experience a major health issue?', min=0, max=100)
    proplottery = models.FloatField(label='You or your family win a National Lottery Draw?', min=0, max=100)
    propfriend = models.FloatField(label='you or your family make a new best friend?', min=0, max=100)

    # Pre-treatment model belief
    pre_eu = models.IntegerField(
        widget=widgets.RadioSelect,
        label='What do you think? Do immigrants from EU countries (e.g., Poland, Romania, or Bulgaria) '
              'commit less or more crimes than the average native British citizen?',
        choices=[(1, 'Much less'),
                 (2, 'Less'),
                 (3, 'About the same'),
                 (4, 'More'),
                 (5, 'Much more')],
    )
    pre_noneu = models.IntegerField(
        widget=widgets.RadioSelect,
        label='What do you think? Do immigrants from non-EU countries (e.g., India, Pakistan, or Nigeria) '
              'commit less or more crimes than the average native British citizen?',
        choices=[(1, 'Much less'),
                 (2, 'Less'),
                 (3, 'About the same'),
                 (4, 'More'),
                 (5, 'Much more')],
    )

    # Manipulation check question
    control = models.IntegerField(choices=range(1, 8))
    scared = likert1('Scared')
    nervous = likert1('Nervous')
    calm = likert1('Calm')
    relaxed = likert1('Relaxed')
    encouraged = likert1('Encouraged')
    discouraged = likert1('Discouraged')

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )

    # Filler task score
    score = models.IntegerField(initial=0)
    bonus1 = models.FloatField(initial=0)

    # Memory
    memory = models.FloatField(
        label='According to the information slides you read, what is the probability that your household '
              'will experience a burglary in the next 20 years?'
    )
    bonus2 = models.FloatField()
    bonus_total = models.FloatField()

    # Selective recall
    recall = models.IntegerField(choices=range(1, 8))
    legitimacy = models.IntegerField(choices=range(1, 8))
    moreinfo = models.BooleanField(
        label='Do you want to get more evidence related to this debate?',
        choices=[(True, 'Yes, I would like to'),
                 (False, 'No, I would not like to')],
        widget=widgets.RadioSelect
    )

    # Post-treatment model belief
    post_eu = models.IntegerField(
        widget=widgets.RadioSelect,
        label='What do you think? Would a slightly increased immigration from EU countries (e.g., Poland, Romania, or Bulgaria) '
              'overall lead to an increasing or decreasing crime rate in the UK?',
        choices=[(1, 'Strongly increasing rate'),
                 (2, 'Increasing rate'),
                 (3, 'Neither increasing nor decreasing rate'),
                 (4, 'Decreasing rate'),
                 (5, 'Strongly decreasing rate')],
    )
    post_noneu = models.IntegerField(
        widget=widgets.RadioSelect,
        label='What do you think? Would a slightly increased immigration from non-EU countries (e.g., India, Pakistan, or Nigeria) '
              'overall lead to an increasing or decreasing crime rate in the UK?',
        choices=[(1, 'Strongly increasing rate'),
                 (2, 'Increasing rate'),
                 (3, 'Neither increasing nor decreasing rate'),
                 (4, 'Decreasing rate'),
                 (5, 'Strongly decreasing rate')],
    )

    # Feedback, for pilot only
    purpose = models.LongStringField(
        label='Do you have any idea about the purpose of this study? If yes, please briefly describe in the text field. (Optional)',
        blank=True
    )
    feedback = models.LongStringField(
        label='If you have any other feedback to this study, please leave it here. (Optional)',
        blank=True
    )

    # Demographic variables
    age = models.IntegerField(
        label='Age'
    )
    gender = models.StringField(
        widget=widgets.RadioSelect,
        label='Gender',
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say']
    )
    education = models.StringField(
        widget=widgets.RadioSelect,
        label='Highest education level',
        choices=['No formal education', 'Primary school', 'Secondary school',
                 'University', 'Postgraduate', 'Prefer not to say']
    )
    employ = models.StringField(
        label='What is your current employment status?',
        choices=['Full-time employee', 'Part-time employee', 'Self-employed or small business owner',
                 'Unemployed and looking for work', 'Not currently working and not looking for work',
                 'Student', 'Retiree', 'Prefer not to say']
    )
    income = models.StringField(
        label='What was your monthly income, before taxes, on average last year?',
        choices=['Less than £1,000', '£1,000 – £1,499', '£1,500 – £1,999', '£2,000 – £2,499', '£2,500 – £2,999',
                 '£3,000 – £3,999', '£4,000 – £6,999', 'More than £6,000', 'Prefer not to say']
    )
    origin_father = models.StringField(
        label='Where was your father born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Mexico or South America',
                 'Oceania', 'Prefer not to say']
    )
    origin_mother = models.StringField(
        label='Where was your mother born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Mexico or South America',
                 'Oceania', 'Prefer not to say']
    )
    stand = models.IntegerField(choices=range(1, 8))
    vote = models.BooleanField(
        widget=widgets.RadioSelect,
        label='Did you vote in the last general election?',
        choices=[(True, 'Yes'), (False, 'No')]
    )
    vote_yes = models.StringField(
        label='In the last general election, you supported:',
        choices=['Conservative Party', 'Labour Party', 'Democratic Unionist Party', 'Sinn Féin',
                 'Liberal Democrats', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other', 'Prefer not to say'],
        blank=True,
    )
    vote_no = models.StringField(
        label='Even if you did NOT vote, please indicate the party that you were most likely to have voted '
              'for or who represents your views most closely:',
        choices=['Conservative Party', 'Labour Party', 'Democratic Unionist Party', 'Sinn Féin',
                 'Liberal Democrats', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other', 'Prefer not to say'],
        blank=True,
    )
    worry = models.IntegerField(choices=range(1, 8))
    immi_familiar = models.IntegerField(choices=range(1, 8))
    immi_attitude = models.IntegerField(
        widget=widgets.RadioSelect,
        label='Which of the following statements most closely reflect your view on the number of <b>legal immigrants</b> '
              'who are permitted to come to the United Kingdom to live?',
        choices=[(1, 'The number of legal immigrants today is a very big problem. '
                     'We should ask many legal immigrants to leave the UK, '
                     'and stop accepting new immigrants.'),
                 (2, 'The number of legal immigrants today is a big problem. '
                     'We should decrease by a lot the number permitted to come to the UK. '),
                 (3, 'The number of legal immigrants today is somewhat of a problem. '
                     'We should try and decrease by a bit the number permitted to come to the UK. '),
                 (4, 'The number of legal immigrants today is not a problem. '
                     'We should keep letting in the same number of immigrants to come to the UK. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come to the UK. ')
                 ],
    )


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employ', 'income',
                   'region', 'origin_father', 'origin_mother', 'stand',
                   'vote', 'vote_yes', 'vote_no',
                   'worry', 'immi_familiar', 'immi_attitude']


class BaseExpectation(Page):
    form_model = 'player'
    form_fields = ['propburglary', 'prophealth', 'proplottery', 'propfriend']


class Prebelief(Page):
    form_model = 'player'
    form_fields = ['pre_eu', 'pre_noneu']


class AC(Page):
    form_model = 'player'
    form_fields = ['aq']


class Info1(Page):
    pass


class Info2(Page):
    pass


class Info3(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'North East (England)': 'slides/Slide3.PNG',
            'North West (England)': 'slides/Slide4.PNG',
            'Yorkshire and The Humber (England)': 'slides/Slide5.PNG',
            'East Midlands (England)': 'slides/Slide6.PNG',
            'West Midlands (England)': 'slides/Slide7.PNG',
            'East (England)': 'slides/Slide8.PNG',
            'London (England)': 'slides/Slide9.PNG',
            'South East (England)': 'slides/Slide10.PNG',
            'South West (England)': 'slides/Slide11.PNG',
            'Wales': 'slides/Slide12.PNG',
        }
        return {
            'image': image.get(player.region),
        }


class Info4(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'high': 'slides/Slide13.PNG',
            'low': 'slides/Slide15.PNG',
        }
        return {
            'image': image.get(player.efficacy),
        }


class Info5(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'high': 'slides/Slide14.PNG',
            'low': 'slides/Slide16.PNG',
        }
        return {
            'image': image.get(player.efficacy),
        }


class Emotion(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['scared', 'nervous', 'discouraged', 'encouraged', 'calm', 'relaxed']
        random.shuffle(survey)
        return survey


class Control(Page):
    form_model = 'player'
    form_fields = ['control']


class CountIntro(Page):
    pass


class Count(Page):
    timeout_seconds = 120  # two minutes

    @staticmethod
    def live_method(player, data):
        # start task
        if data["type"] == "start":
            cell = random_cell()
            player.participant.vars["current_cell"] = cell

            return {
                player.id_in_group: {
                    "cell": cell
                }
            }

        # submit answer
        if data["type"] == "answer":
            current_cell = player.participant.vars["current_cell"]
            correct_answer = GRID_COUNTS[current_cell]

            if data["answer"] == correct_answer:
                player.score += 1

            cell = random_cell()
            player.participant.vars["current_cell"] = cell

            return {
                player.id_in_group: {
                    "cell": cell
                }
            }

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.bonus1 = player.score * 0.02


class CountEnd(Page):
    pass


class Memory(Page):
    form_model = 'player'
    form_fields = ['memory']

    @staticmethod
    def before_next_page(player, timeout_happened):
        true_value = RATE20[player.region]
        guess = player.memory

        if abs(guess - true_value) <= 0.3:
            player.bonus2 = 0.20
        else:
            player.bonus2 = 0


class Recall(Page):
    form_model = 'player'
    form_fields = ['recall', 'legitimacy', 'moreinfo']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.bonus_total = player.bonus1 + player.bonus2


class Postbelief(Page):
    form_model = 'player'
    form_fields = ['post_eu', 'post_noneu']


class Debrief1(Page):
    pass


class Debrief2(Page):
    pass


class Feedback(Page):
    form_model = 'player'
    form_fields = ['purpose', 'feedback', 'AIuse']


class BonusFeedback(Page):
    pass


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction, Consent,
    Demographics,
    BaseExpectation,  # record optimist/pessimist
    Prebelief,  # pre-treatment model belief
    AC,  # attention check
    Info1, Info2, Info3, Info4, Info5,  # information slides
    Emotion,  # encourage/discourage
    Control,  # perceived control
    CountIntro, Count, CountEnd, # filler task
    Memory,  # memory test
    Recall,  # selective recall
    Postbelief,  # post-treatment model belief
    Debrief1, Debrief2, Feedback, BonusFeedback, ProlificCompletion,
]