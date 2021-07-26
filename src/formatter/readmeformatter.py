from operator import itemgetter
import calendar

class ReadmeFormatter():
    def __init__(self, storage):
        self._storage = storage

    def render(self, filepath:str):
        table = '||Track|Date|\n'
        table += '|---|--------|---|\n'
        tracks_sorted = sorted(self._storage.getTracks().values(), key = lambda x: ( str(x['sort_string']), str('counter') ), reverse=True)
        for trackInfo in tracks_sorted:
            trackname = ''
            trackname += ((str(trackInfo['artist']) + ' - ') if trackInfo.get('artist') else '') + trackInfo['title']

            # Add image
            image = ' '
            if trackInfo.get('image'):
                image = '<img src="{url}" />'.format(url = trackInfo['image'])

            link = ' '
            if trackInfo.get('href'):
                link = '[{image}]({url})'.format(url = trackInfo['href'], image = image)

            date = ' '
            if trackInfo.get('date'):
                month_name = (', ' + calendar.month_name[trackInfo['date']['month']]) if isinstance(trackInfo['date']['month'], int) else ''
                date ='<a id="{id}" href="#{id}">'.format(id = trackInfo['sort_string']) + str(trackInfo['date']['year']) + month_name + '</a>'

            table += '|{linkimage}|{trackname}|{date}|\n'.format(
                trackname = trackname,
                linkimage = link,
                date = date
            )

        with open('template/readme_top.md') as readme_top_fp:
            with open(filepath, 'w', encoding='utf8') as fp:
                fp.write(readme_top_fp.read())
                fp.write('\n')
                fp.write(table)
                fp.close()
            readme_top_fp.close()
