import web
from gothonweb import map

urls = (
    '/game', 'GameEngine',
    '/', 'Index'
)

app = web.application(urls, globals())

# hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout")

class Index(object):
    
    def GET(self):
    # this is used to "setup" the session with starting values (module.class)
        session.room = map.START
        # seeother() redirects to a new page
        web.seeother("/game")
    
class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)
        else:
            return render.you_died()
                
    def POST(self):
        form = web.input(action=None)
        if session.room and form.action:
            # fixed: changed session.room to room, since go() returns one value, session.room implies two
            room = session.room.go(form.action)
            if room:
                session.room = room
                # alternatively one could return render.show_room(room=session.room)
                return GameEngine.GET(self)
        else:
            print "Not computable Try Again."
            return render.show_room(room=session.room)
            
if __name__ == "__main__":
    app.run()
