from otree.api import *
import itertools
import random

doc = """
Pretest on anticipatory utility and donation (online)
"""
# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    task = itertools.cycle(['simple_hope', 'simple_unhope', 'complex_hope', 'complex_unhope'])
    # Control group is not included in the pretest on narrative understanding
    for player in subsession.get_players():
        player.task = next(task)

def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)

def cq_group_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_group_choices' not in player.participant.vars:
        choices = ['Retired workers',
                   'Immigrants with little education',
                   'University graduates',
                   'Children']
        random.shuffle(choices)
        player.participant.vars['cq_group_choices'] = choices
    return player.participant.vars['cq_group_choices']

def cq_challenge_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_challenge_choices' not in player.participant.vars:
        choices = ['Language barriers',
                   'Difficulty finding stable jobs',
                   'Access to healthcare',
                   'High living costs']
        random.shuffle(choices)
        player.participant.vars['cq_challenge_choices'] = choices
    return player.participant.vars['cq_challenge_choices']

def cq_ngo_choices(player):
    # Shuffle choices at the first time loading the page
    if 'cq_ngo_choices' not in player.participant.vars:
        choices = ['Language instruction and job placement',
                   'Tax advice and loans',
                   'Free meals and clothing',
                   'Housing subsidies']
        random.shuffle(choices)
        player.participant.vars['cq_ngo_choices'] = choices
    return player.participant.vars['cq_ngo_choices']

def cq_group_error_message(player, value):
    if value != 'Immigrants with little education':
        return "This is not the correct answer. Please read and select again."

def cq_challenge_error_message(player, value):
    if value != 'Difficulty finding stable jobs':
        return "This is not the correct answer. Please read and select again."

def cq_ngo_error_message(player, value):
    if value != 'Language instruction and job placement':
        return "This is not the correct answer. Please read and select again."

def make_image_data(image_names):
    return [dict(name=name, path='Memory test question/{}'.format(name)) for name in image_names]

# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment assignment
    task = models.StringField()

    # Comprehension check question
    cq_group = models.StringField(
        label='Which group is mentioned as facing barriers to securing stable jobs?',
        widget=widgets.RadioSelect,
    )
    cq_challenge = models.StringField(
        label='What challenge do immigrants with little education often face?',
        widget=widgets.RadioSelect,
    )
    cq_ngo = models.StringField(
        label='What types of assistance do nonprofit employment programs offer from the text you just read?',
        widget=widgets.RadioSelect,
    )

    # Memory test question
    memory_choice = models.StringField()
    memory_confidence = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7]
    )

    # Demographic variables
    age = models.IntegerField(
        label='Enter your age. (Please leave this blank if you prefer not to say.)',
        blank=True
    )
    gender = models.StringField(
        widget=widgets.RadioSelect,
        label='Identify your gender',
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say']
    )
    education = models.StringField(
        widget=widgets.RadioSelect,
        label='Enter your highest education level',
        choices=['No formal education', 'Primary school', 'Secondary school',
                 'University', 'Postgraduate', 'Prefer not to say']
    )
    stand = models.StringField(
        widget=widgets.RadioSelect,
        label='On a scale of 1 to 7, where would you place yourself politically?',
        choices=['1 (Far Left)', '2 (Left)', '3 (Center-Left)', '4 (Central)',
                 '5 (Center-Right)', '6 (Right)', '7 (Far Right)']
    )
    party = models.StringField(
        widget=widgets.RadioSelect,
        label='Which political party do you most closely identify with or support?',
        choices=['Democratic Party', 'Republican Party', 'Other (please describe if you wish)',
                 'I do not support any party', 'Prefer not to say']
    )
    party_other = models.StringField(
        label="Please describe if you wish",
        blank=True,
    )

# PAGES
class Introduction(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'stand',
                   'party', 'party_other']


class Narrative1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.task == 'simple_hope' or player.task == 'simple_unhope')

    form_model = 'player'
    form_fields = ['cq_group', 'cq_challenge', 'cq_ngo']


class Narrative2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (player.task == 'complex_hope' or player.task == 'complex_unhope')

    form_model = 'player'
    form_fields = ['cq_group', 'cq_challenge', 'cq_ngo']


class Memory(Page):
    form_model = 'player'
    form_fields = ['memory_choice', 'memory_confidence']

    @staticmethod
    def vars_for_template(player: Player):
        image_names = [
            'img1.JPG', 'img2.JPG', 'img3.JPG', 'img4.JPG',
        ]
        random.shuffle(image_names)
        return dict(image_data=make_image_data(image_names))


class ProlificCompletion(Page):
    pass



page_sequence = [
    Introduction,
    Demographics,
    Narrative1,  # simple narrative
    Narrative2,  # complex narrative
    Memory,
    ProlificCompletion
]