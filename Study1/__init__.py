from otree.api import *
import itertools
import random

doc = """
Study 1: the phenomenon
"""


# FUNCTION
def creating_session(subsession):
    treatment_cycle = itertools.cycle(['crime', 'cancer', 'neutral'])
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
    NAME_IN_URL = 's1pt1'
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
    answer = models.IntegerField(blank=True)
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
    region = models.StringField(
        label='Please tell us your region of residence.',
        choices=['North East (England)', 'North West (England)', 'Yorkshire and The Humber (England)',
                 'East Midlands (England)', 'West Midlands (England)', 'East (England)', 'London (England)',
                 'South East (England)', 'South West (England)', 'Wales']
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
    crime_worry = models.IntegerField(choices=range(1, 8))
    cancer_worry = models.IntegerField(choices=range(1, 8))
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
                     'We should keep letting the same number of legal immigrants to come to the UK. '),
                 (5, 'The number of legal immigrants today is not a problem at all. '
                     'We should let even more legal immigrants come to the UK. ')
                 ],
    )

    # Manipulation check question
    control_crime = models.IntegerField(choices=range(1, 8), blank=True)
    control_cancer = models.IntegerField(choices=range(1, 8), blank=True)
    scared = likert1('Scared')
    nervous = likert1('Nervous')
    calm = likert1('Calm')
    relaxed = likert1('Relaxed')
    encouraged = likert1('Encouraged')
    discouraged = likert1('Discouraged')
    angry = likert1('Angry')
    joyful = likert1('Joyful')

    # Attention check question
    aq = models.BooleanField(
        label='',
        choices=[(True, 'Yes, I have devoted full attention to the questions so far and '
                        'I think you should use my responses for your study.'),
                 (False, 'No, I have NOT devoted full attention to the questions so far and '
                         'I think you should NOT use my responses for your study.')],
        widget=widgets.RadioSelect
    )

    # Narrative endorsement
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

    # Feedback
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
    expcancer = models.BooleanField(
        label='Have you or your close family experienced cancer in your life? (Optional)',
        blank=True
    )
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


class ACvideoFail(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.aqvideo != 1


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employ', 'income',
                   'region', 'origin_father', 'origin_mother', 'stand',
                   'crime_worry', 'cancer_worry', 'vote', 'vote_yes', 'vote_no',
                   'immi_familiar', 'immi_attitude']


class Info1(Page):
    @staticmethod
    def vars_for_template(player):
        image = {
            'crime': 'crime/Slide1.JPG',
            'cancer': 'cancer/Slide1.JPG',
            'neutral': 'sunlight/Slide1.JPG'
        }
        return {
            'image': image.get(player.treatment),
        }


class Info2(Page):
    @staticmethod
    def vars_for_template(player):
        image = {
            'crime': 'crime/Slide2.JPG',
            'cancer': 'cancer/Slide2.JPG',
            'neutral': 'sunlight/Slide2.JPG'
        }
        return {
            'image': image.get(player.treatment),
        }


class Info3(Page):
    @staticmethod
    def vars_for_template(player):
        region_slide_mapping = {
            'North East (England)': 'Slide3.JPG',
            'North West (England)': 'Slide4.JPG',
            'Yorkshire and The Humber (England)': 'Slide5.JPG',
            'East Midlands (England)': 'Slide6.JPG',
            'West Midlands (England)': 'Slide7.JPG',
            'East (England)': 'Slide8.JPG',
            'London (England)': 'Slide9.JPG',
            'South East (England)': 'Slide10.JPG',
            'South West (England)': 'Slide11.JPG',
            'Wales': 'Slide12.JPG',
        }

        if player.treatment == 'crime':
            folder = 'crime'
        elif player.treatment == 'cancer':
            folder = 'cancer'
        else:
            folder = 'sunlight'

        slide_name = region_slide_mapping.get(player.region)
        image_path = f"{folder}/{slide_name}" if slide_name else None

        return {
            'image': image_path,
        }


class Emotion(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        import random
        survey = ['scared', 'nervous', 'discouraged', 'encouraged', 'calm',
                  'relaxed', 'angry', 'joyful']
        random.shuffle(survey)
        return survey


class Control(Page):
    form_model = 'player'
    form_fields = ['control_crime', 'control_cancer']


class Postbelief(Page):
    form_model = 'player'
    form_fields = ['post_eu', 'post_noneu']


class Feedback1(Page):
    form_model = 'player'
    form_fields = ['aq', 'purpose', 'feedback', 'AIuse', 'expcrime', 'expcancer']


class Feedback2(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        return [demand['name'] for demand in C.DEMAND]


class Debrief1(Page):
    pass


class Debrief2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.treatment == 'cancer' or player.treatment == 'crime'


class BonusFeedback(Page):
    pass


class ProlificCompletion(Page):
    pass


page_sequence = [
    Introduction, Consent,
    ACvideo,  # video attention check for bot detection
    ACvideoFail,  # dead end for participants who failed the bot check twice
    Demographics,
    Info1, Info2, Info3,   # information slides
    Emotion,  # encourage/discourage
    Control,  # perceived control
    Postbelief,  # post-treatment model belief
    Feedback1, Feedback2,
    Debrief1, Debrief2, ProlificCompletion
]