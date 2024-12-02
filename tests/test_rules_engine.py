import pytest
from src.rules_engine import RulesEngine

# Test data for various scenarios
test_data = [
  # Not eligible (familyUnitInPayForDecember is False)
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": 0,
      "familyUnitInPayForDecember": False
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  },
  # Eligible single with no children
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": 0,
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": True,
      "baseAmount": 60.0,
      "childrenAmount": 0.0,
      "supplementAmount": 60.0
    }
  },
  # Eligible couple with two children
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "couple",
      "numberOfChildren": 2,
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": True,
      "baseAmount": 120.0,
      "childrenAmount": 40.0,
      "supplementAmount": 160.0
    }
  },
  # Eligible single with three children
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": 3,
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": True,
      "baseAmount": 120.0,
      "childrenAmount": 60.0,
      "supplementAmount": 180.0
    }
  },
  # Validation error on family composition
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "COUPLE", # Invalid option value
      "numberOfChildren": 2,
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  },
  # Validation error on family composition
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": 10, # Invalid value type
      "numberOfChildren": 2,
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  },
  # Validation error on number of children
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": -1, # Invalid number of children
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  },
  # Validation error on number of children
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": "Two", # Invalid value type
      "familyUnitInPayForDecember": True
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  },
  # Validation error on family unit pay for December
  {
    "input": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "familyComposition": "single",
      "numberOfChildren": 2,
      "familyUnitInPayForDecember": "True" # Invalid value type
    },
    "expected": {
      "id": "5123fd09-c862-4595-80e5-4b595fbff11c",
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }
  }
]

@pytest.mark.parametrize("data", test_data)
def test_rules_engine(data):
  engine = RulesEngine()
  output = engine.calculate(data["input"])
  assert output == data["expected"], f"Test failed for input: {data['input']}"
