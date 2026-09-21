from otree.api import *
import itertools
import random

doc = """
Pilot3 on efficacy and memory (online)
"""


# FILLER TASK
ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
COLS = [1, 2, 3, 4, 5, 6]
GRID_COUNTS = {
    "A1": 8,  "A2": 10, "A3": 9,  "A4": 11, "A5": 18, "A6": 20,
    "B1": 12, "B2": 9,  "B3": 13, "B4": 7,  "B5": 14, "B6": 9,
    "C1": 7,  "C2": 15, "C3": 3,  "C4": 16, "C5": 6,  "C6": 17,
    "D1": 17, "D2": 6,  "D3": 19, "D4": 4,  "D5": 18, "D6": 9,
    "E1": 4,  "E2": 21, "E3": 12, "E4": 22, "E5": 13, "E6": 10,
    "F1": 18, "F2": 8,  "F3": 20, "F4": 18, "F5": 25, "F6": 14,
    "G1": 9,  "G2": 12, "G3": 9,  "G4": 22, "G5": 15, "G6": 10,
}

CELLS = [
    "C1",
    "E2",
    "C4",
    "G3",
    "A6",
    "F2",
    "B3",
    "G5",
    "F1",
    "D6",
]  # participants do the same questions at this fixed order


# TRUE RATE
CRIME_RATE = {
    'North East (England)': 16.22,
    'North West (England)': 12.76,
    'Yorkshire and The Humber (England)': 18.83,
    'East Midlands (England)': 10.88,
    'West Midlands (England)': 14.75,
    'East (England)': 9.539,
    'London (England)': 18.73,
    'South East (England)': 9.696,
    'South West (England)': 8.81,
    'Wales': 8.22,
}

# FUNCTION
def creating_session(subsession):
    treatment_cycle = itertools.cycle(['recall', 'high', 'low'])
    for player in subsession.get_players():
        player.treatment = next(treatment_cycle)


def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt4uk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # feedback question
    DEMAND = [
        dict(name='believe', label='I made up my mind in which of the options I believed most and then ticked it.'),
        dict(name='against', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked something else.'),
        dict(name='conform', label='I made up my mind about which of the options the researchers wanted me to tick '
                                   'and then ticked it.'),
        dict(name='random', label='I just made a random guess, like mentally flipping a coin.')
    ]


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
    record = models.BooleanField(
        label='If you have written down, taken screenshot/photo of, or used any other method to '
              'record the numbers on the information slides, please tick "Yes". '
              'You will receive the study reward independent of your answer.'
    )

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )
    aqvideo_attempts = models.IntegerField(initial=0)
    aqvideo = models.BooleanField(initial=0)

    # Treatment assignment
    treatment = models.StringField()

    # Demographics
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
    crime_worry = models.IntegerField(choices=range(1, 8))
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
    scared = likert1('Scared')
    nervous = likert1('Nervous')
    calm = likert1('Calm')
    relaxed = likert1('Relaxed')
    encouraged = likert1('Encouraged')
    discouraged = likert1('Discouraged')

    control = models.IntegerField(choices=range(1, 8))

    res_ind = models.IntegerField(choices=range(1, 8))
    res_com = models.IntegerField(choices=range(1, 8))
    res_city = models.IntegerField(choices=range(1, 8))
    res_state = models.IntegerField(choices=range(1, 8))

    # Filler task score
    answer = models.IntegerField(blank=True)
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
    post_recall = models.IntegerField(choices=range(1, 8))
    recall1 = models.IntegerField(choices=range(1, 8))
    recall2 = models.IntegerField(choices=range(1, 8))
    recall3 = models.IntegerField(choices=range(1, 8))

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
    expcrime = models.BooleanField(
        label='Have you or your close family experienced burglary in your life? (Optional)',
        blank=True
    )
    # experimenter demand effect
    believe = models.BooleanField(blank=True, initial=0)
    against = models.BooleanField(blank=True, initial=0)
    conform = models.BooleanField(blank=True, initial=0)
    random = models.BooleanField(blank=True, initial=0)


# PAGES
class Introduction(Page):
    pass


class Consent(Page):
    pass


class ACvideo(Page):
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def error_message(player, values):
        if values['answer'] == 3169:
            return
        player.aqvideo_attempts += 1
        if player.aqvideo_attempts < 2:
            return 'You have typed in wrong digits. Please try again.'

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == 3169:
            player.aqvideo = 1


