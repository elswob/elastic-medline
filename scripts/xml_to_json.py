from collections import defaultdict
import json
import sys
import xml.etree.ElementTree as ET

#http://stackoverflow.com/questions/19286118/python-convert-very-large-6-4gb-xml-files-to-json

def parse_xml(file_name):
    events = ("start", "end")
    context = ET.iterparse(file_name, events=events)

    return pt(context)

def pt(context, cur_elem=None):
    items = defaultdict(list)

    if cur_elem:
        items.update(cur_elem.attrib)

    text = ""

    for action, elem in context:
        # print("{0:>6} : {1:20} {2:20} '{3}'".format(action, elem.tag, elem.attrib, str(elem.text).strip()))

        if action == "start":
            items[elem.tag].append(pt(context, elem))
        elif action == "end":
            text = elem.text.strip() if elem.text else ""
            break

    if len(items) == 0:
        return text

    return { k: v[0] if len(v) == 1 else v for k, v in items.items() }

if __name__ == "__main__":
    json_data = parse_xml("xml/pubmed_result_elsworth.xml")
    #print(json.dumps(json_data, indent=2))
