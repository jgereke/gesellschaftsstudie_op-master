from otree.api import (
    models, widgets, BaseConstants, BaseSubsession,
    BaseGroup, BasePlayer, Currency as c, currency_range,
)

from otree import forms
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.autodetector import MigrationAutodetector
from django.utils import timezone
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator
from django import forms
from django.conf import settings

from os import listdir
import os, json, random
from os.path import isfile, join

from multiselectfield import MultiSelectField

import random
import numpy as np
import itertools

author = 'Johanna Gereke, Max Schaub, Philipp Chapkovski'

doc = """
Gesellschaftsstudie
"""


class Constants(BaseConstants):
    name_in_url = 'gss'
    players_per_group = None
    num_rounds = 1
    contactplaces = (
            (1,'auf der Arbeit'),
            (2,'auf der Straße/im öffentlichen Raum'),
            (3,'in der Schule meiner Kinder'),
            (4,'im Verein'),
            (5,'als Freiwilliger'),
            (6,'bei offiziellen Treffen'),
            (7,'anderswo')
            )


# block randomization of pages
class Subsession(BaseSubsession):
    def creating_session(self):
        from .pages import initial_page_sequence
        aaa = [i.__name__.split('_') for i in initial_page_sequence]
        page_blocks = [list(group) for key, group in itertools.groupby(aaa, key=lambda x: x[0])]
        for p in self.get_players():
            pb=page_blocks.copy()
            random.shuffle(pb)
            level1 = list(itertools.chain.from_iterable(pb))
            level2 = ['_'.join(i) for i in level1]
            p.page_sequence = json.dumps(level2)


class Group(BaseGroup):

    selected_individual_task = models.PositiveIntegerField()
    selected_pgg = models.PositiveIntegerField


