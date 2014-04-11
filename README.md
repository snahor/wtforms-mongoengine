WTForms-Mongoengine
===================
[![Build Status](https://drone.io/github.com/snahor/wtforms-mongoengine/status.png)](https://drone.io/github.com/snahor/wtforms-mongoengine/latest)

WTForms-Mongoengine is a fork of [Flask-Mongoengine][1] without the Flask dependency.

This package provides additional fields like:

    ModelSelectField
    ModelSelectField
    QuerySetSelectField
    QuerySetMultipleSelectField
    
Also, you can generate forms from models with `model_form`.

Examples:

    from wtforms_mongoengine import model_form
    from mongoengine import Document, StringField
    
    
    class Foo(Document):
        bar = StringField()
    
    Form = model_form(Foo)
    

  [1]: https://github.com/mongoengine/fask-mongoengine
