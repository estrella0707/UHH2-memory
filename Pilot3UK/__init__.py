from otree.api import *
import itertools
import random

doc = """
Pilot2 on group-thinking and memory (online)
"""


# FUNCTION
def creating_session(subsession):
    import itertools
    task_cycle = itertools.cycle(['hope', 'unhope'])
    for player in subsession.get_players():
        player.task = next(task_cycle)


def likert1(label):
    return models.IntegerField(
        initial=0,
        choices=[[1, ''], [2, ''], [3, ''], [4, ''], [5, '']],
        label=label,
        widget=widgets.RadioSelect)


# PARAMETERS
class C(BaseConstants):
    NAME_IN_URL = 'pt3uk'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # List of petitions
    PETITION = [
        dict(name='research', label="Some call for more publicly funded research (e.g., funded by UKRI) "
                                    "about the potential relation between immigrant status and crime."),
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

    # Screening questions
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

    # Memory test question
    recall = models.IntegerField(choices=range(1, 8))
    memory = models.FloatField(
        label='According to the information slides you read, what is the probability that your household '
              'will experience a burglary in the next 20 years?'
    )

    # Behavioral measurements: intention to share
    share = models.IntegerField(choices=range(1, 8))
    # Behavioral measurements: petitions
    research = models.BooleanField(blank=True, initial=0)
    quota = models.BooleanField(blank=True, initial=0)

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


class Scr(Page):
    form_model = 'player'
    form_fields = ['region', 'propburglary', 'prophealth', 'proplottery', 'propfriend']


class ScreenedOut(Page):
    @staticmethod
    def is_displayed(player: Player):
        # opposite condition
        rate20_thresholds = {
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

        region = player.region
        thresh = rate20_thresholds.get(region)

        return thresh is not None and player.propburglary > thresh


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employ', 'income',
                   'origin_father', 'origin_mother', 'stand',
                   'vote', 'vote_yes', 'vote_no',
                   'worry', 'immi_familiar', 'immi_attitude']


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
            'North East (England)': 'Pilot2UK/Slide3.PNG',
            'North West (England)': 'Pilot2UK/Slide4.PNG',
            'Yorkshire and The Humber (England)': 'Pilot2UK/Slide5.PNG',
            'East Midlands (England)': 'Pilot2UK/Slide6.PNG',
            'West Midlands (England)': 'Pilot2UK/Slide7.PNG',
            'East (England)': 'Pilot2UK/Slide8.PNG',
            'London (England)': 'Pilot2UK/Slide9.PNG',
            'South East (England)': 'Pilot2UK/Slide10.PNG',
            'South West (England)': 'Pilot2UK/Slide11.PNG',
            'Wales': 'Pilot2UK/Slide12.PNG',
        }
        return {
            'image': image.get(player.region),
        }


class Info4(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'hope': 'Pilot2UK/Slide13.PNG',
            'unhope': 'Pilot2UK/Slide15.PNG',
        }
        return {
            'image': image.get(player.task),
        }


class Info5(Page):
    @staticmethod
    def vars_for_template(player):
        # Map treatments to images and their values
        image = {
            'hope': 'Pilot2UK/Slide14.PNG',
            'unhope': 'Pilot2UK/Slide16.PNG',
        }
        return {
            'image': image.get(player.task),
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


class Memory(Page):
    form_model = 'player'
    form_fields = ['memory']


class Recall(Page):
    form_model = 'player'
    form_fields = ['recall']


class NGO(Page):
    form_model = 'player'
    form_fields = ['share']


class Petition(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [petition['name'] for petition in C.PETITION]


class Debrief1(Page):
    pass


class Debrief2(Page):
    pass


class Feedback(Page):
    form_model = 'player'
    form_fields = ['purpose', 'feedback']


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction,
    Scr,  # screening in only those optimistic
    ScreenedOut,  # screen out page
    Demographics,
    AC,  # attention check
    Info1, Info2, Info3, Info4, Info5,  # information slides
    Emotion,  # scare
    Control,  # perceived control
    Memory,  # memory test
    Recall,  # selective recall of consumption
    NGO,  # intention to share information
    Petition,  # choose whether to receive emails
    Debrief1, Debrief2, Feedback, ProlificCompletion,
]