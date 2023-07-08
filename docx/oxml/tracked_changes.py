"""
Custom element classes related to the tracked changes part
"""

from . import OxmlElement
from .simpletypes import ST_DecimalNumber, ST_String
from ..opc.constants import NAMESPACE
from ..text.paragraph import Paragraph
from ..text.run import Run
from .xmlchemy import (
	BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne
)

class CT_DelText(BaseOxmlElement):
    """
    ``<w:delText>`` element, containing a sequence of characters within a run.
    """


class CT_Ins(BaseOxmlElement):
	"""
	A ``<w:ins>`` element, a container for Insert properties 
	"""
	_id = RequiredAttribute('w:id', ST_DecimalNumber)
	date = RequiredAttribute('w:date', ST_String)
	author = RequiredAttribute('w:author', ST_String)
	
	r = ZeroOrOne('w:r', successors=('w:ins',))

	@classmethod
	def new(cls, ins_id, date, author):
		"""
		Return a new ``<w:ins>`` element having _id of *ins_id* and having
		the passed params as meta data 
		"""
		insert = OxmlElement('w:ins')
		insert.date = date
		insert._id = ins_id
		insert.author = author
		return insert
		
	def _add_r(self, text):
		_r = OxmlElement('w:r')
		#_r = _p.add_r()
		run = Run(_r,self)
		run.text = text
		self.insert(0, _r)
		return _r
	
	@property
	def _next_insId(self):
		"""
		The first ``insId`` unused by a ``<w:ins>`` element, starting at
		1 and filling any gaps in numbering between existing ``<w:ins>``
		elements.
		"""
		insId_strs = self.xpath('.//@w:id')
		print(insId_strs)
		ins_ids = [int(insId_str) for insId_str in insId_strs]
		for ins in range(1, len(ins_ids)+2):
			if ins not in ins_ids:
				break
		return ins

	@property
	def meta(self):
		return [self.author, self.date]
	
class CT_Del(BaseOxmlElement):
	"""
	A ``<w:del>`` element, a container for Deletion properties 
	"""
	_id = RequiredAttribute('w:id', ST_DecimalNumber)
	date = RequiredAttribute('w:date', ST_String)
	author = RequiredAttribute('w:author', ST_String)
	
	r = ZeroOrOne('w:r', successors=('w:ins',))

	@classmethod
	def new(cls, del_id, date, author):
		"""
		Return a new ``<w:del>`` element having _id of *del_id* and having
		the passed params as meta data 
		"""
		delete = OxmlElement('w:del')
		delete.date = date
		delete._id = del_id
		delete.author = author
		return delete
		
	def _add_r(self, text):
		_r = OxmlElement('w:r')
		_del_text = OxmlElement('w:delText')
		_del_text.text = text

		#_r = _p.add_r()
		#run = Run(_r,self)
		_r.insert(0, _del_text)
		self.insert(0, _r)
		return _r
	
	@property
	def _next_insId(self):
		"""
		The first ``insId`` unused by a ``<w:ins>`` element, starting at
		1 and filling any gaps in numbering between existing ``<w:ins>``
		elements.
		"""
		insId_strs = self.xpath('.//@w:id')
		print(insId_strs)
		ins_ids = [int(insId_str) for insId_str in insId_strs]
		for ins in range(1, len(ins_ids)+2):
			if ins not in ins_ids:
				break
		return ins

	@property
	def meta(self):
		return [self.author, self.date]