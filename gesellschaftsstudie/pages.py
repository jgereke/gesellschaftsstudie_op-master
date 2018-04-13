from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page as OPage, WaitPage
from .models import Constants
from django.utils import timezone
import time, random
from datetime import datetime, timedelta
from django.utils.timezone import activate
import json

from django_user_agents.utils import get_user_agent


def vars_for_all_templates(self):
    progress=self.progress()
    return {
        'progressrel':"{0:.2f}".format(progress),
        'progress_round':round(progress)
    }


class Page(OPage):
    # Progress bar
    def progress(self):
        progressrel = self._index_in_pages / self.player.participant._max_page_index * 100

        return progressrel



class abs0_einverstandnis(Page):

    def before_next_page(self):
        self.player.set_picture_order()
        self.player.set_prime()
        self.player.starttime = timezone.now() + timezone.timedelta(hours=1)
        self.player.mobile_user = self.request.user_agent.is_mobile


class abs1_hintergrund(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'married', 'children', 'household']


class abs1_wohnort(Page):
    form_model = 'player'
    form_fields = ['bundesland', 'village', 'residencetime', 'neighborsmovingin', 'neighborsmovingout', 'housing']


class abs1_btw(Page):
    form_model = 'player'
    form_fields = ['election']


class abs1_wahl1(Page):
    def is_displayed(self):
        return self.player.election == 1

    form_model = 'player'
    form_fields = ['party']


class abs1_wahl2(Page):
    def is_displayed(self):
        return self.player.election == 2

    form_model = 'player'
    form_fields = ['partyif']


class abs2_zeitung1(Page):
    def is_displayed(self):
        return self.player.newsprime == 'yes'


class abs2_zeitung2(Page):
    def is_displayed(self):
        return self.player.newsprime == 'yes'

    form_model = 'player'
    form_fields = ['manipulationcheck']


