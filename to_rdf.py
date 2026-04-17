from pprint import pprint
import rdflib
import yaml_ld

n_quads_formats = yaml_ld.to_rdf("formats.yaml", {"format": "application/n-quads"})
n_quads_nfdi = yaml_ld.to_rdf("nfdi.yaml", {"format": "application/n-quads"})

g = rdflib.ConjunctiveGraph()
g.parse(data=n_quads_formats, format="nquads")

g.parse(data=n_quads_nfdi, format="nquads")

# save as Turtle
g.serialize(destination="rdf/nfdi_formats.ttl", format="turtle")
