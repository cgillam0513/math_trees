# Math Trees

Make math expressions with trees


## Getting Started
```
    git clone https://github.com/spboyle/math-trees
    cd math-trees
    pip install -r requirements_dev.txt
    python setup.py develop
```

### Running tests
`python setup.py test`


## Code Challenge
Please code the following. Feel free to add to or re-structure the project as needed.
1. Create a data structure which can represent math expressions that supports the following:
  * Real numbers
  * plus(+)
  * minus(-)
  * times(*)
  * divide(/)
2. Implement an evaluation method which calculates the value of the expression
3. Write a parser which converts an ascii string to your data structure
4. Implement a `__str__` method which converts your data structure into an ascii string equivalent
5. Make the string parser from step 3 handle parentheses ()

Please dedicate about two to four hours on this -- complete as much as you are able, but it is not required to complete every item. They are ordered by relative difficulty, so we suggest coding to each requirement in top-down order.


## Credits
This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
