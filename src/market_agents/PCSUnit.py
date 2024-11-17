from src.market_agents.market_agent import MarketAgent


class PCSUnit(MarketAgent):
    def __init__(self, agent_id, max_production, internal_demand, storage_capacity, initial_storage, production_price):
        """
        SCPUnit (Storage-Controllable Production Unit) class, inherits from MarketAgent.

        Args:
            agent_id (str): Unique identifier for the agent.
            max_production (list[float]): Maximum production for each timestamp.
            internal_demand (list[float]): Internal demand for each timestamp.
            storage_capacity (float): Maximum storage capacity.
            initial_storage (float): Initial amount in storage.
            production_price (float): Cost of internal production per unit.
        """
        super().__init__(agent_id)
        self.max_production = max_production  # List of max production per timestamp
        self.internal_demand = internal_demand  # List of internal demand per timestamp
        self.storage_capacity = storage_capacity  # Max storage capacity
        self.current_storage = initial_storage  # Current storage level
        self.production_price = production_price  # Price per unit of production

    def create_order(self, timestamp, buy_price, sell_price):
        # Step 1: Calculate net demand
        net_demand = self.internal_demand[timestamp] - self.max_production[timestamp]

        # Step 2: Discharge storage to meet net demand
        storage_discharge = min(self.current_storage, max(0, net_demand))
        self.current_storage -= storage_discharge
        net_demand -= storage_discharge

        # Step 3: Buy from market if needed and cost-effective
        buy_amount = 0
        if net_demand > 0 and sell_price < self.production_price:
            buy_amount = net_demand
            net_demand = 0  # Remaining demand met

        # Step 4: Sell surplus to market if profitable
        surplus = self.max_production[timestamp] - self.internal_demand[timestamp] + storage_discharge
        sell_amount = 0
        if surplus > 0 and buy_price > self.production_price:
            sell_amount = surplus
            surplus = 0  # Remaining surplus used for selling

        # Step 5: Charge storage if there’s surplus
        storage_charge = min(surplus, self.storage_capacity - self.current_storage)
        self.current_storage += storage_charge

        # Return order
        return {
            "buy_amount": buy_amount,
            "sell_amount": sell_amount
        }

