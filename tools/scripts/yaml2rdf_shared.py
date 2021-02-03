'''
Common functionality for ASKotec training meta-data conversion
from YAML into an RDF/Turtle.
'''

import re
import os
from packaging import version
import yaml
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD

SCHEMA = rdflib.Namespace('http://schema.org/')
SPDX = rdflib.Namespace('http://spdx.org/rdf/terms#')
ASK  = rdflib.Namespace('http://myontology.com/')
ASKA = rdflib.Namespace('http://myontology.com/authors/')
ASKM = rdflib.Namespace('http://myontology.com/modules/')
ASKR = rdflib.Namespace('http://myontology.com/resources/')
ASKC = rdflib.Namespace('http://myontology.com/materials/')
ASKT = rdflib.Namespace('http://myontology.com/tools/')

def version_compare(ver1, ver2):
    '''
    Compares two version strings.
    '''
    return version.parse(ver1) < version.parse(ver2)

def rdf_str(s):
    '''
    Converts a simple string into an RDF string (xsd:string).
    '''
    return rdflib.Literal(s, datatype=XSD.string)

def rdf_int(s):
    '''
    Converts a simple string into an RDF int (xsd:int).
    '''
    return rdflib.Literal(s, datatype=XSD.int)

def rdf_path(s):
    '''
    Converts a simple string into an RDF file path (xsd:string).
    '''
    return rdflib.Literal(s, datatype=XSD.string)

def rdf_url(s):
    '''
    Converts a simple string into an RDF URL (schema:URL).
    '''
    return rdflib.Literal(s, datatype=SCHEMA.URL)

def rdf_monetary_amount(s):
    '''
    Converts a simple string into an RDF monetary amount (schema:MonetaryAmount).
    '''
    return rdflib.Literal(s, datatype=SCHEMA.MonetaryAmount)

def rdf_duration(s):
    '''
    Converts a simple string into an RDF duration (schema:Duration).
    '''
    return rdflib.Literal(s, datatype=SCHEMA.Duration)

def str2id(s):
    '''
    Converts a random string into a valid RDF id (the last part of an IRI).
    '''
    return re.sub('[^a-zA-Z0-9_-]+', '_', s)

def conv_fail(msg):
    raise RuntimeError(msg)

def add(graph, subj, pred, yaml_cont, prop, type_conv, required=True):

    if prop in yaml_cont:
        graph.add(( subj, pred, type_conv(yaml_cont[prop]) ))
    elif required:
        conv_fail('Required property "%s" not present' % prop)

def conv_license(yaml_cont, g):

    subj  = ASK[str2id(yaml_cont['name'])]
    # TODO Replace this with an external type, probably [http://spdx.org/rdf/terms#License](https://spdx.org/rdf/terms/#d4e2374)
    g.add(( subj, RDF.type, ASK.License ))
    g.add(( subj, RDFS.label, rdf_str(yaml_cont['name']) ))
    g.add(( subj, SPDX.licenseDeclared, SPDX[yaml_cont['name']] ))
    g.add(( subj, SCHEMA.file, rdf_str(yaml_cont['file']) ))
    return subj

def conv_licenses(yaml_cont, g, parent_subj):

    if 'licenses' in yaml_cont:
        for yaml_cont_part in yaml_cont['licenses']:
            g.add(( parent_subj, ASK.license, conv_license(yaml_cont_part, g) ))

def conv_author(yaml_cont, graph):

    subj  = ASKA[str2id(yaml_cont['name'])]
    graph.add(( subj, RDF.type, ASK.Author ))
    #graph.add(( subj, RDFS.label, rdf_str(yaml_cont['name']) ))
    graph.add(( subj, SCHEMA.name, rdf_str(yaml_cont['name']) ))
    graph.add(( subj, SCHEMA.email, rdf_str(yaml_cont['email']) ))
    graph.add(( subj, SCHEMA.github, rdf_url(yaml_cont['github-user']) ))
    if 'telegram' in yaml_cont:
        graph.add(( subj, SCHEMA.telegram, rdf_str(yaml_cont['telegram']) ))
    #add(graph, subj, SCHEMA.telegram, yaml_cont, 'telegram', rdf_str, False)
    return subj

def conv_authors(yaml_cont, graph, parent_subj):

    if 'authors' in yaml_cont:
        for yaml_cont_part in yaml_cont['authors']:
            graph.add(( parent_subj, ASK.author,
                conv_author(yaml_cont_part, graph) ))

