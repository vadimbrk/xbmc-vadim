import urllib, urlparse, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
import json
import cookielib
import unicodedata

ADDON = xbmcaddon.Addon(id='plugin.video.dom2')
ADDON_ID = 'plugin.video.dom2'
WEB_PAGE_BASE = 'http://nash-dom2.ru/page/1/'

__plugin__ = "Dom2 Add-on"
__author__ = "Vadim Brook"
my_addon = xbmcaddon.Addon(ADDON_ID)
addon_dir = xbmc.translatePath( my_addon.getAddonInfo('path') )
sys.path.append(os.path.join( addon_dir, 'resources', 'lib' ) )
import util

def playVideo(params):
	response = urllib2.urlopen(params['video'])
	if response and response.getcode() == 200:
		content = response.read()
		videoLink = util.extract(content, '"]="', '"')
		util.playMedia(params['title'], params['image'], videoLink, 'Video')
	else:
		util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))

def buildMenu():
	url = WEB_PAGE_BASE 
	response = urllib2.urlopen(url)
	if response and response.getcode() == 200:
		content = response.read()
		videos = util.extractAll(content, '<div class="post-head">', '</div>')
		for video in videos:
			params = {'play':1}
			diplink = util.extract(video, 'a href="', '\"')
			response = urllib2.urlopen(diplink)
			if response and response.getcode() == 200:
				content = response.read()
				page = util.extractAll(content,'<iframe src="','"')
				for links in page:
					test = util.extract(links, 'http://','.tv')
					if test == 'veterok':
						videoUrl = links
				
			params['video'] = videoUrl
			icon = videoUrl + 'xx'
			params['image'] = 'http://veterok.tv/thumb/' +str(util.extract(icon,'http://veterok.tv/v/','xx')) +'.jpg'
			params['title'] = util.extract(video, '>', '</a>').decode('windows-1251').encode('utf-8')
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


