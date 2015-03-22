import urllib, urlparse, urllib2, re, os, sys 
import xbmcaddon, xbmc, xbmcplugin, xbmcgui
import HTMLParser
import json
import cookielib
import unicodedata

ADDON = xbmcaddon.Addon(id='plugin.video.dom2')
ADDON_ID = 'plugin.video.dom2'
WEB_PAGE_BASE = 'http://video-dom2.ru/onlinetv/'

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
		videoLink = util.extract(content, 'file:"', '"')
		util.playMedia(params['title'], params['image'], videoLink, 'Video')

def buildMenu():
	url = WEB_PAGE_BASE + 'tv_rec.php'
	response = urllib2.urlopen(url)
	if response and response.getcode() == 200:
		content = response.read()
		videos = util.extractAll(content, '<td class="td_ser">', '</td>')
		for video in videos:
			params = {'play':1}
			params['video'] = WEB_PAGE_BASE + util.extract(video, '<a  href="', '"')
			params['image'] = ""
			params['title'] = util.extract(video, 'title="', '"').decode('windows-1251').encode('utf-8')
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


