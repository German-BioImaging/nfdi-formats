# /// script
# requires-python = ">=3.12"
# dependencies = [ "rdflib", "pyyaml", "jsonschema" ]
# ///
from rdflib import Graph, URIRef
from jsonschema import validate
import sys
import json
import yaml
import glob

# Aggregate formats metadata
formats = {}
for file in glob.glob("formats/*.yaml"):
    id = file.split("/")[1][0:-5]
    data = yaml.safe_load(open(file, "r"))
    data["handle"] = id
    formats[id] = data

# Check formats metadata
schema = json.load(open("schema.json", "r"))

def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)

for id in formats:
    try:
        validate(instance=formats[id], schema=schema)
    except Exception as e:
        fail(f"formats/{id}.yaml is invalid!\n{e}")
    # base formats must exist and not be itself
    if "base" in formats[id]:
        base = formats[id]["base"]
        if base is id or base not in formats:
            fail(f"base '{base}' of formats/{id}.yaml not found!")

# Convert to RDF
data = yaml.safe_load(open("nfdi.yaml", "r"))

data["handle"] = ""
data["file_formats"] = [formats[id] for id in formats.keys()],
data["@context"] = json.load(open("context.json", "r"))

g = Graph()
g.parse(data=json.dumps(data), format="json-ld")

# save as Turtle
g.bind("", None, replace=True)
g.bind("schema", URIRef("https://schema.org/"))
g.bind("wd", URIRef("http://www.wikidata.org/entity/"))
g.serialize(destination="docs/formats.ttl", format="turtle")
