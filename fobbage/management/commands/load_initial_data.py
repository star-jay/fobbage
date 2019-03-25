import environ
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fobbage.quizes.models import Quiz, Round, Question

env = environ.Env()
User = get_user_model()


# USER_SPECS = [
#     {
#         'email': 'oda@university.eu',
#         'password': 'not so safe'
#     }
# ]


# flake8: noqa

QUIZ = {
    'title': 'Momos SuperDuperQuizz',
    'rounds': [
        {
            'title': 'De opwarming',
            'questions': [
                {
                    'text': 'In Bangladesh zijn veel kwekers van gevogelte overgestapt van kippen naar eenden. Waarom?',
                    'correct_answer': 'Eenden drijven tijdens de vele overstromingen',
                },
                {
                    'text': 'Iedereen heeft wel eens een borrelend geluid in zijn/haar buik. Wat is de correcte wetenschappelijke term voor deze geluiden?',
                    'correct_answer': 'Borborygmi',
                },
                {
                    'text': 'Rjukan is een klein stadje in een dal in Noorwegen. In de winter is er echter amper zonlicht omdat de zon achter de bergen is. Wat hebben de inwoners gedaan om ook in de winter zonlicht te hebben? ',
                    'correct_answer': 'Grote spiegels op de heuvels gezet',
                },
                {
                    'text': 'In 1986 werd er op een fetival in Cleveland een grote fundraiser georganiseerd. De fundraiser had helaas een hoop onvoorziene gevolgen waardoor er eigenlijk miljoenen aan schade werd aangericht. Wie/wat veroorzaakte deze schade?',
                    'correct_answer': '1,5 miljoen ballonnen werden opgelaten',
                },
                {
                    'text': 'Name this pokémon!',
                    'correct_answer': 'Trubbish',
                },
                {
                    'text': 'Het amazonewoud heeft op zichzelf niet genoeg fosfor om zo veel planten te ondersteunen. Waar komt dat fosfor vandaan?',
                    'correct_answer': 'Zand van de Sahara',
                },
                {
                    'text': 'Hoe heet de volgende wetmatigheid? "De hoeveelheid energie nodig om leugens te ontkrachten is een orde van magnitudes groter dan de energie nodig om leugens te verspreiden"',
                    'correct_answer': 'Het assymetrische bullshit principe',
                },
                {
                    'text': 'In 1908 barstte de vulkaan Pelé uit op het eiland Martinique? Ludger Sylbaris was 1 van 3 overlevenden uit een stadje van 30000 inwoners. Hoe overleefde hij de vulkaanuitbarsting?',
                    'correct_answer': 'Hij zat in een isoleercel met meters dikke muren',
                },
                {
                    'text': 'Jesse Shipley was een Amerikaanse tiener die overleed in een auto-ongeluk. Waarom waren zijn klasgenoten maanden later opnieuw gechoqueerd?',
                    'correct_answer': 'In een klasuitstap naar het mortuarium vonden ze de hersens van Jesse in een bokaal terug',
                },
                {
                    'text': 'In 1474 werd in Basel, Zwitserland een haan ter dood gebracht. Waarom?',
                    'correct_answer': 'Hij en veroordeeld voor hekserij omdat hij een ei had gelegd',
                }
            ]
        },
        {
            'title': 'Double Trouble',
            'questions': [
                {
                    'text': 'Wie had bijna de rol van "Mace Windu" in Starwars gekregen in plaats van Samuel L. Jackson?',
                    'correct_answer': 'Tupac',
                },
                {
                    'text': 'In 2014 bouwde de Deense geografische overheidsdienst Denemarken na in Minecraft op ware schaal. Wat gebeurde er kort na de bekendmaking?',
                    'correct_answer': 'Spelers deden de boel ontploffen en plantten het vol met Amerikaanse vlaggen',
                },
                {
                    'text': 'De "Habeas Corpus" akte is een rechtsbeginsel dat in de 17e eeuw op een vreemde wijze door stemming aanvaard werd in het britse parlement. Wat was er zo vreemd?',
                    'correct_answer': 'Er werd een dikzak voor 10 stemmen gerekend',
                },
                {
                    'text': 'Geef de naam van deze Pornofilm!',
                    'correct_answer': 'Dawsons Crack',
                },
                {
                    'text': 'Gyromitra esculenta is een dodelijk paddestoel die zelfs na hem te koken niet eetbaar is. Toch is er een manier om hem op te eten, welke?',
                    'correct_answer': 'Tweemaal koken',
                },
                {
                    'text': 'Wat gebeurde er enkele uren nadat deze foto werd getrokken?',
                    'correct_answer': 'De auto ontplofte',
                },
                {
                    'text': 'Het geluid dat vaak in films wordt gehoord bij neerstortende gevechtsvliegtuigen is vals. Hoe maakten deze vliegtuigen dat geluid?',
                    'correct_answer': 'Ze maakten een soort sirene vast aan de onderkant van hun vliegtuig',
                },
                {
                    'text': 'In 1913 verzonden Jesse and Mathilda Beagle een pakketje met de post dat wel heel bijzonder was. Wat verzonden ze?',
                    'correct_answer': 'Hun 8 maand oude baby',
                },
                {
                    'text': 'DisneyWorld heeft een kleur uitgevonden dat overal bij past om bepaalde gebouwen etc... te camoufleren. Hoe heet deze tint??',
                    'correct_answer': 'Go away green',
                },
                {
                    'text': 'Wat is Venustraphobia?',
                    'correct_answer': 'De angst voor mooie vrouwen',
                }
            ]
        },
        {
            'title': 'It takes three baby!',
            'questions': [
                {
                    'text': 'Name this pokémon!',
                    'correct_answer': 'Luvdisc',
                },
                {
                    'text': 'Homely betekent in het Brits: Gastvrij, Down-to-earth. Maar wat betekent het in het Amerikaans?',
                    'correct_answer': 'Lelijk',
                },
                {
                    'text': 'Als Hogwarts wordt aangevallen door Voldemort en zijn leger, laat professor McGonagall de standbeelden tot leven komen. Met welke spreuk doet ze dat',
                    'correct_answer': 'Piertotum Locomotor',
                },
                {
                    'text': 'Porn Parodies strikes again!',
                    'correct_answer': 'Hairy Twatter',
                },
                {
                    'text': 'Wat is "Naki Sumo"',
                    'correct_answer': 'Een festival in Japan waar Sumo worstelaars kleine babys om ter snelst doen wenen',
                },
                {
                    'text': 'BridgeAnne d Avignon, een meisje van twaalf ontdekte iets heel speciaals tijdens haar genetisch onderzoek. Wat ontdekte ze?',
                    'correct_answer': 'Dat 42 Amerikaanse presidenten afstammen van een Engelse koning.',
                },
                {
                    'text': 'Geef het Noorse woord voor ochtenderectie',
                    'correct_answer': 'Morgenbrød',
                },
                {
                    'text': 'Wat hebben de top van een penis, het trommelvlies en het nagelbed van een mens met elkaar gemeen?',
                    'correct_answer': 'Het zijn lichaamsdelen die niet zweten',
                },
                {
                    'text': 'Het boek  Arsène Houssaye’s “Des destinées de l’ame” uit de bibliotheek van Harvard veroorzaakte heel wat ophef in 2014, waarom?',
                    'correct_answer': 'Het is gebonden in de huid van een vrouw',
                },
                {
                    'text': 'Iedereen heeft wel eens een fantastisch idee wanneer men zich in een dronken toestand bevindt. De Duitsers hebben voor zulke ideeen zelfs een apart woord. Welk woord?',
                    'correct_answer': 'Schnapsidee',
                }
            ]
        }
    ]
}


class Command(BaseCommand):
    help = 'Loads initial data for Fobbage'

    def create_superuser_from_env(self):
        """creates a super user if info is in .env file"""
        if env.str('DEFAULT_ADMIN_USERNAME', None) and env.str(
           'DEFAULT_ADMIN_PASSWORD', None):
            self.stdout.write('Create superuser...')
            User.objects.create_superuser(
                username=env.str('DEFAULT_ADMIN_USERNAME'),
                password=env.str('DEFAULT_ADMIN_PASSWORD'),
            )
        else:
            self.stdout.write(
                'No superuser info found in the environment file...')

    def create_quiz(self):
        quiz = Quiz.objects.create(title=QUIZ['title'])
        for r in QUIZ['rounds']:
            round = Round.objects.create(
                quiz=quiz,
                title=r['title'],
            )
            i = 0
            for q in r['questions']:
                i += 1
                Question.objects.create(
                    round=round,
                    text=q['text'],
                    correct_answer=q['correct_answer'],
                    order=i,
                )

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser from env-file')
        self.create_superuser_from_env()
        self.stdout.write('Create first quiz')
        self.create_quiz()
