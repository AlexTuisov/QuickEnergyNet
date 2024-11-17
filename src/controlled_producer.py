class ControlledProducer:
    def __init__(self, producer_id, capacity, production_price_func):
        """
        ControlledProducer class represents a producer with controllable output.

        Args:
            producer_id (str): Unique identifier for the producer.
            capacity (float): Maximum production capacity of the producer.
            production_price_func (function): A function that takes a production level as input and
                                               returns the production cost per unit.
        """
        self.producer_id = producer_id
        self.capacity = capacity
        self.production_price_func = production_price_func
        self.production_order = 0  # Production order given by the ISO

    def get_production_cost(self, production_level):
        """
        Calculates the cost of production for a given production level.

        Args:
            production_level (float): The level of production to calculate the cost for.

        Returns:
            float: The cost of production per unit at the given production level.
        """
        return self.production_price_func(production_level)