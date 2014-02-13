Python Survival Kit
===================

.. literalinclude:: complex.py


Copy the previous code into a complex.py file, then launch the python interpreter in the directory containing the complex.py file:

.. code-block:: python

    $ python
    $ Python 2.7.5+ (default, Sep 19 2013, 13:48:49)
    [GCC 4.8.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from complex import Complex
    >>> z = Complex(1.0, 2.0)
    >>> print z
    <complex.Complex object at 0x7f37b155e3d0>
    >>> print u"{0}".format(z)
    1.0+i2.0
    >>> z.is_pure_real()
    False
    >>> import complex
    >>> print complex.dictionary
    {'another_key': 'another_value', 'key': 'value'}
    >>> print complex.dictionary['key']
    value
    >>> complex.some_function(["Test", "String"])
    Test
    String
    >>>
