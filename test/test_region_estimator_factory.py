import unittest

from region_estimators.region_estimator_factory import RegionEstimatorFactory, get_classname

class TestFactory(unittest.TestCase):
  """
  Tests for RegionEstimatorFactory.
  """

  def test_get_classname(self):
    """
    Test that the get_classname method works as expected.
    """
    self.assertEqual(get_classname('diffusion'), 'DiffusionEstimator')
    self.assertEqual(get_classname('distance-simple'), 'DistanceSimpleEstimator')
    with self.assertRaises(ValueError):
      get_classname('___')


if __name__ == '__main__':
  unittest.main()
