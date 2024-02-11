#!/usr/bin/env python
#
# Autonomous catepillar by m.e. of cartheur
# Started 27.01.2015 and only now is it cool!

from bottle import run, get, post, request, route, redirect
import socket

class WebFramework:
    def __init__(self,func):
        self.ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        print( "---------")
        print( "cartheur presents emotional toys")
        print( "Open a browser and point it to " + str(self.ip) + ":8080")
        print( "---------")
        self.talkFunc = func
        
        @route('/')
        def index():
            return '''
                <form action="/" method="post">
                    What do you want your animal to say?<p><input name="speech" type="text" />
                    <input value="TALK" type="submit" />
                </form>
            '''
        @post('/')
        def speak():
            speech = request.forms.get('speech')            
            self.talkFunc( speech )
            redirect('/')

        run(host=self.ip, port=8080, debug=True)
