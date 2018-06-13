#INCOMPLETE :: DOES NOT FIX THE LAST POM.XML IN THE COMPARE LINK
#INCOMPLETE :: CHECK IF THE FIX IS CORRECT

import re
import os
import xml.etree.ElementTree as xml

#Non-resolvable parent POM: 
#Could not transfer artifact de.charite.compbio:Jannovar:pom:0.15-SNAPSHOT 
##from/to codehaus-snapshots (https://nexus.codehaus.org/snapshots/): 
#nexus.codehaus.org and 'parent.relativePath' points at wrong local POM @ line 11, column 10: Unknown host nexus.codehaus.org

input_error = " Non-resolvable parent POM: Could not transfer artifact de.charite.compbio:Jannovar:pom:0.15-SNAPSHOT from/to codehaus-snapshots (https://nexus.codehaus.org/snapshots/): nexus.codehaus.org and 'parent.relativePath' points at wrong local POM @ line 11, column 10: Unknown host nexus.codehaus.org"

namespaces = {'xmlns' : 'http://maven.apache.org/POM/4.0.0'}

xml.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
xml.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')


#STORING PATHS TO ALL POM.XML FILES IN AN ARRAY
def find_all_pom_files(name, path):
	poms = []
	for root, dirs, files in os.walk(path):
		if name in files:
			poms.append(os.path.join(root, name))
	return poms

def main(input_error, to_print=False):
	print "Inside main function"
	if "Could not find artifact" and "Non-resolvable parent POM" in input_error : #Convert this to a regex match later.
		print "We are inside the if statement"

		regex_whole_damn_thing = r".+ Could not transfer artifact ([\w\.\:\-]+) .+"
		grouped_output = re.search(regex_whole_damn_thing, input_error)

		print "grouped_output", grouped_output

		artifact = grouped_output.group(1).split(":")
		print artifact

		#Find the file which needs to be opned.
		poms = find_all_pom_files("pom.xml","/home/prerit/Spring2018/ECS260/Project/BuildEZ/Code/charite")
		#poms = find_all_pom_files("pom.xml","/home/travis/build/failed")
		print poms

		#Remove the dependency
		for filepath in poms:
			pomFile = xml.parse(filepath)
			root = pomFile.getroot()
			print "-----------"
			print filepath

			parent = root.find(".//xmlns:parent", namespaces=namespaces)
			print parent

			groupId = parent.find("xmlns:groupId", namespaces=namespaces)
			artifactId = parent.find("xmlns:artifactId", namespaces=namespaces)

			print "dddd ::",artifact[0]
			print "dddd :: ",artifact[1]
			
			if(groupId.text == artifact[0] and artifactId.text == artifact[1]):
				print groupId.text
				print artifactId.text
				version = parent.find("xmlns:version", namespaces=namespaces)
				version_numbers_error_message = [int(s) for s in re.findall(r'\d+', artifact[3])]
				version_numbers_pom = [int(s) for s in re.findall(r'\d+', version.text)]
				print version.text
				if(version_numbers_pom[1] == version_numbers_error_message[1]):
					version.text = version.text.replace(str(version_numbers_pom[1]), str(version_numbers_pom[1] - 1))
				print version.text

				print "File updating "
				pomFile.write(filepath)
			else:
				groupId = root.find("xmlns:groupId", namespaces=namespaces)
				artifactId = root.find("xmlns:artifactId", namespaces=namespaces)
				version = root.find("xmlns:version", namespaces=namespaces)
				print groupId.text
				print artifactId.text
				if(groupId.text == artifact[0] and artifactId.text == artifact[1]):
					version_numbers_error_message = [int(s) for s in re.findall(r'\d+', artifact[3])]
					version_numbers_pom = [int(s) for s in re.findall(r'\d+', version.text)]
					if(version_numbers_pom[1] == version_numbers_error_message[1]):
						version.text = version.text.replace(str(version_numbers_pom[1]), str(version_numbers_pom[1] - 1))
					print "File updating "
					pomFile.write(filepath)



if __name__ == '__main__':
	main(input_error)
