"""assign/unassign to ToDo"""

import webnotes

@webnotes.whitelist()
def get():
	"""get assigned to"""
	return webnotes.conn.sql("""select owner from `tabToDo Item`
		where reference_type=%(doctype)s and reference_name=%(name)s
		order by modified desc limit 5""", webnotes.form_dict, as_dict=1)
		
@webnotes.whitelist()
def add():
	"""add in someone's to do list"""
	if webnotes.conn.sql("""select owner from `tabToDo Item`
		where reference_type=%(doctype)s and reference_name=%(name)s
		and owner=%(assign_to)s""", webnotes.form_dict):
		webnotes.msgprint("Already in todo")
		return
	else:
		from webnotes.model.doc import Document
		from webnotes.utils import nowdate
		
		d = Document("ToDo Item")
		d.owner = webnotes.form_dict['assign_to']
		d.reference_type = webnotes.form_dict['doctype']
		d.reference_name = webnotes.form_dict['name']
		d.description = webnotes.form_dict['description']
		d.priority = webnotes.form_dict.get('priority', 'Medium')
		d.date = webnotes.form_dict.get('date', nowdate())
		d.save(1)
		
	# update feeed
	try:
		import home
		from webnotes.utils import get_full_name
		home.make_feed('Assignment', d.reference_type, d.reference_name, webnotes.session['user'],
			'[%s] Assigned to %s' % (d.priority, get_full_name(d.owner)), '#C78F58')
	except ImportError, e:
		pass
	
	
	return get()

@webnotes.whitelist()
def remove():
	"""remove from todo"""
	webnotes.conn.sql("""delete from `tabToDo Item`
		where reference_type=%(doctype)s and reference_name=%(name)s
		and owner=%(assign_to)s""", webnotes.form_dict)
		
	return get()
