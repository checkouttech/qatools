from bottle import route, run, request, get ,static_file 
from bottle import template 
import bottle
from bottle import BaseResponse
from bottle import LocalResponse
import json
from voluptuous import Schema, Required, Invalid , MultipleInvalid, All
from voluptuous import *
from collections import OrderedDict

# REMEMBER :  LocalResponse is the subclass of Response class which contains the "body"  variable 
# Therefore it needs to be inherited 
class ResponseClass(LocalResponse):


    _cwd = os.path.dirname(os.path.realpath(__file__))

    _linksBar = """ 
        <div>
            | <a href="/?json=1&ui=1">Home</a>
            | <a href="/qatools/videoad?json=1&ui=1">Video Ad Page</a>  
            | <a href="/qatools/vastresponse?json=1&ui=1">VAST Response Page</a>  
        </div>
    """ 

    _htmlHeader = """
        <HTML>
        <HEAD>
        <TITLE>Hello World With JavaScript</TITLE>
        </HEAD>
        <BODY>
    """

    _htmlFooter = """
        </BODY>
        </HTML>
    """


    _htmlForm   = """
         <div> 
            <form > 
               <input type="hidden" value="1" name="ui"> 
               <input type="hidden" value="0" name="json"> 
               <input type="text" name=id size="50" rows=4 value="[VAR:id]"> 
               <input type="submit" value="submit">  
            </form>  
         </div> 
    """
    
    _htmlResult = """
        <div>
           <pre>
             [VAR:result] 
           </pre>
      </div>
   """
 
    def __init__(self):
        pass 

   
    def home(self):
        self.body = self._htmlHeader +  self._linksBar + self._htmlFooter

  
    def sendvastxml(self):
        self.content_type = 'xml/application'

        # vast xml sample from http://loopme.biz/wiki/index.php/VAST_ad_tags
        vast_response_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<VAST xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.0" xsi:noNamespaceSchemaLocation="vast.xsd">
    <Ad id="22175">
        <InLine>
            <AdSystem version="v0.2.225">LoopMe LTD</AdSystem>
            <AdTitle><![CDATA[ i-mopub test s2s-VAST-creative-5-copy3 ]]></AdTitle>
            <Error>
                <![CDATA[ http://loopme.me/api/errors?msg=vast_error ]]>
            </Error>
            <Impression id="LoopMe">
                <![CDATA[ http://loopme.me/api/v2/events?et=INBOX_OPEN&rid=7fwcr09c&id=7fwcr09c0h3z03kc ]]>
            </Impression>
            <Impression id="Client Impression">
                <![CDATA[ http://3rdpartyviewtracker.com ]]>
            </Impression>
            <Creatives>
                <Creative sequence="1" id="22175">
                    <Linear>
                        <Duration>00:00:25</Duration>
                        <TrackingEvents>
                            <Tracking event="start">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_STARTS&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="firstQuartile">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_25&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="midpoint">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_50&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="thirdQuartile">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_75&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="complete">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_COMPLETES&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="close">
                                <![CDATA[ http://loopme.me/api/v2/events?et=AD_CLOSE&rid=7fwcr09c&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="pause">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_PAUSE&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                            <Tracking event="resume">
                                <![CDATA[ http://loopme.me/api/v2/events?et=VIDEO_RESUME&id=7fwcr09c0h3z03kc ]]>
                            </Tracking>
                        </TrackingEvents>
                        <VideoClicks>
                            <ClickThrough>
                                <![CDATA[ http://loopme.me/go2/7fwcr09c0h3z03kc ]]>
                            </ClickThrough>
                        </VideoClicks>
                        <MediaFiles>
                            <MediaFile delivery="progressive" width="480" height="320" type="video/mp4">
                                <![CDATA[ http://i.loopme.me/09184cada87e995c.mp4 ]]>
                            </MediaFile>
                        </MediaFiles>
                    </Linear>
                </Creative>
                <Creative sequence="1" id="22175">
                    <CompanionAds>
                        <Companion width="480" height="320">
                            <StaticResource creativeType="image/jpg">
                                <![CDATA[ http://i.loopme.me/0d295c06b9ab0e0d.jpg ]]>
                            </StaticResource>
                            <TrackingEvents>
                                <Tracking event="creativeView">
                                    <![CDATA[  http://loopme.me/api/v2/events?et=COMPANION_SHOW&id=7fwcr09c0h3z03kc ]]>
                                </Tracking>
                            </TrackingEvents>
                            <CompanionClickThrough>
                                <![CDATA[ http://loopme.me/go2/7fwcr09c0h3z03kc ]]>
                            </CompanionClickThrough>
                        </Companion>
                    </CompanionAds>
                </Creative>
            </Creatives>
        </InLine>
    </Ad>
</VAST>
        """

        self.body = vast_response_xml 

  
    def videoadpage(self):
       # self.content_type = 'text/html; charset=UTF-8'

        print self._cwd 
   
        videoPageHtml = '''
<!DOCTYPE html>
<html>
<head>
<script type="text/javascript" src="/static/video/jwplayer/jwplayer.js" ></script>
<script type="text/javascript">jwplayer.key="JWPLAYER_KEY"</script><!-- LongTail JW license read from config file -->
</head>

<h1>Video Ad Call Page</h1>

<body>

<!-- Place were the video player is supposed to appear -->
<div id="myVideoPlayer"></div> 


<!-- Script section declaring video details -->
<script>

var playerInstance = jwplayer("myVideoPlayer");
  playerInstance.setup({
    
    // video will start only when clicked upon 
    autostart: "false", 
    
    // video should start in mute mode 
    mute: "true", 

    title: "AE-wrapper", 

    // this will not show the play button in center of screen , instead the title will be displayed 
    displaytitle: "false",

    // logo to be shown on the top right of the player
    logo: { "file": "/static/video/content-via-wrapper.png", "position":"top-right" },
    
    // Image file to be displayed in case of companion ad 
    image: "/static/video/content-via-wrapper.png",

    // Video file to be played after ad is served 
    file: "/static/video/media/30-sec_content.flv",

    // Block to integrate advertising 
    advertising: {

      // client type vast 
      client: "vast",

      // Ad server url to call to get vast xml (
      // tag : "http://192.168.150.101:8080/xml",
      tag : "http://192.168.150.101:28080/qatools/vastresponse?json=1&ui=1",

      // Message shown next to play icon when  aad is being played 
      admessage: "Ad-via-wrapper: content will resume in XX seconds..."
    }
  });
</script>

</body>
</html> 
       '''

        self.body = self._htmlHeader +  self._linksBar + videoPageHtml



STATIC_ROOT="/home/vagrant/qatools/static/"
#STATIC_ROOT="/home/vagrant/qatools/static/video/jwplayer/"
    

@route('/')
@route('/qatools/')
@route('/qatools/home')
def home():
    res = ResponseClass() 
    res.home()
    return res  


@route('/qatools/vastresponse')
def vastresponse():
    res = ResponseClass() 
    res.sendvastxml()
    return res  


@route('/qatools/videoad')
def videoad():
    res = ResponseClass() 
    res.videoadpage()
    return res  


@get('/static/<filename:path>')
def send_static(filename):
    """ Serves static files """
    print  "........ filename " + filename 
    return static_file(filename, root=STATIC_ROOT)

run(host="0.0.0.0", port=28080, debug=True)