class abs2_parteien(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.afd_first == 1:
            return 'afd',
        else:
            return 'petition',

    def vars_for_template(self):
        return {
            'afd_first': self.player.afd_first,
        }


class abs2_petition(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.afd_first == 0:
            return 'afd',
        else:
            return 'petition',

    def vars_for_template(self):
        return {
            'afd_first': self.player.afd_first,
        }


class abs3_politik(Page):
    form_model = 'player'
    form_fields = ['populism1', 'populism2']


class abs3_deutschland(Page):
    form_model = 'player'
    form_fields = ['nationalism1', 'nationalism2', 'nationalism3']


class abs3_kinder(Page):
    form_model = 'player'
    form_fields = ['authoritarian1', 'authoritarian2', 'authoritarian3', 'authoritarian4']


class abs3_meinung(Page):
    form_model = 'player'
    form_fields = ['immposi1', 'immposi2', 'rightwing1', 'rightwing2']


class abs3_personengruppen(Page):
    form_model = 'player'
    form_fields = ['attdiff1', 'attdiff2', 'attdiff3', 'attdiff4']


class abs3_fluchtlinge(Page):
    form_model = 'player'
    form_fields = ['asyl_compete', 'asyl_deport', 'asyl_diverse', 'asyl_protect']


class abs5_ausland1(Page):
    form_model = 'player'
    form_fields = ['percentageforeignbula', 'percentageforeignvillage', 'aquaintances']


class abs5_ausland2(Page):
    def is_displayed(self):
        return self.player.aquaintances != 1

    form_model = 'player'
    form_fields = ['aquaintancesrefugees']


class abs5_kontakt1(Page):
    form_model = 'player'
    form_fields = ['refugees', 'contactrefugees']


class abs5_kontakt2(Page):
    def is_displayed(self):
        return self.player.contactrefugees == 1

    form_model = 'player'
    form_fields = ['contactrefugeesplace']


class abs5_fluchtlinge1(Page):
    form_model = 'player'
    form_fields = ['supportrefugees1', 'supportrefugees2']

    def get_form_fields(self):
        return ["supportrefugees1",
                "supportrefugees2",
                ]


class abs5_fluchtlinge2(Page):
    form_model = 'player'
    form_fields = ['againstrefugees', 'understandcontraref', 'understandproref']


class abs5_einstellung(Page):
    form_model = 'player'
    form_fields = ['feelingforeign', 'politicians', 'splitcommunity', 'sympathy']


class abs5_sicherheit(Page):
    form_model = 'player'
    form_fields = ['fearalone', 'fearviolence', 'feartheft']


class abs5_situation(Page):
    form_model = 'player'
    form_fields = ['ownfinancial', 'fairshare', 'loserside', 'secondclass']


class abs5_nachbarn(Page):
    form_model = 'player'
    form_fields = ['neighborpoles', 'neighborturks', 'neighborsyrian', 'neighbornigerian']


class abs5_heiraten(Page):
    form_model = 'player'
    form_fields = ['familypoles', 'familyturks', 'familysyrian', 'familynigerian']


class abs5_muslime(Page):
    form_model = 'player'
    form_fields = ['muslim1', 'muslim2']


class abs5_beruf(Page):
    form_model = 'player'
    form_fields = ['education', 'employed']


class abs5_erwerbstatigkeit(Page):
    def is_displayed(self):
        return self.player.employed == 4

    form_model = 'player'
    form_fields = ['notemployed']


class abs5_haushaltseinkommen(Page):
    form_model = 'player'
    form_fields = ['income']


class abs5_religion(Page):
    form_model = 'player'
    form_fields = ['religion']


class abs5_migrationshintergrund(Page):
    form_model = 'player'
    form_fields = ['selfmigrant', 'selfvertrieben']


class abs5_interesse(Page):
    form_model = 'player'
    form_fields = ['politics', 'rightleft', 'mayor']


class abs5_informationen(Page):
    form_model = 'player'
    form_fields = ['mainsourcenews', 'intpoluse', 'opiniondiff', 'afdsupport']


class abs5_vertrauen(Page):
    form_model = 'player'
    form_fields = ['wallet', 'trustneighbor', 'communitybelonging']


class abs4_einleitung(Page):
    pass


class abs4_dg1_einleitung(Page):
    pass


class abs4_dg1_entscheidung(Page):
    form_model = 'player'
    form_fields = ['dec_dg1']

    def vars_for_template(self):
        return {
            'first_pic': self.player.first_pic,
            'first_name': self.player.first_name,
            'first_age': self.player.first_age,
            'first_bl': self.player.first_bl,
        }


class abs4_tg1_einleitung(Page):
    pass


class abs4_tg1_schaubild(Page):
    def vars_for_template(self):
        return {
            'first_pic': self.player.first_pic,
        }


class abs4_tg1_entscheidung(Page):
    form_model = 'player'
    form_fields = ['dec_tg1']

    def vars_for_template(self):
        return {
            'first_pic': self.player.first_pic,
            'first_name': self.player.first_name,
            'first_age': self.player.first_age,
            'first_bl': self.player.first_bl,
        }


class abs4_tg2_einleitung(Page):
    pass


class abs4_tg2_entscheidung(Page):
    form_model = 'player'
    form_fields = ['dec_tg2']

    def vars_for_template(self):
        return {
            'second_pic': self.player.second_pic,
            'second_name': self.player.second_name,
            'second_age': self.player.second_age,
            'second_bl': self.player.second_bl,
        }


class abs4_dg2_einleitung(Page):
    pass


class abs4_dg2_entscheidung(Page):
    form_model = 'player'
    form_fields = ['dec_dg2']

    def vars_for_template(self):
        return {
            'second_pic': self.player.second_pic,
            'second_name': self.player.second_name,
            'second_age': self.player.second_age,
            'second_bl': self.player.second_bl,
        }


class abs4_split_einleitung(Page):
    pass


class abs4_split_entscheidung(Page):
    form_model = 'player'
    form_fields = ['dec_split']

    def error_message(self, values):
        if values['dec_split'] > 10 or values['dec_split'] < 0:
            return 'Bitte geben Sie einen Betrag zwischen 0€ und 10€ an.'

    def vars_for_template(self):
        return {
            'third_pic': self.player.third_pic,
            'fourth_pic': self.player.fourth_pic,
            'third_name': self.player.third_name,
            'fourth_name': self.player.fourth_name,
            'third_age': self.player.third_age,
            'fourth_age': self.player.fourth_age,
            'third_bl': self.player.third_bl,
            'fourth_bl': self.player.fourth_bl,
        }


class abs6_bezahlung1(Page):
    form_model = 'player'
    form_fields = ['dec_excluded']

    def before_next_page(self):
        self.player.calculate_payoffs()


class abs6_bezahlung2(Page):
    def vars_for_template(self):
        return {
            'dec_excluded': self.player.dec_excluded,
            'final_payoff': self.player.final_payoff_shown,
        }


class abs6_adresse(Page):
    form_model = 'player'
    form_fields = ['email1','email2']

    def error_message(self, values):
        if values['email1'] != values['email2']:
            return 'Die zwei E-Mail-Adressen sind nicht identisch. Bitte korrigieren Sie die Eingabe.'


class abs6_ruckmeldung(Page):
    form_model = 'player'
    form_fields = ['feedback']

    def before_next_page(self):
        self.player.endtime = timezone.now() + timezone.timedelta(hours=1)



start_pages = [
    abs0_einverstandnis,
    abs1_hintergrund,
    abs1_wohnort,
    abs1_btw,
    abs1_wahl1,
    abs1_wahl2,
]

end_pages = [abs5_ausland1,
             abs5_ausland2,
             abs5_fluchtlinge1,
             abs5_fluchtlinge2,
             abs5_kontakt1,
             abs5_kontakt2,
             abs5_einstellung,
             abs5_sicherheit,
             abs5_situation,
             abs5_nachbarn,
             abs5_heiraten,
             abs5_muslime,
             abs5_beruf,
             abs5_erwerbstatigkeit,
             abs5_haushaltseinkommen,
             abs5_religion,
             abs5_migrationshintergrund,
             abs5_interesse,
             abs5_informationen,
             abs5_vertrauen,
             abs6_ruckmeldung,
             abs6_bezahlung1,
             abs6_bezahlung2,
             ]

initial_page_sequence = [

    abs2_zeitung1,
    abs2_zeitung2,
    abs2_parteien,
    abs2_petition,
    abs3_politik,
    abs3_deutschland,
    abs3_meinung,
    abs3_kinder,
    abs3_personengruppen,
    abs3_fluchtlinge,
    abs4_einleitung,
    abs4_dg1_einleitung,
    abs4_dg1_entscheidung,
    abs4_tg1_einleitung,
    abs4_tg1_schaubild,
    abs4_tg1_entscheidung,
    abs4_tg2_einleitung,
    abs4_tg2_entscheidung,
    abs4_dg2_einleitung,
    abs4_dg2_entscheidung,
    abs4_split_einleitung,
    abs4_split_entscheidung,

]
page_sequence = [

]


class MyPage(Page):
    def inner_dispatch(self):
        page_seq = int(self.__class__.__name__.split('_')[1])
        page_to_show = json.loads(self.player.page_sequence)[page_seq]
        self.__class__ = globals()[page_to_show]
        return super(globals()[page_to_show], self).inner_dispatch()


for i, _ in enumerate(initial_page_sequence):
    NewClassName = "Page_{}".format(i)
    A = type(NewClassName, (MyPage,), {})
    locals()[NewClassName] = A
    page_sequence.append(locals()[NewClassName])

page_sequence = start_pages + page_sequence + end_pages
