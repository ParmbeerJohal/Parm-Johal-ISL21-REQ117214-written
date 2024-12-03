import logging

logger = logging.getLogger(__name__)

class RulesEngine:
  def __isValid(self, id, family_composition, num_children, in_pay_for_december):
    """
    Private method.
    Validates input data as a security check.

    Args:
      family_composition (string): string
      num_children (int): int
      in_pay_for_december (bool): boolean

      Returns:
      boolean: True if the input data passes all validation checks.
    """
    
    if not id or id == "":
      logger.warning("Validation failed: ID not found.")
      return False
    if type(family_composition) != str or (family_composition != "single" and family_composition != "couple"):
      logger.warning("Validation failed: Invalid value for family composition.")
      return False
    if type(num_children) != int or num_children < 0:
      logger.warning("Validation failed: Invalid value for number of children.")
      return False
    if type(in_pay_for_december) != bool:
      logger.warning("Validation failed: Invalid value for family unit in pay for December.")
      return False
    logger.info("Validation successful.")
    return True
  
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

    # Validation checks
    if not self.__isValid(id, family_composition, num_children, in_pay_for_december):
      logger.info("Input data is not valid. Returning default output.")
      return output_data
    
    # Check eligibility
    if not in_pay_for_december:
      logger.info("Not eligible due to familyUnitInPayForDecember being False.")
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
    
    logger.info(f"Calculated output data: {output_data}")
    return output_data
