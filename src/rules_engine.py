class RulesEngine:
  def calculate(self, input_data):
    """
    Processes input data and calculates eligibility and supplement amount.

    Args:
      input_data (dict): JSON object with the input schema.

    Returns:
      dict: JSON object with the output schema.
    """

    id = input_data.get("id")
    family_composition = input_data.get("familyComposition")
    num_children = input_data.get("numberOfChildren", 0) # Default to zero
    in_pay_for_december = input_data.get("familyUnitInPayForDecember", False) # Default to False

    # Initialize output data structure
    output_data = {
      "id": id,
      "isEligible": False,
      "baseAmount": 0.0,
      "childrenAmount": 0.0,
      "supplementAmount": 0.0
    }

    # Check eligibility
    if not in_pay_for_december:
      return output_data  # Not eligible, return early

    # Determine base amount based on family composition
    base_amount = 0.0
    if family_composition == "single":
      if num_children == 0:
        base_amount = 60.0
      else:
        base_amount = 120.0
    elif family_composition == "couple":
      base_amount = 120.0

    # Calculate additional amount for children
    children_amount = num_children * 20.0

    # Calculate total supplement amount
    supplement_amount = base_amount + children_amount

    # Update output with calculated values
    output_data.update({
      "isEligible": True,
      "baseAmount": base_amount,
      "childrenAmount": children_amount,
      "supplementAmount": supplement_amount
    })

    return output_data
