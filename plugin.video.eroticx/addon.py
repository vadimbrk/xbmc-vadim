import urllib, urlparse, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
import json
import cookielib
import unicodedata

ADDON = xbmcaddon.Addon(id='plugin.video.eroticax')
ADDON_ID = 'plugin.video.eroticax'
WEB_PAGE_BASE = 'http://api.redtube.com/?data=redtube.Videos.searchVideos&output=xml&search=eroticax&humbsize=all'

__plugin__ = "EroticaX Add-on"
__author__ = "Vadim Brook"
my_addon = xbmcaddon.Addon(ADDON_ID)
addon_dir = xbmc.translatePath( my_addon.getAddonInfo('path') )
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )
import util

def playVideo(params):
	url = 'http://embed.redtube.com/video/info/?id=' + params['video']
	response = urllib2.urlopen(url)
	if response and response.getcode() == 200:
		content = response.read()
		videoLink = util.extract(content, '<url src=\'', '\'>')
		util.playMedia(params['title'], params['image'], videoLink, 'Video')

def buildMenu():
	url = WEB_PAGE_BASE
	response = urllib2.urlopen(url)
	if response and response.getcode() == 200:
		content = response.read()
		videos = util.extractAll(content, '<video duration', '</video>')
		for video in videos:
			params = {'play':1}
			params['video'] = util.extract(video, 'video_id="', '"')
			params['image'] = util.extract(video, 'default_thumb="', '"')
			params['title'] = util.extract(video, '<title><![CDATA[', ']]')
			link = util.makeLink(params)
			util.addMenuItem(params['title'], link, 'DefaultVideo.png', params['image'], False)
		util.endListing()
	else:
		util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))


parameters = util.parseParameters()
if 'play' in parameters:
	playVideo(parameters)
else:
	buildMenu()


