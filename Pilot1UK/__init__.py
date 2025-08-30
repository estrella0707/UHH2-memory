from otree.api import *
import itertools
import random

doc = """
Pilot1 on anticipatory utility and donation (online)
"""


# FUNCTION
def creating_session(subsession):
    # Treatment randomization
    task = itertools.cycle(['simple_hope', 'simple_unhope', 'complex_hope',
                            'complex_unhope', 'control'])
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


def cq_group_error_message(player, value):
    if value != 'Immigrants with little education':
        return "This is not the correct answer. Please read and select again."


def cq_challenge_error_message(player, value):
    if value != 'Difficulty finding stable jobs':
        return "This is not the correct answer. Please read and select again."


def cr1_choices(player):
    choices = ['Social media → Sleep → Mood',
               'Sleep → Mood ← social media',
               'Social media → Mood ← Sleep']
    random.shuffle(choices)
    return choices


def cr2_choices(player):
    choices = ['Air Pollution → Asthma ← Exercise',
               'Exercise → Asthma → Air Pollution',
               'Air Pollution → Exercise → Asthma']
    random.shuffle(choices)
    return choices


def cr3_choices(player):
    choices = ['Eye Strain ← Smartphone Use → Distraction',
               'Eye Strain → Smartphone Use → Distraction',
               'Smartphone Use → Eye Strain → Distraction']
    random.shuffle(choices)
    return choices


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt1uk'
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
    cq_group = models.StringField(label='',widget=widgets.RadioSelect)
    cq_challenge = models.StringField(label='',widget=widgets.RadioSelect)

    # Manipulation check question
    mq_logic = models.IntegerField(choices=range(1, 8))
    mq_language = models.IntegerField(choices=range(1, 8))
    mq_agree = models.IntegerField(choices=range(1, 8))
    control = models.IntegerField(choices=range(1, 8))

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and'
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )

    # Measure of causal reasoning ability
    cr1 = models.StringField(
        label='Which diagram fits this explanation best? ',
        widget=widgets.RadioSelect
    )
    cr2 = models.StringField(
        label='Which diagram fits this explanation best? ',
        widget=widgets.RadioSelect
    )
    cr3 = models.StringField(
        label='Which diagram fits this explanation best? ',
        widget=widgets.RadioSelect
    )

    # Memory test question
    memory = models.IntegerField(choices=range(1, 8))

    # Donation decision
    advisor = models.IntegerField(
        label='',
        choices=[(1, 'Advisor 1: I advise you to support a program that reduces the number of immigrants '
                     'without stable jobs in order to reduce the crime rate.'),
                 (2, 'Advisor 2: I advise you to support a program that help immigrants find employment. ')],
        widget=widgets.RadioSelect
    )
    decision = models.BooleanField(
        label='Would you like to donate?',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=widgets.RadioSelect
    )
    amount = models.FloatField(
        label='How much would you like to donate?',
        min=0,
        max=5
    )

    # Demographic variables
    age = models.IntegerField(
        label='Age (Please leave this blank if you prefer not to say.)',
        blank=True
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
    region = models.StringField(
        label='Region of residence',
        choices=['North East (England)', 'North West (England)', 'Yorkshire and The Humber (England)',
                 'East Midlands (England)', 'West Midlands (England)', 'East (England)', 'London (England)',
                 'South East (England)', 'South West (England)', 'Wales', 'Northern Ireland', 'Prefer not to say']
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
                 '£3,000 – £3,999', '£4,000 – £4,999', '£5,000 – £6,999', '£7,000 – £9,999', 'More than £10,000',
                 'Prefer not to say']
    )
    origin_father = models.StringField(
        label='Where was your father born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'North America', 'South America',
                 'Oceania', 'Prefer not to say']
    )
    origin_mother = models.StringField(
        label='Where was your father born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'North America', 'South America',
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
                 'Liberal Democrat Party', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other (please describe if you wish)', 'Prefer not to say'],
        blank=True,
    )
    vote_yes_other = models.StringField(
        label='Please describe if you wish',
        blank=True,
    )
    vote_no = models.StringField(
        label='Even if you did NOT vote, please indicate the party that you were most likely to have voted '
              'for or who represents your views most closely',
        choices=['Conservative Party', 'Labour Party', 'Democratic Unionist Party', 'Sinn Féin',
                 'Liberal Democrat Party', 'Ukip', 'Green Party', 'Plaid Cymru - Party of Wales', 'Reform UK',
                 'Other (please describe if you wish)', 'Prefer not to say'],
        blank=True,
    )
    vote_no_other = models.StringField(
        label='Please describe if you wish',
        blank=True,
    )
    donation = models.BooleanField(
        widget=widgets.RadioSelect,
        label='In the past 12 months, have you made any financial contributions to a charitable or '
              'nonprofit organization or group?',
        choices=[(True, 'Yes'), (False, 'No')]
    )
    donation_amount = models.FloatField(
        label='Please indicate the amount if you wish',
        blank=True
    )
    worry = models.IntegerField(choices=range(1, 8))
    immi_familiar = models.IntegerField(choices=range(1, 8))
    immi_attitude = models.IntegerField(
        widget=widgets.RadioSelect,
        label='Which of the following statements most closely reflects your view on the number of legal immigrants '
              'from foreign countries who are permitted to come to the United Kingdom to live?',
        choices=[(1, 'The excessive number of legal immigrants today is a very big problem. '
                     'We should ask many legal immigrants to leave the country, '
                     'and we should stop accepting new immigrants.'),
                 (2, 'The number of legal immigrants today is a big problem, '
                     'and we should decrease by a lot the number permitted to come to the U.K. in the future. '),
                 (3, 'The number of legal immigrants today is somewhat of a problem, '
                     'and we should try and decrease a bit the number permitted to come in.'),
                 (4, 'The number of legal immigrants today is not a problem. '
                     'We should keep letting in the same number of immigrants each year as until now. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come live in the U.K. and '
                     'increase the number that is permitted to come every year. ')
                 ],
    )


