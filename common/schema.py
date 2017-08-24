import graphene

class BaseNode(graphene.Node):
	"""Interface to remove the base64 encoding and use defaul django ids."""

	pass
	# @classmethod
	# def get_node_from_global_id(cls, global_id, context, info, only_type=None):
	# 	node = super().get_node_from_global_id(global_id, context, info, only_type)

	# 	if node:
	# 		return node

	# 	get_node = getattr(only_type, 'get_node', None)
	# 	if get_node:
	# 		return get_node(global_id, context, info)
	
	# @classmethod
	# def to_global_id(cls, type, id):
	# 	return id
