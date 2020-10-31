'''
Converts ASKotec training module resource meta-data
(from resource.yaml) into an RDF/Turtle.
'''

import re
import os
import yaml
import rdflib
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from yaml2rdf_shared import *

def convert_resource_yaml_to_rdf(yaml_cont, g):
    '''
    Converts ASKotec training module resource meta-data content
    into an RDF/Turtle string.
    '''

    supported_version = "1.0"
    if version_compare(yaml_cont['version'], supported_version) < 0:
        raise 'The content version is not supported by this converter. Please get a newer version!'

    y = yaml_cont['resource']
    pre_path = 'resource'
    m_s = ASKR[str2id(y['name'])]

    g.add(( m_s, RDF.type, ASK.Resource ))
    g.add(( m_s, RDFS.label, rdf_str(y['name']) ))
    if 'manual' in y:
        g.add(( m_s, ASK.manual, rdf_str(y['manual']) ))
    elif os.path.exists('manual.md'):
        g.add(( m_s, ASK.manual, rdf_str('manual.md') ))
    else:
        conv_fail('Entry not found "%s", and default path "%s" does not exist'
                % (pre_path + '.' + 'manual', os.path.curdir + '/manual.md'))
    g.add(( m_s, ASK.release, rdf_str(y['release']) ))
    g.add(( m_s, ASK.duration, rdf_str(y['duration']) ))
    g.add(( m_s, ASK.difficulty, rdf_str(y['difficulty']) ))
    g.add(( m_s, ASK.cost, rdf_str(y['cost']) ))
    g.add(( m_s, ASK.language, rdf_str(y['language']) ))
    #g.add(( m_s, ASK.issues, rdf_str(y['issues']) ))
    #g.add(( m_s, ASK.newIssue, rdf_str(y['new-issue']) ))

    for cp in y['connected-platforms']:
        for key, val in cp.items():
            g.add(( m_s, ASK[str2id(key)], rdf_str(val) ))

    conv_authors(y, g, m_s)
    conv_licenses(y, g, m_s)

    for t in y['materials']:
        t_s  = ASKC[str2id(t['name'])]
        g.add(( t_s, RDF.type, ASK.Material ))
        g.add(( t_s, RDFS.label, rdf_str(t['name']) ))
        g.add(( t_s, SCHEMA.stockroom, rdf_str(t['stockroom']) ))
        g.add(( t_s, SCHEMA.quantity, rdf_int(t['quantity']) ))
        if 'notes' in t:
            g.add(( t_s, SCHEMA.notes, rdf_int(t['notes']) ))
        g.add(( m_s, ASKR.material, t_s ))

    for t in y['tools']:
        t_s  = ASKT[str2id(t['name'])]
        g.add(( t_s, RDF.type, ASK.Tool ))
        g.add(( t_s, RDFS.label, rdf_str(t['name']) ))
        g.add(( t_s, SCHEMA.stockroom, rdf_str(t['stockroom']) ))
        g.add(( t_s, SCHEMA.quantity, rdf_int(t['quantity']) ))
        if 'notes' in t:
            g.add(( t_s, SCHEMA.notes, rdf_int(t['notes']) ))
        g.add(( m_s, ASKR.tool, t_s ))

