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


def memory2_choices(player):
    choices = ['Increasing immigrant employment decreases the crime rate.',
               'The worsening of the economy leads to both an increase in the crime rate and a decrease in immigrant employment.',
               'Increasing immigrant employment improves the economy. Economic improvement decreases the crime rate.',
               'Decreasing the crime rate improves the economy. Economic improvement increases immigrant employment.']
    random.shuffle(choices)
    return choices


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt1uk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # List of petitions
    PETITION = [
        dict(name='research', label="Some call for more publicly funded research (e.g., those funded by UKRI) "
                                    "into the connection between immigrant status and crime."),
        dict(name='language', label="Some advocate for higher language requirements for all immigrants arriving in "
                                    "the UK who are unemployed, in order to make them more employable."),
        dict(name='period', label="Some propose reducing the period that immigrants are permitted to stay in the "
                                  "UK after becoming unemployed."),
        dict(name='quota', label="Some demand lowering the quota of all types of immigrants allowed to enter the UK, "
                                 "EXCEPT those under the Skilled Worker category."),
    ]


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
    afraid = likert1('Afraid')
    scared = likert1('Scared')
    frightened = likert1('Frightened')
    nervous = likert1('Nervous')
    jittery = likert1('Jittery')

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
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
    memory1 = models.IntegerField(choices=range(1, 8))
    memory2 = models.StringField(
        label='Which of the following statements most closely reflects the message of the text?',
        widget=widgets.RadioSelect
    )

    # Behavioral measurements: intention to share
    advisor = models.IntegerField(
        label='',
        choices=[(1, 'Advisor 1: I advise you to support a program that reduces the number of immigrants '
                     'without stable jobs in order to reduce the crime rate.'),
                 (2, 'Advisor 2: I advise you to support a program thats help immigrants find employment. ')],
        widget=widgets.RadioSelect
    )
    share = models.IntegerField(choices=range(1, 8))
    # Behavioral measurements: petitions
    research = models.BooleanField(blank=True, initial=0)
    language = models.BooleanField(blank=True, initial=0)
    period = models.BooleanField(blank=True, initial=0)
    quota = models.BooleanField(blank=True, initial=0)

    # Feedback, for pilot only
    sell = models.BooleanField(
        label='Did you think during the study that we attempted to sell anything to you?',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=widgets.RadioSelect,
        blank=True
    )
    purpose = models.LongStringField(
        label='Do you have any idea about the purpose of this study? If yes, please briefly describe in the text field. (optional)',
        blank=True
    )
    feedback = models.LongStringField(
        label='If you have any other feedback to this study, please leave it here. (optional)',
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
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Latin America',
                 'Oceania', 'Prefer not to say']
    )
    origin_mother = models.StringField(
        label='Where was your mother born?',
        choices=['UK', 'other countries in Europe', 'Africa', 'Asia', 'US or Canada', 'Latin America',
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


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'region', 'employ', 'income',
                   'origin_father', 'origin_mother', 'stand',
                   'vote', 'vote_yes', 'vote_no',
                   'worry', 'immi_familiar', 'immi_attitude']


class AC(Page):
    form_model = 'player'
    form_fields = ['aq']


class CR(Page):
    form_model = 'player'
    form_fields = ['cr1', 'cr2', 'cr3']


class Nar(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

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


class Emotion(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['afraid', 'scared', 'frightened', 'nervous', 'jittery']
        random.shuffle(survey)
        return survey


class Control(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    form_model = 'player'
    form_fields = ['control']


class Memory1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'
    
    form_model = 'player'
    form_fields = ['memory1']


class Memory2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.task != 'control'

    form_model = 'player'
    form_fields = ['memory2']


class NGO1(Page):
    form_model = 'player'
    form_fields = ['advisor']


class NGO2(Page):
    form_model = 'player'
    form_fields = ['share']


class Petition(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [petition['name'] for petition in C.PETITION]


class Feedback(Page):
    form_model = 'player'
    form_fields = ['sell', 'purpose', 'feedback']


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Demographics,
    AC,  # attention check
    CR,  # measure of causal reasoning ability
    Nar,  # narrative treatment
    Info1, Info2, Info3, Info4, Info5,  # information slides
    Emotion,  # scare
    Control,  # perceived control
    Memory1, Memory2,  # memory test
    NGO1, NGO2,  # intention to share information
    Petition,  # choose whether to receive emails
    Feedback,
    ProlificCompletion
]