class ACvideofail(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.aqvideo != 1


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employ', 'income',
                   'region', 'origin_father', 'origin_mother', 'stand',
                   'vote', 'vote_yes', 'vote_no',
                   'crime_worry', 'immi_familiar', 'immi_attitude']


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
        image = {
            'North East (England)': 'Slide3.PNG',
            'North West (England)': 'Slide4.PNG',
            'Yorkshire and The Humber (England)': 'Slide5.PNG',
            'East Midlands (England)': 'Slide6.PNG',
            'West Midlands (England)': 'Slide7.PNG',
            'East (England)': 'Slide8.PNG',
            'London (England)': 'Slide9.PNG',
            'South East (England)': 'Slide10.PNG',
            'South West (England)': 'Slide11.PNG',
            'Wales': 'Slide12.PNG',
        }
        return {
            'image': image.get(player.region),
        }


class Info4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'high' or player.treatment == 'low'

    @staticmethod
    def vars_for_template(player):
        image = {
            'high': 'Slide13.PNG',
            'low': 'Slide15.PNG',
        }
        return {
            'image': image.get(player.treatment),
        }


class Info5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'high' or player.treatment == 'low'

    @staticmethod
    def vars_for_template(player):
        image = {
            'high': 'Slide14.PNG',
            'low': 'Slide16.PNG',
        }
        return {
            'image': image.get(player.treatment),
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


class Responsibility(Page):
    form_model = 'player'
    form_fields = ['res_ind', 'res_com', 'res_city', 'res_state']


class CountIntro(Page):
    pass


class CountC1(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "C1"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["C1"]:
            player.score += 1


class CountE2(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "E2"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["E2"]:
            player.score += 1


class CountC4(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "C4"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["C4"]:
            player.score += 1


class CountG3(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "G3"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["G3"]:
            player.score += 1


class CountA6(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "A6"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["A6"]:
            player.score += 1


class CountF2(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "F2"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["F2"]:
            player.score += 1


class CountB3(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "B3"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["B3"]:
            player.score += 1


class CountG5(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "G5"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["G5"]:
            player.score += 1


class CountF1(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "F1"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["F1"]:
            player.score += 1


class CountD6(Page):
    timeout_seconds = 12
    form_model = 'player'
    form_fields = ['answer']

    @staticmethod
    def vars_for_template(player):
        return {"cell": "D6"}

    @staticmethod
    def before_next_page(player, timeout_happened):
        answer = player.field_maybe_none('answer')
        if answer == GRID_COUNTS["D6"]:
            player.score += 1


class CountEnd(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.bonus1 = player.score * 0.02


class Memory(Page):
    form_model = 'player'
    form_fields = ['memory']

    @staticmethod
    def before_next_page(player, timeout_happened):
        true_value = CRIME_RATE.get(player.region)
        guess = player.memory

        if abs(guess - true_value) <= 0.1:
            player.bonus2 = 0.20
        else:
            player.bonus2 = 0


class Postrecall(Page):
    form_model = 'player'
    form_fields = ['post_recall', 'recall1', 'recall2', 'recall3']


class Postbelief(Page):
    form_model = 'player'
    form_fields = ['post_eu', 'post_noneu']


class Feedback1(Page):
    form_model = 'player'
    form_fields = ['purpose', 'feedback', 'AIuse', 'record', 'expcrime']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.bonus_total = player.bonus1 + player.bonus2


class Feedback2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [demand['name'] for demand in C.DEMAND]


class Debrief1(Page):
    pass


class Debrief2(Page):
    pass


class BonusFeedback(Page):
    pass


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction, Consent,
    ACvideo,  # video attention check for bot detection
    ACvideofail,  # dead end for participants who failed the bot check twice
    Demographics,
    BaseExpectation,  # record optimist/pessimist
    Prebelief,  # pre-treatment model belief
    AC,  # attention check
    Info1, Info2, Info3, Info4, Info5,  # information slides
    Emotion,  # encourage/discourage
    Control,  # perceived efficacy
    Responsibility,  # responsibility attrition
    CountIntro, CountC1, CountE2, CountC4, CountG3, CountA6,
    CountF2, CountB3, CountG5, CountF1, CountD6, CountEnd,  # filler task
    Memory,  # memory test
    Postrecall,  # selective recall
    Postbelief,  # post-treatment model belief
    Feedback1, Feedback2,
    Debrief1, Debrief2, BonusFeedback, ProlificCompletion,
]
