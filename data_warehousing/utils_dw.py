from shutil import copyfile, rmtree
#from collections import OrderedDict
import os, errno, re, sys, yaml, json
from collections import OrderedDict, defaultdict



# Utils file for the Data Warehousing scripts


# http://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)    
    return yaml.load(stream, OrderedLoader)

# Get a hierarchical dictionary of categories based on the categories.yml file.
# The idea is you can look up a category to get its parent... i.e. "operator" -> "person"
# category -> parent_name
def get_category_hierarchy(categories):
	def parse_categories(category_hierarchy, categories, parent_category):
		for category in categories:			
			category_hierarchy[category] = parent_category
			if categories[category]:
				parse_categories(category_hierarchy, categories[category], category)

	category_hierarchy = {}
	parse_categories(category_hierarchy, categories, None)
	return category_hierarchy

# Gets a dictionary of Superparents (top level categories) matched to an id, for display on the report.
def get_superparent_ids(category_hierarchy):
	superparent_ids = {}
	i = 0
	for key in sorted(category_hierarchy):
		if category_hierarchy[key] == None:
			i += 1
			superparent_ids[key] = i
	return superparent_ids


# Gets the top-level parent (body, injury_type etc) of a category.
def get_superparent_of_category(category, category_hierarchy):	
	top_level = False
	while not top_level:
		parent = category_hierarchy[category]
		if parent is not None:
			category = parent
		else:			
			top_level = True
			parent = category

	superparent = parent
	return superparent

# Creates a dictionary that maps each category to its superparent.
def get_superparent_dict(category_hierarchy):
	superparent_dict = {}
	for category in category_hierarchy:
		superparent_dict[category] = get_superparent_of_category(category, category_hierarchy)
	return superparent_dict

# Creates a dictionary that maps each category to all of its parents.
def get_parent_lookup_dict(category_hierarchy):
	parent_lookup_dict = defaultdict(list)
	for category in category_hierarchy:
		original_category = category
		top_level = False
		while not top_level:
			parent = category_hierarchy[category]
			if parent is not None:
				category = parent
				parent_lookup_dict[original_category].append(category)
			else:			
				top_level = True
				parent = category			
	#print parent_lookup_dict
	return parent_lookup_dict
