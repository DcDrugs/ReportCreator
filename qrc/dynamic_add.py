qrc = "./qrc/resource.qrc"

target_folder = "./qrc/docs/_build/html"

from bs4 import BeautifulSoup


# Reading the data inside the xml
# file to a variable under the name 
# data
with open(qrc, 'r') as f:
    data = f.read()

Bs_data = BeautifulSoup(data, "xml", preserve_whitespace_tags=["file"])
value = Bs_data.find('qresource', {'prefix':'files'})
import os
result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(target_folder) for f in filenames]

for item in result:
    new_tag = Bs_data.new_tag("file")
    new_tag.string = item[len("./qrc/"):]
    value.append(new_tag)
    
savechanges = Bs_data.prettify("utf-8") 
savechanges = savechanges[len('<?xml version="1.0" encoding="utf-8"?>'):]
with open("./qrc/resourcebuild.qrc", "wb") as file: 
    file.write(savechanges) 