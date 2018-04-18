<%
    fields = plugin_config['fields'].split()
    if not fields:
        fields = ("preferredDisplayName", "eduPersonPrimaryAffiliation", "eduPersonAffiliation", "title", "eduPersonPrimaryOrgUnitDN", "mail", "campusAddress", "telephoneNumber", "uid")
%>

%for r in records:
<%
cn, values = r
%>
<h4>${cn}</h4>
<table border="1" cellpadding="1" cellspacing="0">
%for f in [x for x in fields if x in values]:
<%
result = ', '.join(values[f])
%>
<tr>
    <td> ${f} </td>
    <td> ${result} </td>
</tr>
%endfor
</table>
%endfor
