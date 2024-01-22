from django.forms.models import model_to_dict


################################################################################
# SOURCE:
# https://stackoverflow.com/questions/62840397/how-to-pass-foreignkey-in-dict-to-create-model-object-django#
#
#
# modified model_to_dict returning fk's instances instead of id's,
# allowing SomeModel.objects.create(**model_to_dict_wfk(some_instance)
# extended to support exclude for fk's
def model_to_dict_wfk(modelobj, *args, **kwargs):
    opts = modelobj._meta.fields
    exclude = {}
    if 'exclude' in kwargs.keys():
        exclude = set(kwargs['exclude'])
    modeldict = model_to_dict(modelobj, *args, **kwargs)
    for m in opts:
        if m.is_relation:
            foreignkey = getattr(modelobj, m.name)
            if foreignkey and m.name not in exclude:
                modeldict[m.name] = model_to_dict_wfk(foreignkey)
    return modeldict
################################################################################
