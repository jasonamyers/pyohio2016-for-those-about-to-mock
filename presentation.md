# For Those About to Mock

---

## Why I Test

* Test because I'm prone to silly mistakes
* Because test a function often highlights bad function calls etc
* Test to Enforce Behaviors (Good and Bad)

---

## Testing Toolkits

* Unittest / Nose
* PyTest
* DocTests (not covering today)
* So many other things

---

![](quiet_riot.jpg)

^ Unittest is our Quiet Riot
^ Part of the Standard Library
^ Often used in conjunction with Nose
^ Built as a python class
^ Regularly coupled with Nose

[^aerokay]: http://www.deviantart.com/art/Quiet-Riot-236233999

---

![](foo_fighters.jpg)

^ Py.Test is our Foo Fighters

^ Has to be pip installed (pytest)
^ Has a bunch of extra tricks
    ^ Fixtures
    ^ Parameterized Testing
^ Works with existing Unittest, Nose, and DocTest tests

[^Jo]: https://www.flickr.com/photos/39562150@N00/1917475990

---

## Setting up a Unittest TestSuite

* built like a python module (needs a `__init__.py`)
* A class per group of tests

---

## Unittest TestSuite Example

```python
import unittest

from metal.hair import count_hairspray_cans
from rock.foo_fighters import are_the_foo_fighters_still_a_band

class TestRock(unittest.TestCase):

    def test_count_hairspray_cans(self):
        self.assertEqual(10, count_hairspray_cans())

    def test_is_rock_still_alive(self):
        self.assertTrue(are_the_foo_fighters_still_a_band())
```

---

## Setting up a Py.Test TestSuite

* `pip install pytest`
* Just a collection of Functions
* Can be grouped with classes

---

## Py.Test TestSuite Example

```python
import pytest

from metal.hair import count_hairspray_cans
from rock.foo_fighters import are_the_foo_fighters_still_a_band

class TestRock:

    def test_count_hairspray_cans(self):
        assert count_hairspray_cans() == 10

    def test_is_rock_still_alive(self):
        assert are_the_foo_fighters_still_a_band() is True
```

---

## Testing Vocabulary Lessons

^ Disclaimer all these bands are awesome, okay maybe not spinal tap. I had to find a way to work in my favorite rock covers.
---

![](spinal_tap.jpg)

^ Fake: objects actually have working implementations, but usually take some shortcut which makes them not suitable for production.

---

![](mini_kiss.jpg)

^ Mock: a class that implements an interface and allows the ability to dynamically set the values to return/exceptions to throw from particular methods and provides the ability to check if particular methods have been called/not called.

---

![](hells_belles.jpg)

^ Stub: provide canned answers to calls made during the test, usually not responding at all to anything outside what's programmed in for the test. (The Belles do originals sometimes.)

---

## Rock ain't about Vocabulary

---

![fit](school_house.jpg)

---
## Our First Code to Test

### app.py
```python
def hello_world():
    return {'message': 'Hello World'}
```
---
## Our First Test

### unittests.py
```python
import unittest

from app import hello_world


class TestFlaskApp(unittest.TestCase):

    def test_hello_world(self):
        result = hello_world()
        self.assertDictEqual({'message': 'Hello World'}, result)
```

---
```bash
(for-those-about-to-mock) ~/d/f/rock ❯❯❯ python -m unittest unittests               ⏎
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
---

### dal.py
```python
def process_results(results):
    if results.status_code == 404:
        return {'message': 'Rock Not found!'}
    elif results.status_code == 500:
        return {'message': 'Rock Imploded!'}
    elif results.status_code == 200:
        return results.json()
    else:
        return {'message': 'this function works like Ozzy - SHARON!'}
```

---

### unittests.py
```python
    def test_process_results_not_found(self):
         Faker = namedtuple("Faker", ['status_code', ])
         test_object = Faker(status_code=404)
         result = process_results(test_object)
         self.assertDictEqual({'message': 'Rock Not Found!'}, result)
```

---

```bash
(for-those-about-to-mock) ~/d/for-those-about-to-mock ❯❯❯ python -m unittest rock.unittests
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s
```

---

### dal.py
```python
def process_results(results):
    if results.status_code == 404:
        return {'message': 'Rock Not found!'}
    elif results.status_code == 500:
        return {'message': 'Rock Imploded!'}
    elif results.status_code == 200:
        return results.json()
    else:
        raise ValueError('SHARON!')
```

---

### unittests.py
```python
    def test_process_results_success(self):
        test_object = MagicMock()
        test_object.status_code = 200
        test_object.json.return_value = {'message': 'This is just a tribute!'}
        result = process_results(test_object)
        self.assertDictEqual({'message': 'This is just a tribute!'}, result)

```
---

```bash
(for-those-about-to-mock) ~/d/for-those-about-to-mock ❯❯❯ python -m unittest rock.unittests
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s
```
---

![](jagger.jpg)

^ But Umm it called that function on our test_object...

---

```python
from mock import call

class TestDal(unittest.TestCase)
    def test_process_results_success(self):
          test_object = MagicMock()
          test_object.status_code = 200
          test_object.json.return_value = {'message': 'This is just a tribute!'}
          result = process_results(test_object)
          self.assertDictEqual({'message': 'This is just a tribute!'}, result)

          expected_calls = [call.json()]
          self.assertListEqual(expected_calls, test_object.mock_calls)
  ```
---

![](mountain.jpg)

^ Mountain of Mississippi Queen Fame.

---

# Dealing with exceptions

* There's a method for that
* Drugs have side_effects

---

![](morrison.jpg)

---

```python
def test_process_results_bad_status(self):
      test_object = MagicMock()
      test_object.status_code = 'cookies'
      self.assertRaises(ValueError, process_results, test_object)

      expected_calls = []
      self.assertListEqual(expected_calls, test_object.mock_calls)
```

---

```python
def test_process_results_bad_status_message(self):
      test_object = MagicMock()
      test_object.status_code = 'cookies'
      with self.assertRaises(ValueError) as exc_info:
          process_results(test_object)

          self.assertTrue('SHARON!' in exc_info.exception)

      expected_calls = []
      self.assertListEqual(expected_calls, test_object.mock_calls)
```

---

```python
def test_process_results_bad_json_call(self):
      test_object = MagicMock()
      test_object.status_code = 200
      test_object.json.side_effects = ValueError('Nickleback')
      with self.assertRaises(ValueError) as exc_info:
          process_results(test_object)

          self.assertTrue('Nickleback' in exc_info.exception)

      expected_calls = [call.json()]
      self.assertListEqual(expected_calls, test_object.mock_calls)
```

---

![](cooper-gill.jpg)

^ Mocking built ins is ... odd

---

# Mocking builtins

* ``__builtin__`` in Python 2 (boo/hiss)
* ```builtins`` in Python 3 (cheers)

---

```python
@patch('__builtin__.open')
def test_process_file(self, open_mock):
    fake_file = BytesIO(b'Joan Jett\nJanis Joplin\nAlanis Morissette')
    expected_results = ['Joan Jett', 'Janis Joplin', 'Alanis Morissette']
    open_mock.return_value = fake_file
    results = process_file('cookies.csv')

    self.assertListEqual(expected_results, results)
```

---

![](stevie-nicks.jpg)

^ Let's take a breather like the interludes in a great Stevie Nicks song...

---
