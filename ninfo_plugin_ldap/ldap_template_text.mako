<%
    fields = plugin_config['fields'].split()
    if not fields:
        fields = ("preferredDisplayName", "eduPersonPrimaryAffiliation", "eduPersonAffiliation", "title", "eduPersonPrimaryOrgUnitDN", "mail", "campusAddress", "telephoneNumber", "uid")
%>

%for r in records:
<% cn, values = r %>
%for f in [x for x in fields if x in values]:
<% result = ', '.join(values[f]) %>${f}  ${result}
%endfor

%endfor
