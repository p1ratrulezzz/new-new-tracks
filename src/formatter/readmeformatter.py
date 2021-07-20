from operator import itemgetter
import calendar

class ReadmeFormatter():
    def __init__(self, storage):
        self._storage = storage

    def render(self, filepath:str):
        table = '||Track|Date|\n'
        table += '|---|--------|---|\n'
        tracks_sorted = sorted(self._storage.getTracks().values(), key=itemgetter('counter'))
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
                date = str(trackInfo['date']['year']) + ', ' + calendar.month_name[trackInfo['date']['month']]

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
