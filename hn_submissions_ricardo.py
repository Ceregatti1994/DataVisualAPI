import requests
import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

from operator import itemgetter

#Faz uma chamada de API e armazena a resposta
url ='https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code: ",r.status_code)

#Armazena a resposta da API em uma variável
submission_ids = r.json()
submission_dicts = []
names = []
for submission_id in submission_ids[:30]:
    #Cria uma chamada de API separada para cada artigo submetido
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
            str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()
    submission_dict = {
        'value': response_dict.get('descendants', 0),
        'label': str(response_dict['title']),
        'xlink': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        }
    submission_dicts.append(submission_dict)
   

submission_dicts = sorted(submission_dicts, key=itemgetter('value'), reverse=True)

for articles in submission_dicts:
    names.append(articles['label'])

"""
for submission_dict in submission_dicts:
    print("\nTitle:",submission_dict['title'])
    print("Discussion link:",submission_dict['link'])
    print("Comments:",submission_dict['comments'])
"""
#Cria a visualização

my_style = LS('#333366', base_style=LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size =24
my_config.label_font_size =14
my_config.major_label_font_size = 18
my_config.truncate_label = 20
my_config.show_y_guides = False
my_config.width = 1000


chart = pygal.Bar(my_config,style = my_style)
chart.title = str('Top topics on Hacker-News')
chart.x_labels = names

chart.add('', submission_dicts)
chart.render_in_browser()
        