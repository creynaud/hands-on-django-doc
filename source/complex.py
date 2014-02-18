# -*- coding: utf-8 -*-

ascii_string = "https://django-notes.herokuapp.com"
unicode_string = u"Éèêà, je suis une string unicode"

list_of_words = [u"The", "cat", "ate", "my", "source", "code"]
tuple_with_one_element = (1, )
tuple_with_several_element = (1, 2, 3)
dictionary = {'key': 'value'}
dictionary['another_key'] = 'another_value'


def print_list(notes):
    for note in notes:
        print note

def parity(n):
    if n % 2 == 0:
        return "even"
    else:
        return "odd"

class Complex(object):
    real = 0.0
    imag = 0.0

    def __init__(self, real, imag):
        super(Complex, self).__init__()
        self.real = real
        self.imag = imag

    def __unicode__(self):
        return u"{0}+i{1}".format(self.real, self.imag)

    def is_pure_real(self):
        return self.imag == 0.0
