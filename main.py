"""
This module provides functions to search for items in Wikidata and extract important information from them.

Functions:
    get_Q_type_basic(label: str) -> str:
        Returns the Q type for a the most common types of items.
    get_Q_code(name: str, type: str, type_matching_func: Callable[[str], str]) -> Optional[Tuple[str, bool]]:
        Gets the Q_code in wikidata of the given item based on the string that it's name and the type of item it is.
    extract_important_information(Q_code: str, item: str, type: str, n_of_properties: int) -> dict:
        Extracts important information from a given Q-code and returns it as a dictionary.
"""
from __future__ import annotations
from typing import Callable, Optional
from wikibaseintegrator import wbi_helpers, wbi_config
from wikidataintegrator import wdi_core
from utils import Node

#############################################################
#LOGIN INFO

WIKIDATA_USERNAME = "Targeted Data Acquisition"
WIKIDATA_PASSWORD = "jU_ui5!7-JzJBQc"
USER_AGENT = "TargetedDataAcquisition (shay.pripstein@polytechnique.edu)"


#############################################################
#MACROS
RECURSIVE_CODE = "/wdt:P279*"

COMMON_Q_TYPES = {
    "human": "Q5",
    "organization": "Q43229",
    "location": "Q7481476",
    "business": "Q4830453",
    "city": "Q515",
}

WIKIDATA_QUERY_SEARCH_TEMPLATE = """
        SELECT ?item ?itemLabel
        WHERE
        {{
            ?item wdt:P31{recursive} wd:{q_type}.
            ?item rdfs:label "{item}"@en.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """



WIKIDATA_PROPERTY_EXTRACTIONS_TEMPLATE = """
    SELECT ?proprty
    WHERE {{
    wd:{Q_code} wdt:{prop} ?proprty.
    }}
    """

WIKIDATA_NAME_EXTRACTIONS_TEMPLATE = """
    SELECT ?propertyLabel
    WHERE {{
    wd:{P_code} rdfs:label ?propertyLabel.
    FILTER(LANG(?propertyLabel) = "en").
    }}
    """
#############################################################

BASIC_SEARCHES_DICT = {
    "Bill Gates": "human",
    "Microsoft": "organization",
    "Seattle": "city",
    "Cristiano Ronaldo": "human",
    "Barcelona": "city",
    "Apple": "organization",
    "New York": "city",
    "LVMH": "organization",
    "Ronald Reagan": "human",
    "UNICEF": "organization",

}




def get_Q_type_basic(label: str) -> str:
    """
    Returns the Q type for a the most common types of items
    """
    if label in COMMON_Q_TYPES: 
        return COMMON_Q_TYPES[label.lower()]
    return ""


def get_Q_code(name: str, type: str, type_matching_func: Callable[[str], str],
                exact_type: bool = False) -> Optional[str]:
    """
    Given a name and a type, returns the Q-code of the corresponding Wikidata item.

    Args:
        name (str): The name of the item to search for.
        type (str): The type of the item to search for.
        type_matching_func (Callable[[str], str]): A function that maps the type to a Wikidata type.

    Returns:
        Optional[str]: The Q-code of the corresponding Wikidata item, or None if no item was found.
    """
    q_type = type_matching_func(type)
    query = WIKIDATA_QUERY_SEARCH_TEMPLATE.format(recursive = "",q_type=q_type, item=name)
    # search wikidata for the item
    results = wbi_helpers.execute_sparql_query(query)
    if not exact_type and len(results["results"]["bindings"]) == 0:
        query = WIKIDATA_QUERY_SEARCH_TEMPLATE.format(recursive=RECURSIVE_CODE ,q_type=q_type,      item=name)
        results = wbi_helpers.execute_sparql_query(query)
    # if there are no results, return None
    if len(results["results"]["bindings"]) == 0:
        return None
    # otherwise, return the first result
    return results["results"]["bindings"][0]["item"]["value"].split("/")[-1]


def extract_properties_by_popularity(Q_code: str) -> list[str]:
    
    """
    Extracts the n properties with the most references from the Wikidata page with the given Q code.

    Args:
        Q_code (str): The Q-code of the Wikidata item to extract properties from.
        n (int): The number of properties to extract.

    Returns:
        dict: A dictionary containing the extracted properties and their reference counts.
    """
    # get the Wikidata page
    item = wdi_core.WDItemEngine(wd_item_id=Q_code)
    # get the properties
    properties = item.get_wd_json_representation()["claims"]

    # sort the properties by the number of references they have
    def ref_sort(x):
        max_score = 0
        for item in properties[x]:
            if "references" in item:
                max_score = max(max_score, len(item["references"]))
        return max_score

    return sorted(properties, key=ref_sort, reverse=True)

def extract_n_item_properties(node: Node, most_referenced_props: list[str], n: int) -> None:
    """
    Extracts the values of the n most referenced properties for a given Wikidata item,
    and adds them as children of the given node.

    Args:
        node (Node): The node representing the Wikidata item to extract properties from.
        most_referenced_props (list[str]): A list of property IDs (PIDs) representing the most referenced properties for the given Wikidata item.
        n (int): The maximum number of properties to extract. If n is greater than the length of most_referenced_props, only the latter will be extracted.

    Returns:
        None.
    """
    n = min(n, len(most_referenced_props))
    for prop in most_referenced_props[:n]:
        query = WIKIDATA_PROPERTY_EXTRACTIONS_TEMPLATE.format(Q_code=node.get_code(), prop=prop)
        prop_name = extract_property_label(prop)
        results = wbi_helpers.execute_sparql_query(query)
        for item in results["results"]["bindings"]:
            node.add_child(Node(prop_name, prop, value=item["proprty"]["value"], parent=node))



def extract_property_label(P_code: str):
    """
    Extracts the property label for a given P-code.

    Args:
        P_code (str): The P-code for the property.

    Returns:
        str: The property label.
    """
    query = WIKIDATA_NAME_EXTRACTIONS_TEMPLATE.format(P_code=P_code)
    results = wbi_helpers.execute_sparql_query(query)
    return results["results"]["bindings"][0]["propertyLabel"]["value"]
    


if __name__ == "__main__":
    wbi_config.config["USER_AGENT"] = USER_AGENT
    for item, type in BASIC_SEARCHES_DICT.items():
        q_code = get_Q_code(item, type, get_Q_type_basic, exact_type=False)
        if q_code is None:
            print(f"Could not find {item} of type {type}")
        else:
            print(f"{item} is of type {type} and has Q code {q_code}")
            node = Node(item, q_code)
            best_props = extract_properties_by_popularity(q_code)
            extract_n_item_properties(node, best_props, 8)
            print(node.get_details())
            
