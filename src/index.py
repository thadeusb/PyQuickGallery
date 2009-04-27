#!/usr/bin/python
#
# Copyright (C) 2009 Thadeus Burgess
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__="Thadeus Burgess <thadeusb@thadeusb.com>"
__date__ ="$Apr 25, 2009 2:32:57 AM$"

import os
import Image

print "Content-type: text/html\n\n"
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>Auto Generating Photo Gallery</title>
	<link rel="stylesheet" type="text/css" href="style.css" />
	<link rel="stylesheet" type="text/css" href="resources/fancy.css" />

	<script type="text/javascript" src="js/jquery-1.2.3.pack.js"></script>
	<script type="text/javascript" src="js/jquery.fancybox-1.0.0.js"></script>

	<script type="text/javascript">
                $(document).ready(function() {

                    $(".show-hide-div").hide();

                    $(".show-hide").click(function(event){
                        event.preventDefault();
                        $(".show-hide-div").hide();
                        $(".show-hide").removeClass("selected");
                        $("#"+$(this).attr("name")).show();
                        $(this).addClass("selected");
                    });
                    
                    $(".photo-link").fancybox({ 'zoomSpeedIn': 500, 'zoomSpeedOut': 500, 'overlayShow': true });
                });
                

        </script>
</head>

<body>
	<div id="page-wrap">
		<img src="resources/header.png" alt="Photo Gallery" /><br />
"""
per_column = 6

pictures = {}
thumbs = []
images = []
to_thumbnail = []

dir = '.'

# Find Files
for root, dirs, files in os.walk(dir):
    for file in files:
        if file[-3:] == "jpg":
            full_path = os.path.join(root, file)
            if '-thumb' in file:
                thumbs.append(full_path)
            else:
                root_name = root.split('/')[-1]
                if not root_name in pictures:
                    pictures[root_name] = []
                images.append(full_path)
                pictures[root_name].append(full_path)

# Reconcile Images
for img in images:
    flg = True
    for thb in thumbs:
        f = thb.replace('-thumb.jpg', '')
        i = img.replace('.jpg', '')
        if f == i:
            flg = False

    if flg:
        to_thumbnail.append(img)

# Create New Thumbnails
for thmbing in to_thumbnail:
    try:
        thmb_name = thmbing.replace('.jpg', '') + '-thumb.jpg'

        im1 = Image.open(thmbing)

        im2 = im1.resize((100, 100), Image.ANTIALIAS)

        im2.save(thmb_name)
    except:
        pass

# Print Categories
count = 0
print '<ul>'
for div, pics in pictures.items():
    print '<li>'
    print '<a class="show-hide" id="show-hide-'+div+'" name="' + div + '"rel="show-hide-all" href="#">'
    print '<img src="' + pics[0].replace('.jpg', '-thumb.jpg') + '" width="100" height="100"/>'
    print '<p>' + div + '</p>'
    print '</a>'
    print '</li>'
    if count % per_column == 0:
        print '<div class="clear"></div>'
    count += 1
print '</ul>'
print '<br />'
print '<div class="clear"></div>'


# Print Pictures
for div, pics in pictures.items():
    print '<div class="show-hide-div" id="' + div + '">'

    count = 0
    for image in pics:
        thumb = image.replace('.jpg', '-thumb.jpg')
        print '<a class="photo-link" rel="one-big-group" href="' + image + '"><img src="' + thumb + '" width="100" height="100" /></a>'
        if count % per_column == 0:
            print '<div class="clear"></div>'
        count += 1

    print '</div>'


print """
	</div>

</body>
</html>
"""