class Player(BasePlayer):
    page_sequence=models.StringField()
    # mobile or desktop PC
    mobile_user = models.StringField()

    #timers
    starttime = models.DateTimeField()
    endtime =  models.DateTimeField()

    immi_first = models.StringField()
    man_woman_first_pic = models.StringField()
    man_woman_second_pic = models.StringField()
    headscarf_first_pic = models.StringField()
    immi_left_right = models.StringField()
    headscarf_split = models.StringField()
    first_pic = models.StringField()
    second_pic = models.StringField()
    third_pic = models.StringField()
    fourth_pic = models.StringField()
    first_name = models.StringField()
    second_name = models.StringField()
    third_name = models.StringField()
    fourth_name = models.StringField()
    first_age = models.StringField()
    second_age = models.StringField()
    third_age = models.StringField()
    fourth_age = models.StringField()
    first_bl = models.StringField()
    second_bl = models.StringField()
    third_bl = models.StringField()
    fourth_bl = models.StringField()

    newsprime = models.StringField()
    afd_first = models.BooleanField()


    def set_prime(self):
        self.newsprime= random.choice(['yes','no'])
        self.afd_first= False

    def set_picture_order(self):

        gM1 = 'pictures/MD1_Stefan.png'
        gM2 = 'pictures/MD2_Felix.png'
        gW1 = 'pictures/WD1_Leni.png'
        gW2 = 'pictures/WD2_Marina.png'
        iM1 = 'pictures/MI1_Hooman.png'
        iM2 = 'pictures/MI2_Mostafa.png'
        iW1 = 'pictures/WI1_Bouba.png'
        iW2 = 'pictures/WI2_Esra.png'
        iW1hs = 'pictures/WH1_Bouba.png'
        iW2hs = 'pictures/WH2_Esra.png'

        names_dict = dict(
            [
                (gM1, 'Nico'),
                (gM2, 'Sven'),
                (gW1, 'Conny'),
                (gW2, 'Saskia'),
                (iM1, 'Ali'),
                (iM2, 'Mohammed'),
                (iW1, 'Farida'),
                (iW2, 'Özlem'),
                (iW1hs, 'Farida'),
                (iW2hs, 'Özlem'),
                ]
                )

        age_dict = dict(
            [
                (gM1, '29'),
                (gM2, '31'),
                (gW1, '33'),
                (gW2, '34'),
                (iM1, '35'),
                (iM2, '32'),
                (iW1, '34'),
                (iW2, '33'),
                (iW1hs, '34'),
                (iW2hs, '33'),
                ]
                )

        # set random order
        self.immi_first = random.choice(['yes','no'])
        self.man_woman_first_pic = random.choice(['man','woman'])
        self.man_woman_second_pic = random.choice(['man','woman'])
        self.headscarf_first_pic = random.choice(['yes','no'])

        # select first and second pic
        if self.immi_first == 'no':
            if self.man_woman_first_pic == 'man':
                self.first_pic = random.choice([gM1,gM2])
            elif self.man_woman_first_pic == 'woman':
                self.first_pic = random.choice([gW1,gW2])
        # second picture
            if self.man_woman_second_pic == 'man':
                self.second_pic = random.choice([iM1,iM2])
            else:
                if self.headscarf_first_pic == 'no':
                    self.second_pic = random.choice([iW1,iW2])
                elif self.headscarf_first_pic == 'yes':
                    self.second_pic = random.choice([iW1hs,iW2hs])

        elif self.immi_first == 'yes':
        # first picture
            if self.man_woman_first_pic == 'man':
                self.first_pic = random.choice([iM1,iM2])
            else:
                if self.headscarf_first_pic == 'no':
                    self.first_pic = random.choice([iW1,iW2])
                elif self.headscarf_first_pic == 'yes':
                    self.first_pic = random.choice([iW1hs,iW2hs])
        # second picture
            if self.man_woman_second_pic == 'man':
                self.second_pic = random.choice([gM1,gM2])
            if self.man_woman_second_pic == 'woman':
                self.second_pic = random.choice([gW1,gW2])

        # third and fourth pictures
        self.immi_left_right= random.choice(['left','right'])
        self.headscarf_split = random.choice(['yes','no'])
        choicelist = [self.first_pic, self.second_pic]
        glist = [gM1,gM2,gW1,gW2]
        glistleft = [x for x in glist if x not in choicelist]
        gmlist = [gM1,gM2]
        gwlist = [gW1,gW2]
        imlist = [iM1,iM2]
        imlistleft = [x for x in imlist if x not in choicelist]
        iwlist = [iW1,iW2]
        iwlistleft = [x for x in iwlist if x not in choicelist]
        iwhslist = [iW1hs,iW2hs]
        iwhslistleft = [x for x in iwhslist if x not in choicelist]

        if self.immi_left_right == 'right':
            # Third picture choice of leftover native profiles
            self.third_pic = random.choice(glistleft)
            # if a native man is chosen, choose immigrant man
            if self.third_pic in gmlist:
                self.fourth_pic = random.choice(imlistleft)
            # if a native woman is chosen, choose immigrant woman, either with our without headscarf
            elif  self.third_pic in gwlist:
                if self.headscarf_split == 'no':
                    self.fourth_pic = random.choice(iwlistleft)
                elif self.headscarf_split == 'yes':
                    self.fourth_pic = random.choice(iwhslistleft)

        elif self.immi_left_right == 'left':
            self.fourth_pic = random.choice(glistleft)
            if self.fourth_pic in gmlist:
                self.third_pic = random.choice(imlistleft)
            elif  self.fourth_pic in gwlist:
                if self.headscarf_split == 'no':
                    self.third_pic = random.choice(iwlistleft)
                elif self.headscarf_split == 'yes':
                    self.third_pic = random.choice(iwhslistleft)

        # set names
        self.first_name = names_dict[self.first_pic]
        self.second_name = names_dict[self.second_pic]
        self.third_name = names_dict[self.third_pic]
        self.fourth_name = names_dict[self.fourth_pic]

         # set ages
        self.first_age= age_dict[self.first_pic]
        self.second_age = age_dict[self.second_pic]
        self.third_age = age_dict[self.third_pic]
        self.fourth_age = age_dict[self.fourth_pic]

         # set BL
        self.first_bl = random.choice(['Brandenburg','Mecklenburg-Vorpommern','Sachsen','Sachsen-Anhalt','Thüringen'])
        self.second_bl = random.choice(['Brandenburg','Mecklenburg-Vorpommern','Sachsen','Sachsen-Anhalt','Thüringen'])
        self.third_bl = random.choice(['Brandenburg','Mecklenburg-Vorpommern','Sachsen','Sachsen-Anhalt','Thüringen'])
        self.fourth_bl = random.choice(['Brandenburg','Mecklenburg-Vorpommern','Sachsen','Sachsen-Anhalt','Thüringen'])


    dec_dg1 = models.PositiveIntegerField(choices=[
          [0,'0,00€'],
          [1,'0,50€'],
          [2,'1,00€'],
          [3,'1,50€'],
          [4,'2,00€'],
          [5,'2,50€'],
          [6,'3,00€'],
          [7,'3,50€'],
          [8,'4,00€'],
          [9,'4,50€'],
          [10,'5,00€'],
          ],
          widget=widgets.RadioSelectHorizontal(),
          )


    dec_dg2 = models.PositiveIntegerField(choices=[
          [0,'0,00€'],
          [1,'0,50€'],
          [2,'1,00€'],
          [3,'1,50€'],
          [4,'2,00€'],
          [5,'2,50€'],
          [6,'3,00€'],
          [7,'3,50€'],
          [8,'4,00€'],
          [9,'4,50€'],
          [10,'5,00€'],
          ],
          widget=widgets.RadioSelectHorizontal(),
          )

    dec_tg1 = models.PositiveIntegerField(choices=[
          [0,'0,00€'],
          [1,'0,50€'],
          [2,'1,00€'],
          [3,'1,50€'],
          [4,'2,00€'],
          [5,'2,50€'],
          [6,'3,00€'],
          [7,'3,50€'],
          [8,'4,00€'],
          [9,'4,50€'],
          [10,'5,00€'],
          ],
          widget=widgets.RadioSelect(),
          )

    dec_tg2 = models.PositiveIntegerField(choices=[
          [0,'0,00€'],
          [1,'0,50€'],
          [2,'1,00€'],
          [3,'1,50€'],
          [4,'2,00€'],
          [5,'2,50€'],
          [6,'3,00€'],
          [7,'3,50€'],
          [8,'4,00€'],
          [9,'4,50€'],
          [10,'5,00€'],
          ],
          widget=widgets.RadioSelect(),
          )

    dec_split = models.PositiveIntegerField(min=0, max=10)

    po_dg1 = models.DecimalField(max_digits=5, decimal_places=2)
    po_dg1_shown = models.StringField()
    po_dg2 = models.DecimalField(max_digits=5, decimal_places=2)
    po_dg2_shown = models.StringField()
    po_tg1 = models.DecimalField(max_digits=5, decimal_places=2)
    po_tg1_shown = models.StringField()
    tg1_multifac = models.DecimalField(max_digits=5, decimal_places=2)
    po_tg2 = models.DecimalField(max_digits=5, decimal_places=2)
    po_tg2_shown = models.StringField()
    tg2_multifac = models.DecimalField(max_digits=5, decimal_places=2)

    dec_dg1_shown = models.StringField()
    dec_dg2_shown = models.StringField()
    dec_tg1_shown = models.StringField()
    dec_tg2_shown = models.StringField()

    tg1_sentback_shown = models.StringField()
    tg2_sentback_shown = models.StringField()

    final_payoff = models.DecimalField(max_digits=5, decimal_places=2)
    final_payoff_shown = models.StringField()

    dec_excluded = models.PositiveIntegerField(choices=[
        [1, 'Entscheidungssituation 1'],
        [2, 'Entscheidungssituation 2'],
        [3, 'Entscheidungssituation 3'],
        [4, 'Entscheidungssituation 4'],
        ],
        )

    def calculate_payoffs(self):
        self.po_dg1 = 5 - float(self.dec_dg1)/2
        self.po_dg1_shown = "{:.2f}".format(self.po_dg1).replace('.',',')
        self.po_dg2 = 5 - float(self.dec_dg2)/2
        self.po_dg2_shown = "{:.2f}".format(self.po_dg2).replace('.',',')

        # TG payoff calculation. Expression below chooses multiplication factor according to distribution in SOEP trust game (Fehr 2002)
        self.tg1_multifac = np.random.choice([0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1],
        p=[0.159,0.027,0.053,0.049,0.054,0.352,0.059,0.031,0.029,0.029,0.158])
        # payoff = amount left (recorded numbers are twice indicated amount) + double amount times multiplication factor
        po_tg1_prelim = (5-float(self.dec_tg1)/2) + float(self.dec_tg1)*float(self.tg1_multifac)
        # round to .5
        self.po_tg1 = .5*round(float(po_tg1_prelim)/.5)
        self.po_tg1_shown = "{:.2f}".format(self.po_tg1).replace('.',',')
        tg1_sentback = self.po_tg1 - (5-float(self.dec_tg1)/2)
        self.tg1_sentback_shown = "{:.2f}".format(tg1_sentback).replace('.',',')

        self.tg2_multifac = np.random.choice([0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1],
        p=[0.159,0.027,0.053,0.049,0.054,0.352,0.059,0.031,0.029,0.029,0.158])
        po_tg2_prelim = (5-float(self.dec_tg2)/2) + float(self.dec_tg2)*float(self.tg2_multifac)
        self.po_tg2 = .5*round(float(po_tg2_prelim)/.5)
        self.po_tg2_shown = "{:.2f}".format(self.po_tg2).replace('.',',')
        tg2_sentback = self.po_tg2 - (5-float(self.dec_tg2)/2)
        self.tg2_sentback_shown = "{:.2f}".format(tg2_sentback).replace('.',',')

        # displayed game decisions
        dec_dg1_prelim = float(self.dec_dg1)/2
        self.dec_dg1_shown = "{:.2f}".format(dec_dg1_prelim).replace('.',',')
        dec_dg2_prelim = float(self.dec_dg2)/2
        self.dec_dg2_shown = "{:.2f}".format(dec_dg2_prelim).replace('.',',')
        dec_tg1_prelim = float(self.dec_tg1)/2
        self.dec_tg1_shown = "{:.2f}".format(dec_tg1_prelim).replace('.',',')
        dec_tg2_prelim = float(self.dec_tg2)/2
        self.dec_tg2_shown = "{:.2f}".format(dec_tg2_prelim).replace('.',',')

        # calculate final payoff, excluding one decision
        if self.dec_excluded == 1:
            final_payoff_prelim = float(self.po_tg1) + float(self.po_tg2) + float(self.po_dg2)
        elif  self.dec_excluded == 2:
            final_payoff_prelim = float(self.po_dg1) + float(self.po_tg2) + float(self.po_dg2)
        elif  self.dec_excluded == 3:
            final_payoff_prelim = float(self.po_dg1) + float(self.po_tg1) + float(self.po_dg2)
        elif  self.dec_excluded == 4:
            final_payoff_prelim = float(self.po_dg1) + float(self.po_tg1) + float(self.po_tg2)

        if final_payoff_prelim < 10:
            self.final_payoff = 10
        elif final_payoff_prelim >20:
            self.final_payoff = 20
        else:
            self.final_payoff = final_payoff_prelim

        self.final_payoff_shown = "{:.2f}".format(self.final_payoff).replace('.',',')


    # demographics

    gender = models.StringField(choices=['Weiblich', 'Männlich'])

    age = models.PositiveIntegerField(min=18, max=99)

    married = models.PositiveIntegerField(choices=[
        [1, 'Verheiratet und leben mit Ehepartner zusammen'],
        [2, 'Nicht verheiratet aber in fester Lebensgemeinschaft'],
        [3, 'Verheiratet und leben getrennt'],
        [4, 'Verwitwet'],
        [5, 'Geschieden'],
        [6, 'Ledig'],
        ],
        )

    children = models.PositiveIntegerField(choices=[
        [1,'Nein'],
        [2,'Ja, 1 Kind'],
        [3,'Ja, 2 Kinder'],
        [4,'Ja, 3 Kinder oder mehr'],
        ],
        )

    household = models.PositiveIntegerField(choices=[
        [1,'Nein, lebe allein'],
        [2,'Ja, noch 1 andere Person'],
        [3,'Ja, noch 2 andere Personen'],
        [4,'Ja, noch 3 andere Personen'],
        [5,'Ja, mehr als 3 andere Personen'],
        ],
        )

    bundesland = models.PositiveIntegerField(choices=[
        [1,'Baden-Württemberg'],
        [2,'Bayern'],
        [3,'Berlin'],
        [4,'Bremen'],
        [5,'Brandenburg'],
        [6,'Hamburg'],
        [7,'Hessen'],
        [8,'Mecklenburg-Vorpommern'],
        [9,'Niedersachsen'],
        [10,'Nordrhein-Westfalen'],
        [11,'Rheinland-Pfalz'],
        [12,'Saarland'],
        [13,'Sachsen'],
        [14,'Sachsen-Anhalt'],
        [15,'Schleswig-Holstein'],
        [16,'Thüringen'],

        ],
        )

    village = models.StringField()

    residencetime = models.PositiveIntegerField(choices=[
        [1, 'weniger als 1 Jahr'],
        [2, '1-3 Jahren'],
        [3, '4-10 Jahren'],
        [4, 'seit mehr 10 oder mehr Jahren'],
        ],
        )

    neighborsmovingout = models.PositiveIntegerField(choices=[
        [1, 'Keine Nachbarn sind weggezogen'],
        [2, '1-3 Nachbarn sind weggezogen'],
        [3, '4-10 Nachbarn sind weggezogen'],
        [4, '11 oder mehr  Nachbarn sind weggezogen'],
        [999,'weiß nicht/ keine Angabe']
        ],
        )

    neighborsmovingin = models.PositiveIntegerField(choices=[
        [1, 'Keine Nachbarn sind hergezogen'],
        [2, '1-3 Nachbarn sind hergezogen'],
        [3, '4-10 Nachbarn sind hergezogen'],
        [4, '11 oder mehr  Nachbarn sind hergezogen'],
        [999,'weiß nicht/ keine Angabe']
        ],
        )

    election = models.PositiveIntegerField(choices=[
        [1, 'ja, habe gewählt '],
        [2, 'nein, habe nicht gewählt'],
        ],
        )

    party = models.PositiveIntegerField(choices=[
        [1, 'CDU'],
        [2, 'SPD'],
        [3, 'DIE LINKE'],
        [4, 'AfD'],
        [5, 'FDP'],
        [6, 'DIE GRÜNEN'],
        [7, 'NPD '],
        [8, 'andere Partei'],
        ],
        )

    partyif = models.PositiveIntegerField(choices=[
        [1, 'CDU'],
        [2, 'SPD'],
        [3, 'DIE LINKE'],
        [4, 'AfD'],
        [5, 'FDP'],
        [6, 'DIE GRÜNEN'],
        [7, 'NPD '],
        [8, 'andere Partei'],
        ],
        )

    afd = models.PositiveIntegerField(choices=[
        [1, '-5, halte überhaupt nichts von dieser Partei'],
        [2, '-4'],
        [3, '-3'],
        [4, '-2'],
        [5, '-1'],
        [6, '0'],
        [7, '+1'],
        [8, '+2'],
        [9, '+3'],
        [10, '+4'],
        [11, '+5, halte sehr viel von dieser Partei'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    manipulationcheck = models.PositiveIntegerField(choices=[
        [1,'1, entsprechen gar nicht meiner persönlichen Wahrnehmung'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7, entsprechen voll meiner persönlichen Wahrnehmung'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    petition = models.PositiveIntegerField(choices=[
        [1,'1, lehne die Petition völlig ab'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7'],
        [8,'8'],
        [9,'9'],
        [10,'10'],
        [11,'11, unterstütze die Petition voll und ganz'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    populism1 = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    populism2 = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    nationalism1 = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    nationalism2 = models.PositiveIntegerField(choices=[
        [1,'Sehr zufrieden'],
        [2,'Zufrieden'],
        [3,'Teils zufrieden/teils unzufrieden'],
        [4,'Unzufrieden'],
        [5,'Sehr unzufrieden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    nationalism3 = models.PositiveIntegerField(choices=[
        [1,'überhaupt nicht stolz'],
        [2,'nicht sehr stolz'],
        [3,'ziemlich stolz'],
        [4,'sehr stolz'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    rightwing1 = models.PositiveIntegerField(choices=[
        [1,'1, stimme überhaupt nicht zu'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7, stimme voll und ganz zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    rightwing2 = models.PositiveIntegerField(choices=[
        [1,'1, stimme überhaupt nicht zu'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7, stimme voll und ganz zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    authoritarian1 = models.PositiveIntegerField(choices=[
        [1,'Unabhängigkeit'],
        [2,'Achtung vor älteren Menschen '],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    authoritarian2 = models.PositiveIntegerField(choices=[
        [1,'Neugier'],
        [2,'Gutes Benehmen'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )
    authoritarian3 = models.PositiveIntegerField(choices=[
        [1,'Gehorsam'],
        [2,'Eigenständigkeit'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    authoritarian4 = models.PositiveIntegerField(choices=[
        [1,'Rücksichtsvoll'],
        [2,'Wohlerzogen'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    immposi1 = models.PositiveIntegerField(choices=[
        [1,'1, stimme überhaupt nicht zu'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7, stimme voll und ganz zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    immposi2 = models.PositiveIntegerField(choices=[
        [1,'1, stimme überhaupt nicht zu'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7, stimme voll und ganz zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )


    attdiff1 = models.PositiveIntegerField(choices=[
        [1,'Der Zuzug soll uneingeschränkt möglich sein'],
        [2,'Der Zuzug soll begrenzt werden'],
        [3,'Der Zuzug soll völlig unterbunden werden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    attdiff2 = models.PositiveIntegerField(choices=[
        [1,'Der Zuzug soll uneingeschränkt möglich sein'],
        [2,'Der Zuzug soll begrenzt werden'],
        [3,'Der Zuzug soll völlig unterbunden werden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    attdiff3 = models.PositiveIntegerField(choices=[
        [1,'Der Zuzug soll uneingeschränkt möglich sein'],
        [2,'Der Zuzug soll begrenzt werden'],
        [3,'Der Zuzug soll völlig unterbunden werden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    attdiff4 = models.PositiveIntegerField(choices=[
        [1,'Der Zuzug soll uneingeschränkt möglich sein'],
        [2,'Der Zuzug soll begrenzt werden'],
        [3,'Der Zuzug soll völlig unterbunden werden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
    )

    asyl_compete = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Stimme eher nicht zu'],
        [4,'Stimme überhaupt nicht zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    asyl_deport = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    asyl_diverse = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    asyl_protect = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    percentageforeignbula = models.StringField(blank = True)

    percentageforeignvillage = models.PositiveIntegerField(choices=[
        [1,'Nein, es gibt keine.'],
        [2,'ca. 1-10 Einzelpersonen'],
        [3,'ca. 11-50 Einzelpersonen'],
        [4,'ca. 51-100 Einzelpersonen'],
        [5,'101-199 Einzelpersonen'],
        [6,'Mehr als 200 Einzelpersonen'],
        [6,'Mehr als 1000 Einzelpersonen'],
        ],
        )

    aquaintances = models.PositiveIntegerField(choices=[
        [1,'niemand'],
        [2,'1-3'],
        [3,'4-5'],
        [4,'mehr als 5'],
        ],
        )

    aquaintancesrefugees = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [3, 'Teilweise'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    refugees = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    contactrefugees = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    contactrefugeesplace = MultiSelectField(
        choices=Constants.contactplaces,
        blank=True,
        )

    supportrefugees1 = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    supportrefugees2 = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    againstrefugees = models.PositiveIntegerField(choices=[
        [1, 'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    understandcontraref = models.PositiveIntegerField(choices=[
       [1,'Ja, habe volles Verständnis'],
       [2,'Ja, habe etwas Verständnis'],
       [3,'Nein, habe kein Verständnis'],
       [4,'Nein, überhaupt kein Verständnis'],
       [999,'weiß nicht/ keine Angabe'],
       ],
       )

    understandproref = models.PositiveIntegerField(choices=[
       [1,'Ja, habe volles Verständnis'],
       [2,'Ja, habe etwas Verständnis'],
       [3,'Nein, habe kein Verständnis'],
       [4,'Nein, überhaupt kein Verständnis'],
       [999,'weiß nicht/ keine Angabe'],
       ],
       )


    feelingforeign = models.PositiveIntegerField(choices=[
       [1,'Stimme völlig zu'],
       [2,'Stimme überwiegend zu'],
       [3,'Lehne überwiegend ab'],
       [4,'Lehne völlig ab'],
       [999,'weiß nicht/ keine Angabe'],
       ],
       )

    politicians = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    splitcommunity = models.PositiveIntegerField(choices=[
         [1,'Ja'],
         [2,'Nein'],
         [999,'weiß nicht/ keine Angabe'],
         ],
         )


    sympathy  = models.PositiveIntegerField(choices=[
        [1,'Sehr viel'],
        [2,'Eher viel'],
        [3,'Eher wenig'],
        [4,'Wenig '],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    fearalone  = models.PositiveIntegerField(choices=[
        [1,'Ja, gibt es hier'],
        [0,'Nein, gibt es hier nicht'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    feartheft = models.PositiveIntegerField(choices=[
        [1,'Höchst wahrscheinlich'],
        [2,'Eher wahrscheinlich'],
        [3,'Wahrscheinlich'],
        [4,'Eher unwahrscheinlich'],
        [5,'Völlig unwahrscheinlich'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    fearviolence = models.PositiveIntegerField(choices=[
        [1,'Höchst wahrscheinlich'],
        [2,'Eher wahrscheinlich'],
        [3,'Wahrscheinlich'],
        [4,'Eher unwahrscheinlich'],
        [5,'Völlig unwahrscheinlich'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    ownfinancial = models.PositiveIntegerField(choices=[
        [1,'Schlecht'],
        [2,'Weniger gut'],
        [3,'Gut'],
        [4,'Sehr gut'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    fairshare = models.PositiveIntegerField(choices=[
        [1,'Erhalte sehr viel weniger als gerechten Anteil'],
        [2,'Erhalte etwas weniger als gerechten Anteil'],
        [3,'Erhalte gerechten Anteil'],
        [4,'Erhalte etwas mehr als gerechten Anteil'],
        [5,'Erhalte sehr viel mehr als gerechten Anteil'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    loserside = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    secondclass = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    neighborpoles = models.PositiveIntegerField(choices=[
        [1,'+3: wären mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wären mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    neighborturks = models.PositiveIntegerField(choices=[
        [1,'+3: wären mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wären mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    neighborsyrian = models.PositiveIntegerField(choices=[
        [1,'+3: wären mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wären mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    neighbornigerian = models.PositiveIntegerField(choices=[
        [1,'+3: wären mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wären mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    familypoles = models.PositiveIntegerField(choices=[
        [1,'+3: wäre mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wäre mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    familyturks = models.PositiveIntegerField(choices=[
        [1,'+3: wäre mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wäre mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    familysyrian = models.PositiveIntegerField(choices=[
        [1,'+3: wäre mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wäre mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    familynigerian = models.PositiveIntegerField(choices=[
        [1,'+3: wäre mir sehr angenehm'],
        [2,'+2 '],
        [3,'+1: eher angenehm'],
        [4,' 0: ist mir egal'],
        [5,'-1: eher unangenehm'],
        [6,'-2 '],
        [7,'-3: wäre mir sehr unangenehm'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    muslim1 = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Stimme nicht zu'],
        [4,'Stimme überhaupt nicht zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    muslim2 = models.PositiveIntegerField(choices=[
        [1,'Stimme völlig zu'],
        [2,'Stimme überwiegend zu'],
        [3,'Lehne überwiegend ab'],
        [4,'Lehne völlig ab'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    education = models.PositiveIntegerField(choices=[
        [1,'Schule beendet ohne Abschluss'],
        [2,'Hauptschulabschluss/ Volksschulabschluss'],
        [3,'Realschulabschluss/ Mittlere Reife'],
        [4,'Fachhochschulreife (Abschluss einer Fachoberschule)'],
        [5,'Abitur bzw. Hochschulreife '],
        [6,'noch in der Schule'],
        ],
        )

    employed = models.PositiveIntegerField(choices=[
        [1,'Vollzeit erwerbstätig'],
        [2,'Teilzeit erwerbstätig'],
        [3,'in Ausbildung/Studium'],
        [4,'nicht erwerbstätig'],
        [5,'trifft nicht zu'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    notemployed = models.PositiveIntegerField(choices=[
        [1,'in Rente, Pension oder im Vorruhestand'],
        [2,'Hausfrau/Hausmann'],
        [3,'Mutterschutz/Elternzeit'],
        [4,'arbeitslos (inkl. Ein-Euro-Jobs)'],
        [5,'aus anderen Gründen nicht berufstätig'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    religion = models.PositiveIntegerField(choices=[
        [1,'römisch-katholische Kirche '],
        [2,'evangelisch/protestantische Kirche'],
        [3,'andere Glaubensgemeinschaft'],
        [4,'keine Glaubensgemeinschaft '],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    selfmigrant = models.PositiveIntegerField(choices=[
        [1,'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    selfvertrieben = models.PositiveIntegerField(choices=[
        [1,'Ja'],
        [0,'Nein'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    politics = models.PositiveIntegerField(choices=[
        [1,'sehr stark'],
        [2,'stark'],
        [3,'mittelmäßig'],
        [4,'weniger stark'],
        [5,'überhaupt nicht'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    mainsourcenews = models.PositiveIntegerField(choices=[
        [1, 'Fernsehen'],
        [2, 'Zeitung'],
        [3, 'Radio'],
        [4, 'Internet'],
        [5, 'persönliche Gespräche'],
        [6, 'andere Quelle'],
        ],
        )

    intpoluse = models.PositiveIntegerField(choices=[
        [1, 'gar nicht'],
        [2, '1 Tagen'],
        [3, '2 Tage'],
        [4, '3 Tage'],
        [5, '4 Tage'],
        [6, '5 Tage'],
        [7, '6 Tage'],
        [8, '7 Tage'],
        ],
        )

    opiniondiff = models.PositiveIntegerField(choices=[
        [1, 'Nie'],
        [2, 'Selten'],
        [3, 'Manchmal'],
        [4, 'Oft'],
        [5, 'Immer'],
        ],
        )

    afdsupport = models.PositiveIntegerField(choices=[
         [1, 'Niemand (0%)'],
         [2, 'Ein paar (ca. 10%)'],
         [3, 'Einige (ca. 25%)'],
         [4, 'Ungefähr die Hälfte (ca. 50%)'],
         [5, 'Viele von ihnen (ca. 75%)'],
         [6, 'Alle (100%)'],
         ],
         )


    rightleft = models.PositiveIntegerField(choices=[
        [1,'1, links'],
        [2,'2'],
        [3,'3'],
        [4,'4'],
        [5,'5'],
        [6,'6'],
        [7,'7'],
        [8,'8'],
        [9,'9'],
        [10,'10'],
        [11,'11, rechts'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    mayor = models.StringField(blank = True)


    wallet = models.PositiveIntegerField(choices=[
        [1,'höchst wahrscheinlich'],
        [2,'eher wahrscheinlich'],
        [3,'wahrscheinlich'],
        [4,'eher unwahrscheinlich'],
        [5,'völlig unwahrscheinlich'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    trustneighbor = models.PositiveIntegerField(choices=[
        [1,'sehr stark'],
        [2,'stark'],
        [3,'mittelmäßig'],
        [4,'weniger stark'],
        [5,'überhaupt nicht'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    communitybelonging = models.PositiveIntegerField(choices=[
        [1,'Stark verbunden'],
        [2,'Ziemlich verbunden'],
        [3,'Wenig verbunden'],
        [4,'Gar nicht verbunden'],
        [999,'weiß nicht/ keine Angabe'],
        ],
        )

    housing = models.PositiveIntegerField(choices=[
        [1,'zur Untermiete'],
        [2,'in einer Mietwohnung / in einem gemieteten Haus'],
        [3,'in einer Eigentumswohnung (Eigen- oder Familienbesitz)'],
        [4,'im eigenen Haus (oder dem Haus der Familie)'],
        [5,'Andere Wohnform'],
        ],
        )


    income = models.PositiveIntegerField(min=0, max=100000)

    feedback=   models.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 70}),
        verbose_name="",
        validators=[
            MinLengthValidator(
                10,
                message="Bitte schreiben Sie mindestens 10 Wörter.",
                ),
                ]
    )

    # name =   models.CharField(
    #     widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}),
    #     verbose_name="",
    # )
    #
    # street =   models.CharField(
    #     widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}),
    #     verbose_name="",
    # )
    #
    # town =   models.CharField(
    #     widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}),
    #     verbose_name="",
    # )

    email1 =   models.EmailField()

    email2 =   models.EmailField()
