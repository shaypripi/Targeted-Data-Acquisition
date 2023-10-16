# Targeted-Data-Acquisition
Targeted Data Acquisition from Open Data Repositories project as part of the CSE303 class of Ecole Polytechnique

**Project Description**
This module is designed to facilitate the retrieval of information from Wikidata, focusing on common types of items such as humans, organizations and locations.
It provides functions to search for items in Wikidata and extract important information from them, based on graph traversing, as opposed to NLP oriented search.

**It's main functions are:**

**get_Q_code(name: str, type: str, type_matching_func: Callable[[str], str], exact_type: bool = False) -> Optional[str]**

  Description: Given a name and a type, this function returns the Q-code of the corresponding Wikidata item.
  
  Parameters:
  
  name (str): The name of the item to search for.
  type (str): The type of the item to search for.
  type_matching_func (Callable[[str], str]): A function that maps the type to a Wikidata type.
  exact_type (bool): If True, only search for items of the exact specified type. If False, search for items that are instances of the specified type or its subclasses.
  Returns:
  
  Optional[str]: The Q-code of the corresponding Wikidata item, or None if no item was found.

**extract_properties_by_popularity(Q_code: str) -> list[str]**
  
  Description: Extracts properties from a Wikidata item, sorted by their popularity (number of references).
  
  Parameters:
  
  Q_code (str): The Q-code of the Wikidata item to extract properties from.
  Returns:
  
  list[str]: A list of property IDs (PIDs) representing the properties for the given Wikidata item sorted by the number of references.

**extract_n_item_properties(node: Node, most_referenced_props: list[str], n: int) -> None**

  Description: Extracts the values of the n most referenced properties for a given Wikidata item and adds them as children of the given node.
  
  Parameters:
  
  node (Node): The node representing the Wikidata item to extract properties from.
  most_referenced_props (list[str]): A list of property IDs (PIDs) representing the most referenced properties for the given Wikidata item.
  n (int): The maximum number of properties to extract. If n is greater than the length of most_referenced_props, only the latter will be extracted.

  
