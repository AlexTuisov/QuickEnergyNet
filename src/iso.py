class ISO:
    def __init__(self, high_price=200, low_price=50):
        """
        ISO (Independent System Operator) class responsible for market regulation.

        Args:
            high_price (float): Market price when demand cannot be met.
            low_price (float): Market price when demand is fully met.
        """
        self.high_price = high_price
        self.low_price = low_price

    def decide_action(self, timestamp, demand, controlled_producers, market_agents):
        """
        Decides the production order for each controlled producer and the price for each market agent.

        Args:
            timestamp (int): Current simulation timestamp.
            demand (float): Current market demand for electricity.
            controlled_producers (list): List of all ControlledProducer instances.
            market_agents (list): List of all MarketAgent instances.

        Returns:
            dict: {
                "production_orders": list of floats (production orders for each controlled producer),
                "agent_prices": list of dicts (prices for each market agent: {"buy_price", "sell_price"})
            }
        """
        # Step 1: Sort producers by production cost (cheapest first)
        sorted_producers = sorted(controlled_producers, key=lambda p: p.get_production_cost(p.capacity))

        # Step 2: Allocate production to meet demand
        remaining_demand = demand
        production_orders = []
        total_cost = 0
        total_capacity_used = 0

        for producer in sorted_producers:
            if remaining_demand <= 0:
                production_orders.append(0)
            else:
                production_order = min(remaining_demand, producer.capacity)
                production_cost = producer.get_production_cost(production_order)
                production_orders.append(production_order)
                total_cost += production_cost * production_order
                total_capacity_used += production_order
                remaining_demand -= production_order

        # Step 3: Determine market price based on unmet demand
        if remaining_demand > 0:
            # Demand cannot be fully met, set high price
            buy_price = self.high_price
            sell_price = self.high_price + 20  # Add margin for selling
        else:
            # Demand can be fully met, set low price
            buy_price = self.low_price
            sell_price = self.low_price + 20  # Add margin for selling

        # Step 4: Generate individual prices for market agents (using same buy/sell prices for simplicity)
        agent_prices = [
            {
                "buy_price": buy_price,
                "sell_price": sell_price
            }
            for _ in market_agents
        ]

        return {
            "production_orders": production_orders,
            "agent_prices": agent_prices
        }