# PAGES
class Introduction(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'region', 'employ', 'income',
                   'origin_father', 'origin_mother', 'stand',
                   'vote', 'vote_yes', 'vote_yes_other', 'vote_no', 'vote_no_other',
                   'donation', 'donation_amount', 'worry', 'immi_familiar', 'immi_attitude']


class AC(Page):
    form_model = 'player'
    form_fields = ['aq']


class CR(Page):
    form_model = 'player'
    form_fields = ['cr1', 'cr2', 'cr3']


class Nar(Page):
    form_model = 'player'
    form_fields = ['cq_group', 'cq_challenge',
                   'mq_logic', 'mq_language', 'mq_agree']


class Info1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'simple_hope': 'Pilot1UK/UK(Hopeful)_01.png',
            'simple_unhope': 'Pilot1UK/UK(Unhopeful)_01.png',
            'complex_hope': 'Pilot1UK/UK(Hopeful)_01.png',
            'complex_unhope': 'Pilot1UK/UK(Unhopeful)_01.png',
        }
        return {
            'image': image.get(player.task),
        }


class Info2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'simple_hope': 'Pilot1UK/UK(Hopeful)_02.png',
            'simple_unhope': 'Pilot1UK/UK(Unhopeful)_02.png',
            'complex_hope': 'Pilot1UK/UK(Hopeful)_02.png',
            'complex_unhope': 'Pilot1UK/UK(Unhopeful)_02.png',
        }
        return {
            'image': image.get(player.task),
        }


class Info3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'simple_hope': 'Pilot1UK/UK(Hopeful)_03.png',
            'simple_unhope': 'Pilot1UK/UK(Unhopeful)_03.png',
            'complex_hope': 'Pilot1UK/UK(Hopeful)_03.png',
            'complex_unhope': 'Pilot1UK/UK(Unhopeful)_03.png',
        }
        return {
            'image': image.get(player.task),
        }


class Info4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'simple_hope': 'Pilot1UK/UK(Hopeful)_04.png',
            'simple_unhope': 'Pilot1UK/UK(Unhopeful)_04.png',
            'complex_hope': 'Pilot1UK/UK(Hopeful)_04.png',
            'complex_unhope': 'Pilot1UK/UK(Unhopeful)_04.png',
        }
        return {
            'image': image.get(player.task),
        }


class Info5(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'simple_hope': 'Pilot1UK/UK(Hopeful)_05.png',
            'simple_unhope': 'Pilot1UK/UK(Unhopeful)_05.png',
            'complex_hope': 'Pilot1UK/UK(Hopeful)_05.png',
            'complex_unhope': 'Pilot1UK/UK(Unhopeful)_05.png',
        }
        return {
            'image': image.get(player.task),
        }

    form_model = 'player'
    form_fields = ['control']


class Memory(Page):
    form_model = 'player'
    form_fields = ['memory']


class NGO1(Page):
    form_model = 'player'
    form_fields = ['advisor']


class NGO2(Page):
    pass


class Donation1(Page):
    form_model = 'player'
    form_fields = ['decision']


class Donation2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.decision == True

    form_model = 'player'
    form_fields = ['amount']


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Demographics,
    AC,  # attention check
    CR,  # measure of causal reasoning ability
    Nar,  # narrative treatment
    Info1, Info2, Info3, Info4, Info5,  # information slides
    Memory,  # memory test
    NGO1,  # advisor choice
    NGO2,  # NGO introduction
    Donation1,  # choose whether to donate
    Donation2,  # enter donation amount
    ProlificCompletion
]