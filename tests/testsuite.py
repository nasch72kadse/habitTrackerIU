import unittest
from tests import test_commands, test_Habit, test_HabitCollection
from create_examples import prepare

def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    # Arrange
    prepare()
    test_suite = unittest.TestSuite()
    # Act and assert
    test_suite.addTest(unittest.makeSuite(test_commands.CommandsTest))
    test_suite.addTest(unittest.makeSuite(test_Habit.HabitTest))
    test_suite.addTest(unittest.makeSuite(test_HabitCollection.HabitCollectionTest))
    return test_suite


mySuit = suite()

runner = unittest.TextTestRunner()
runner.run(mySuit)