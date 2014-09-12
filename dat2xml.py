"""
	Converts dat files into Hyperspin XML database files.
	
	v0.1: only tested on Nintendo - Super Nintendo Entertainment System (20140910-225940_CM).dat
	
	Entries are converted as follows:
	
	game (
	name "3x3 Eyes - Seima Kourinden (Japan)"
	description "3x3 Eyes - Seima Kourinden (Japan)"
	rom ( name "3x3 Eyes - Seima Kourinden (Japan).sfc" size 1048576 crc FBF3C0FF md5 E9140405887A1D5F32AA009F1E2CD0DA sha1 3B04986BD3BA2A5E49155CD395F51D2389BFFA51 flags verified )
	)

	into 

	<game name="3x3 Eyes - Seima Kourinden (Japan)">
		<description>3x3 Eyes - Seima Kourinden (Japan)</description>
		<cloneof></cloneof>
		<crc>FBF3C0FF</crc>
		<manufacturer></manufacturer>
		<year></year>
		<genre></genre>
		<rating></rating>
		<enabled>Yes</enabled>
	</game>
"""

entry = {}
is_new_entry = False
with open('Nintendo - Super Nintendo Entertainment System (20140910-225940_CM).dat', 'r') as input_file, open('Super Nintendo Entertainment System.xml', 'w') as output_file:
	# Write initial headers
	output_file.write("""<?xml version="1.0"?>
<menu>
	<header>
		<listname>Super Nintendo Entertainment System</listname>
		<lastlistupdate>dd/mm/yyyy</lastlistupdate>
		<listversion>0.1</listversion>
		<exporterversion>dat2xml.py</exporterversion>
	</header>
	""")
	
	for line in input_file:
		line = line.rstrip().lstrip()
		if line.startswith('game ('):
			# New entry
			is_new_entry = True
			entry = {}
		if is_new_entry:
			if line.startswith("name"):
				entry['name'] = line[len("name")+2:-1]		
			if line.startswith("description"):
				entry['description'] = line[len("description")+2:-1]
			if line.startswith("rom"):
				split = line.split("\"")
				info = split[2:][0].lstrip().rstrip().split(" ")			
				entry['crc'] = info[3]
		if line==')' and is_new_entry:
			xml_entry = """
	<game name="{name}">
		<description>{desc}</description>
		<cloneof></cloneof>
		<crc>{crc}</crc>
		<manufacturer></manufacturer>
		<year></year>
		<genre></genre>
		<rating></rating>
		<enabled>Yes</enabled>
	</game>""" .format(name=entry['name'], desc=entry['description'], crc=entry['crc'])
			# print (xml_entry)
			output_file.write(xml_entry.replace('&', '&#x26;'))
			is_new_entry = False
			
	
	output_file.write("""
</menu>""")
