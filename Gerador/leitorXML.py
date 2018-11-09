# -*- coding: utf-8 -*-
import xmlschema
from pprint import pprint


def LerXML(arq):
    xs = xmlschema.XMLSchema('instancia.xsd')
    print xs.is_valid(arq)
    pprint(xs.to_dict(arq))
    my_dict = xs.to_dict(arq)
    return my_dict

def LerXMLGen(arq):
    xs = xmlschema.XMLSchema('GeraInstancia.xsd')
    print xs.is_valid(arq)
    pprint(xs.to_dict(arq))
    my_dict = xs.to_dict(arq)
    return my_dict
