#!/usr/bin/env python3

import ui
import time
import objc_util

# Check out https://github.com/jankais3r/HoloSkype for an example project
url = 'http://192.168.1.75:9090/holo.html'
LG_width = 2560
LG_height = 1600

@objc_util.on_main_thread
def main():
	global wk, second_screen, second_window
	UIScreen = objc_util.ObjCClass('UIScreen')
	
	if len(UIScreen.screens()) > 1:
		second_screen = UIScreen.screens()[1]
		second_screen.overscanCompensation = 0
		bounds = second_screen.bounds()
		
		UIWindow = objc_util.ObjCClass('UIWindow')
		second_window = UIWindow.alloc().initWithFrame_(bounds)
		second_window.setScreen(second_screen)
		second_window.makeKeyAndVisible()
		
		wk = objc_util.ObjCClass('WKWebView').alloc().initWithFrame_(objc_util.CGRect((0, 0), (LG_width, LG_height - 1))).autorelease()
		
		second_window.addSubview(wk)
		
		request = objc_util.ObjCClass('NSURLRequest').alloc().init()
		nsurl = objc_util.nsurl(url)
		x = request.initWithURL_(nsurl)
		wk.loadRequest_(x)
	else:
		print('No secondary screen detected. Connect your Looking Glass.')
		v.close()
		quit()
		
def close_button(sender):
	global v, wk, second_screen, second_window
	wk.loadHTMLString_baseURL_('', None)
	del wk, second_window, second_screen
	v.close()
	quit()
	
button = ui.Button(title = 'Close', background_color = 'white', tint_color = 'white', corner_radius = 5)
button.action = close_button
v = ui.View()
v.add_subview(button)
v.present(style = 'fullscreen', hide_title_bar = True)
button.frame = (v.width / 2 - 40, v.height / 2 - 16, 80, 32)
button.background_color = 'black'

wk, second_window = None, None
main()
try:
	# If you are rendering a complex Three.js scene and the hologram doesn't look right, try increasing the sleep timer.
	# This is a hack around a webkit bug. The window needs to be resized once the rendering completes in order to apply correct shader values.
	time.sleep(3)
	wk.setFrame_(objc_util.CGRect((0, 0), (LG_width, LG_height)))
except:
	pass
