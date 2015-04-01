from django import template
register = template.Library()

@register.filter
def groupbyaxis2(valuelist, columnlist):
    return map(lambda col: filter(lambda p: p.axis2==col, valuelist), columnlist)

@register.filter
def filterbyaxis(queryset, axisvalue):
    return queryset.filter(practiceaxisvalue__value = axisvalue)
