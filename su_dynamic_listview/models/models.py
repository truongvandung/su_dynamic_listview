from odoo.models import BaseModel, AbstractModel
from odoo import api
from lxml import etree
import odoo
# import odoo.SUPERUSER_ID

_load_views = AbstractModel.load_views
_fields_view_get = AbstractModel.fields_view_get


@api.model
def load_views(self, views, options=None):
    res = _load_views(self, views, options=options)
    return res


@api.model
def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    res = _fields_view_get(self, view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    # if view_type in ['list', 'tree'] and (odoo.SUPERUSER_ID ==
    # self.env.user.id or self.env.ref('su_dynamic_listview.group_show_field') in self.env.user.groups_id):
    if view_type in ['list', 'tree']:
        shf_obj = self.env['show.field'].search([('model', '=', self._name),
                                                 ('view_id', '=', res.get('view_id', False)),
                                                 ('create_uid', '=', self.env.user.id)])
        if shf_obj:
            doc = etree.XML(res['arch'])
            fields_show = eval(shf_obj[0].fields_show)
            field_base = {}
            for x in doc.xpath("//field"):
                if 'name' in x.attrib:
                    field_base[x.attrib.get('name')] = x
                    x.set("invisible", "1")
                    doc.remove(x)
            for _field_name in fields_show:
                if _field_name['name'] in field_base:
                    _field = field_base[_field_name['name']]
                    _field.set("invisible", "0")
                    _field.set("string", _field_name['string'])
                    field_base.pop(_field_name['name'])
                else:
                    _field = etree.Element(
                        'field', {'name': _field_name['name'], 'string': _field_name['string']})
                doc.xpath("//tree")[0].append(_field)
            for _field_name in field_base:
                doc.xpath("//tree")[0].append(field_base[_field_name])
            res['arch'] = etree.tostring(doc)
            _arch, _fields = self.env['ir.ui.view'].postprocess_and_fields(
                self._name, etree.fromstring(res['arch']), view_id)
            res['arch'] = _arch
            res['fields'] = _fields
    return res

AbstractModel.load_views = load_views
AbstractModel.fields_view_get = fields_view_get
