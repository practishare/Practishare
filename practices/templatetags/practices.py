from django import template
register = template.Library()

@register.filter
def groupbyaxis2(valuelist, colomnlist):
    return map(lambda col: filter(lambda p: p.axis2==col, valuelist), colomnlist)
