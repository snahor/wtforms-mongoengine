import re
import wtforms

from mongoengine.document import Document
from mongoengine.fields import ReferenceField, StringField, ListField
from mongoengine.fields import IntField, SequenceField, BinaryField

from wtforms_mongoengine.fields import QuerySetSelectField
from wtforms_mongoengine.fields import QuerySetSelectMultipleField
from wtforms_mongoengine.orm import model_form


class MultiDict(dict):
    def getlist(self, key):
        value = self[key]
        if not isinstance(value, list):
            value = [value]
        return value


def test_binary_field(conn):
    class Binary(Document):
        binary = BinaryField()

    BinaryForm = model_form(Binary)
    form = BinaryForm(MultiDict({'binary': '1'}))
    assert form.validate()


def test_model_select_field_using_model_form(conn):
    class Dog(Document):
        pass

    class DogOwner(Document):
        dog = ReferenceField(Dog)

    DogOwnerForm = model_form(DogOwner)

    dog = Dog()
    dog.save()

    form = DogOwnerForm(dog=dog)

    assert form.validate()
    assert wtforms.widgets.Select == type(form.dog.widget)
    assert not form.dog.widget.multiple


def test_model_select_multiple_field(conn):
    class Dog(Document):
        name = StringField()

    class DogOwner(Document):
        dogs = ListField(ReferenceField(Dog))

    DogOwnerForm = model_form(DogOwner)

    dogs = [Dog(name="fido"), Dog(name="rex")]
    for dog in dogs:
        dog.save()

    form = DogOwnerForm(dogs=dogs)
    assert form.validate()

    assert wtforms.widgets.Select == type(form.dogs.widget)
    assert form.dogs.widget.multiple

    # Validate if both dogs are selected
    choices = list(form.dogs)
    assert len(choices) == 2
    assert choices[0].checked
    assert choices[1].checked


def test_queryset_select_field(conn):
    class Foo(Document):
        pass

    class Form(wtforms.Form):
        foo = QuerySetSelectField(queryset=Foo.objects)

    foo = Foo()
    foo.save()

    form = Form(MultiDict(foo=foo.id))
    assert form.validate()
    assert form.foo.data == foo

    class Country(Document):
        code = StringField(primary_key=True)

    for i in ('US', 'PE', 'BR'):
        Country(code=i).save()

    class Form(wtforms.Form):
        country = QuerySetSelectField(queryset=lambda: Country.objects)

    form = Form(MultiDict(country='US'))
    assert form.validate()
    assert isinstance(form.country.data, Country)
    assert form.country.data.code == 'US'

    class Number(Document):
        number = IntField(primary_key=True)

    for i in range(5):
        Number(number=i).save()

    class NumberForm(wtforms.Form):
        number = QuerySetSelectField(queryset=Number.objects)

    form = NumberForm(MultiDict(number=3))
    number_3 = Number.objects.with_id(3)

    assert form.validate()
    assert isinstance(form.number.data, Number)
    assert form.number.data == number_3
    assert form.number.data.number == 3

    class Seq(Document):
        number = SequenceField(primary_key=True)

    for i in range(5):
        Seq().save()

    class SeqForm(wtforms.Form):
        number = QuerySetSelectField(queryset=Seq.objects)

    form = SeqForm(MultiDict(number=3))
    number_3 = Seq.objects.with_id(3)

    assert form.validate()
    assert isinstance(form.number.data, Seq)
    assert form.number.data == number_3
    assert form.number.data.number == 3

    class Seq2(Document):
        id = SequenceField(primary_key=True)

    for i in range(5):
        Seq2().save()

    class Seq2Form(wtforms.Form):
        seq2 = QuerySetSelectField(queryset=Seq2.objects)

    form = Seq2Form(MultiDict(seq2=3))
    number_3 = Seq2.objects.with_id(3)

    assert form.validate()
    assert isinstance(form.seq2.data, Seq2)
    assert form.seq2.data == number_3
    assert form.seq2.data.id == 3


def test_queryset_select_multiple_field(conn):
    class Country(Document):
        code = StringField(primary_key=True)

    for i in ('US', 'PE', 'BR'):
        Country(code=i).save()

    class Form(wtforms.Form):
        country = QuerySetSelectMultipleField(queryset=Country.objects)

    form = Form(MultiDict(country=['US', 'PE']))
    assert form.validate()
    assert isinstance(form.country.data, list)
    assert len(form.country.data) == 2


def test_modelselectfield_multiple_selected_elements_must_be_retained(conn):
    class Dog(Document):
        name = StringField()

        def __unicode__(self):
            return self.name

    class DogOwner(Document):
        dogs = ListField(ReferenceField(Dog))

    DogOwnerForm = model_form(DogOwner)

    fido = Dog(name="fido").save()
    Dog(name="rex").save()

    owner = DogOwner(dogs=[fido])
    form = DogOwnerForm(obj=owner)
    html = form.dogs()

    m = re.search("<option selected .+?>(.*?)</option>", html)
    assert m is not None
    assert "fido" == m.group(1)
